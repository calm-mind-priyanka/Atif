user_settings = {}

def get_user_settings(user_id):
    default = {
        "spell_check": True,
        "auto_delete": False,
        "delete_time": "2m",
        "result_mode": "button",
        "caption": None,
        "shortlinks": {"1": "", "2": ""},  # up to 2 shorteners
        "file_secure": False,

        # These were missing:
        "force_channels": [],
        "max_results": 5,
        "imdb": False,
        "file_mode": {
            "type": "verify",  # or shortlink
            "second_verify": False,
            "verify_time": "300",  # in seconds
            "log_channel": ""
        },
        "tutorial_links": {
            "first": "",
            "second": ""
        },
        "awaiting_input": None
    }
    return user_settings.setdefault(user_id, default)
