import motor.motor_asyncio
from config import MONGO_DB_URI_1, MONGO_DB_URI_2

client_1 = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI_1)
client_2 = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI_2)

db = client_1["autofilter"]
db_backup = client_2["autofilter"]
