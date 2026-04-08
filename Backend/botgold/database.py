from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

client: AsyncIOMotorClient = None
db = None

async def connect_db():
    global client, db
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.DB_NAME]

    # สร้าง indexes
    await db.users.create_index("username", unique=True)
    await db.users.create_index("email", unique=True, sparse=True)
    await db.sessions.create_index("token", unique=True)
    await db.sessions.create_index("user_id")
    await db.sessions.create_index("expires_at", expireAfterSeconds=0)  # TTL
    await db.chat_rooms.create_index("user_id")
    await db.messages.create_index([("room_id", 1), ("created_at", 1)])

    print(f"✅ MongoDB connected: {settings.DB_NAME}")

async def close_db():
    global client
    if client:
        client.close()
        print("MongoDB disconnected")

def get_db():
    return db
