import motor.motor_asyncio
from config import MONGO_DB_URI_1, MONGO_DB_URI_2, USE_BACKUP_DB

client_1 = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI_1)
client_2 = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI_2)

db_primary = client_1["autofilter"]
db_backup = client_2["autofilter"]


def get_collection(name: str):
    """
    Returns a MongoDB collection from the primary DB.
    If it fails and USE_BACKUP_DB is True, returns from backup DB.
    """
    try:
        # Try accessing primary DB collection
        _ = db_primary.list_collection_names()  # Trigger a request
        return db_primary[name]
    except Exception:
        if USE_BACKUP_DB:
            return db_backup[name]
        raise
