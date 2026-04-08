from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# ─── Auth ───
class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=6)
    display_name: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    display_name: str

# ─── Chat Room ───
class CreateRoomRequest(BaseModel):
    title: str = Field(default="การสนทนาใหม่", max_length=100)

class RoomResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    last_activity_at: Optional[datetime] = None
    message_count: int = 0

# ─── Message ───
class SendMessageRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)

class MessageResponse(BaseModel):
    id: str
    role: str          # "user" | "assistant"
    content: str
    created_at: datetime

# ─── Chat (ส่ง message และรับ response พร้อมกัน) ───
class ChatResponse(BaseModel):
    user_message: MessageResponse
    bot_message: MessageResponse
    room_id: str
