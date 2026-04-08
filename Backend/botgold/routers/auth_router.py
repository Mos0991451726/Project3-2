from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from bson import ObjectId
from database import get_db
from models import RegisterRequest, LoginRequest, TokenResponse
from auth import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", status_code=201)
async def register(body: RegisterRequest):
    db = get_db()

    # เช็ค username ซ้ำ
    if await db.users.find_one({"username": body.username}):
        raise HTTPException(status_code=400, detail="Username นี้มีแล้ว")

    now = datetime.utcnow()
    user_doc = {
        "username":     body.username,
        "password":     hash_password(body.password),
        "display_name": body.display_name or body.username,
        "avatar_url":   None,
        "role":         "user",
        "is_active":    True,
        "last_login_at": None,
        "created_at":   now,
        "updated_at":   now,
    }
    result = await db.users.insert_one(user_doc)
    return {"message": "สมัครสมาชิกสำเร็จ", "user_id": str(result.inserted_id)}


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest):
    db = get_db()
    user = await db.users.find_one({"username": body.username})

    if not user or not verify_password(body.password, user["password"]):
        raise HTTPException(status_code=401, detail="Username หรือ Password ไม่ถูกต้อง")

    if not user.get("is_active", True):
        raise HTTPException(status_code=403, detail="บัญชีถูกระงับ")

    # อัพเดท last_login
    await db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"last_login_at": datetime.utcnow()}}
    )

    token = create_token(str(user["_id"]), user["username"])

    # บันทึก session
    await db.sessions.insert_one({
        "user_id":   user["_id"],
        "token":     token,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "expires_at": None,
    })

    return TokenResponse(
        access_token=token,
        username=user["username"],
        display_name=user.get("display_name", user["username"]),
    )


@router.post("/logout")
async def logout(token: str):
    db = get_db()
    await db.sessions.update_one(
        {"token": token},
        {"$set": {"is_active": False}}
    )
    return {"message": "ออกจากระบบสำเร็จ"}
