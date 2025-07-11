from database import get_collection  # ✅ Use dynamic DB getter

# MongoDB collection
settings_col = get_collection("group_settings")  # ✅ Replaces direct db["group_settings"]

# Default group settings
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


# Fetch settings for a group (returns dict)
def get_group_settings(group_id: int) -> dict:
    group_id = str(group_id)
    data = settings_col.find_one({"_id": group_id})
    if not data:
        settings_col.insert_one({"_id": group_id, **DEFAULT_SETTINGS})
        return DEFAULT_SETTINGS.copy()

    # Ensure all keys exist (for backward compatibility)
    updated = False
    for key in DEFAULT_SETTINGS:
        if key not in data:
            data[key] = DEFAULT_SETTINGS[key]
            updated = True

    if updated:
        settings_col.update_one({"_id": group_id}, {"$set": data})

    data.pop("_id", None)
    return data


# Save updated settings for a group
def update_group_settings(group_id: int, updated_data: dict):
    group_id = str(group_id)
    settings_col.update_one({"_id": group_id}, {"$set": updated_data}, upsert=True)
