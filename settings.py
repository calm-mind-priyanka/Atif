from database import db

# MongoDB collection
settings_col = db["user_settings"]

# Default settings
DEFAULT_SETTINGS = {
    "spell_check": True,
    "auto_delete": False,
    "delete_time": "2m",
    "result_mode": "button",
    "caption": None,
    "shortlinks": {"1": "", "2": ""},
    "file_secure": False,
    "force_channels": [],
    "max_results": 5,
    "imdb": False,
    "file_mode": {
        "type": "verify",
        "second_verify": False,
        "verify_time": "300",
        "log_channel": ""
    },
    "tutorial_links": {
        "first": "",
        "second": ""
    },
    "awaiting_input": None
}


# Fetch settings for a user (returns dict)
def get_user_settings(user_id: int) -> dict:
    user_id = str(user_id)
    user_data = settings_col.find_one({"_id": user_id})
    if not user_data:
        # Insert default if not exists
        settings_col.insert_one({"_id": user_id, **DEFAULT_SETTINGS})
        return DEFAULT_SETTINGS.copy()
    
    # Ensure all keys exist (in case bot was updated)
    updated = False
    for key in DEFAULT_SETTINGS:
        if key not in user_data:
            user_data[key] = DEFAULT_SETTINGS[key]
            updated = True
    if updated:
        settings_col.update_one({"_id": user_id}, {"$set": user_data})
    user_data.pop("_id", None)
    return user_data


# Save updated settings
def update_user_settings(user_id: int, updated_data: dict):
    user_id = str(user_id)
    settings_col.update_one({"_id": user_id}, {"$set": updated_data}, upsert=True)
