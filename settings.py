user_settings = {}

def get_user_settings(user_id):
    default = {
        "spell_check": True,
        "auto_delete": False,
        "delete_time": "2m",
        "result_mode": "button",
        "caption": None,
        "shortlinks": {"1": "", "2": ""},
        "file_secure": False
    }
    return user_settings.setdefault(user_id, default)
