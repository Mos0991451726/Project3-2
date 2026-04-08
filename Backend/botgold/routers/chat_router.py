from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from bson import ObjectId
from database import get_db
from models import CreateRoomRequest, SendMessageRequest, ChatResponse, MessageResponse, RoomResponse
from auth import get_current_user
import chatbot

router = APIRouter(prefix="/chat", tags=["Chat"])

def fmt_id(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc

# ─── Rooms ───

@router.get("/rooms")
async def list_rooms(user=Depends(get_current_user)):
    db = get_db()
    cursor = db.chat_rooms.find(
        {"user_id": user["_id"], "status": "active"},
        sort=[("last_activity_at", -1)]
    ).limit(50)
    rooms = []
    async for r in cursor:
        # นับจำนวน messages
        count = await db.messages.count_documents({"room_id": r["_id"]})
        rooms.append({
            "id":               str(r["_id"]),
            "title":            r["title"],
            "created_at":       r["created_at"],
            "last_activity_at": r.get("last_activity_at"),
            "message_count":    count,
        })
    return rooms


@router.post("/rooms", status_code=201)
async def create_room(body: CreateRoomRequest, user=Depends(get_current_user)):
    db = get_db()
    now = datetime.utcnow()
    doc = {
        "user_id":          user["_id"],
        "title":            body.title,
        "status":           "active",
        "last_activity_at": now,
        "created_at":       now,
        "updated_at":       now,
    }
    result = await db.chat_rooms.insert_one(doc)
    return {"id": str(result.inserted_id), "title": body.title, "created_at": now}


@router.delete("/rooms/{room_id}")
async def delete_room(room_id: str, user=Depends(get_current_user)):
    db = get_db()
    room = await db.chat_rooms.find_one({"_id": ObjectId(room_id), "user_id": user["_id"]})
    if not room:
        raise HTTPException(status_code=404, detail="ไม่พบห้องแชท")
    await db.chat_rooms.update_one(
        {"_id": ObjectId(room_id)},
        {"$set": {"status": "archived"}}
    )
    return {"message": "ลบห้องแชทสำเร็จ"}


# ─── Messages ───

@router.get("/rooms/{room_id}/messages")
async def get_messages(room_id: str, user=Depends(get_current_user)):
    db = get_db()
    room = await db.chat_rooms.find_one({"_id": ObjectId(room_id), "user_id": user["_id"]})
    if not room:
        raise HTTPException(status_code=404, detail="ไม่พบห้องแชท")

    cursor = db.messages.find(
        {"room_id": ObjectId(room_id)},
        sort=[("created_at", 1)]
    )
    messages = []
    async for m in cursor:
        messages.append({
            "id":         str(m["_id"]),
            "role":       m["role"],
            "content":    m["content"],
            "created_at": m["created_at"],
        })
    return messages


@router.post("/rooms/{room_id}/messages", response_model=ChatResponse)
async def send_message(room_id: str, body: SendMessageRequest, user=Depends(get_current_user)):
    db = get_db()

    # ตรวจสอบ room
    room = await db.chat_rooms.find_one({"_id": ObjectId(room_id), "user_id": user["_id"]})
    if not room:
        raise HTTPException(status_code=404, detail="ไม่พบห้องแชท")

    now = datetime.utcnow()

    # บันทึก user message
    user_msg_doc = {
        "room_id":    ObjectId(room_id),
        "user_id":    user["_id"],
        "role":       "user",
        "content":    body.content,
        "created_at": now,
    }
    user_result = await db.messages.insert_one(user_msg_doc)

    # อัพเดท title ห้อง (ถ้ายังเป็นชื่อ default)
    if room["title"] == "การสนทนาใหม่" and len(body.content) > 0:
        short_title = body.content[:40] + ("..." if len(body.content) > 40 else "")
        await db.chat_rooms.update_one(
            {"_id": ObjectId(room_id)},
            {"$set": {"title": short_title}}
        )

    # ─── เรียก RAG Bot ───
    bot_answer = chatbot.ask(body.content)

    # บันทึก bot message
    bot_now = datetime.utcnow()
    bot_msg_doc = {
        "room_id":    ObjectId(room_id),
        "user_id":    user["_id"],
        "role":       "assistant",
        "content":    bot_answer,
        "created_at": bot_now,
    }
    bot_result = await db.messages.insert_one(bot_msg_doc)

    # อัพเดท last_activity
    await db.chat_rooms.update_one(
        {"_id": ObjectId(room_id)},
        {"$set": {"last_activity_at": bot_now, "updated_at": bot_now}}
    )

    return ChatResponse(
        room_id=room_id,
        user_message=MessageResponse(
            id=str(user_result.inserted_id),
            role="user",
            content=body.content,
            created_at=now,
        ),
        bot_message=MessageResponse(
            id=str(bot_result.inserted_id),
            role="assistant",
            content=bot_answer,
            created_at=bot_now,
        ),
    )


# ─── Quick Chat (ไม่ต้องสร้าง room ก่อน) ───

@router.post("/quick")
async def quick_chat(body: SendMessageRequest, user=Depends(get_current_user)):
    """สร้างห้องใหม่อัตโนมัติแล้วส่งข้อความ"""
    db = get_db()
    now = datetime.utcnow()

    short_title = body.content[:40] + ("..." if len(body.content) > 40 else "")
    room_doc = {
        "user_id":          user["_id"],
        "title":            short_title,
        "status":           "active",
        "last_activity_at": now,
        "created_at":       now,
        "updated_at":       now,
    }
    room_result = await db.chat_rooms.insert_one(room_doc)
    room_id = str(room_result.inserted_id)

    # ส่งข้อความ
    user_msg = {
        "room_id":    room_result.inserted_id,
        "user_id":    user["_id"],
        "role":       "user",
        "content":    body.content,
        "created_at": now,
    }
    user_result = await db.messages.insert_one(user_msg)

    bot_answer = chatbot.ask(body.content)
    bot_now = datetime.utcnow()
    bot_msg = {
        "room_id":    room_result.inserted_id,
        "user_id":    user["_id"],
        "role":       "assistant",
        "content":    bot_answer,
        "created_at": bot_now,
    }
    bot_result = await db.messages.insert_one(bot_msg)

    await db.chat_rooms.update_one(
        {"_id": room_result.inserted_id},
        {"$set": {"last_activity_at": bot_now}}
    )

    return ChatResponse(
        room_id=room_id,
        user_message=MessageResponse(id=str(user_result.inserted_id), role="user", content=body.content, created_at=now),
        bot_message=MessageResponse(id=str(bot_result.inserted_id), role="assistant", content=bot_answer, created_at=bot_now),
    )
