data_username_tracker_plateforms = {
    "Steam": {
        "url": "https://steamcommunity.com/id/%USERNAME%",
        "method": "get",
        "verification": "username",
        "except": None
    },
    "Telegram": {
        "url": "https://t.me/%USERNAME%",
        "method": "get",
        "verification": "username",
        "except": [
            "if you have telegram, you can contact @%USERNAME% right away.",
            "resolve?domain=%USERNAME%",
            "telegram: contact @%USERNAME%"
        ]
    },
    "TikTok": {
        "url": "https://www.tiktok.com/@%USERNAME%",
        "method": "get",
        "verification": "username",
        "except": ["\\u002f@%USERNAME%\""]
    },
    "Instagram": {
        "url": "https://www.instagram.com/%USERNAME%",
        "method": "get",
        "verification": "username",
        "except": None
    },
    "GitHub": {
        "url": "https://github.com/%USERNAME%",
        "method": "get",
        "verification": "status",
        "except": None
    },
    "YouTube": {
        "url": "https://www.youtube.com/@%USERNAME%",
        "method": "get",
        "verification": "username",
        "except": None
    },
    "Reddit": {
        "url": "https://reddit.com/user/%USERNAME%",
        "method": "get",
        "verification": "status",
        "except": None
    },
    "Twitch": {
        "url": "https://www.twitch.tv/%USERNAME%",
        "method": "get",
        "verification": "username",
        "except": None
    }
}