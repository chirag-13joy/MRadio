"""
Configuration file for Highrise Radio Bot
"""

# Highrise Bot Configuration
HIGHRISE_BOT_TOKEN = "your_highrise_bot_token_here"
ROOM_ID = "your_room_id_here"

# Radio Server Configuration
RADIO_API_URL = "http://localhost:9126/api"
RADIO_STREAM_URL = "http://localhost:9126/stream"

# Bot Settings
DEFAULT_ADMINS = ["admin_user_id_1", "admin_user_id_2"]  # Add your admin user IDs here
BOT_PREFIX = "!"
MAX_QUEUE_DISPLAY = 5

# API Endpoints (you can modify these if needed)
RADIO_ENDPOINTS = {
    "current": "songs/current",
    "queue": "songs/queue",
    "skip": "songs/skip",
    "add": "songs/add",
    "remove": "songs/remove/{index}",
    "upcoming": "songs/upcoming",
    "block": "songs/block",
    "unblock": "songs/block/{song_name}",
}

# Messages Configuration
MESSAGES = {
    "welcome": "🎵 Radio Bot is now online! Type !help for commands.",
    "admin_only": "❌ Only admins can use this command.",
    "invalid_command": "❌ Unknown command. Type !help for available commands.",
    "api_error": "❌ Could not connect to radio server.",
    "queue_empty": "📋 The music queue is empty.",
    "song_added": "✅ Added '{song}' to the queue!",
    "song_removed": "✅ Removed song from queue!",
    "song_skipped": "⏭️ Song skipped!",
    "now_playing": "🎵 Now Playing: {title} by {artist}",
}

# Feature Flags
FEATURES = {
    "auto_announce_songs": True,
    "admin_commands": True,
    "queue_management": True,
    "song_search": False,  # Set to True when search is implemented
    "volume_control": False,  # Set to True when volume control is implemented
}