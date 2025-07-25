#!/usr/bin/env python3
"""
Startup script for Highrise Radio Bot
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from highrise_radio_bot import HighriseRadioBot
from bot_config import HIGHRISE_BOT_TOKEN, ROOM_ID, RADIO_API_URL, DEFAULT_ADMINS

async def main():
    print("🎵 Starting Highrise Radio Bot...")
    print("=" * 50)
    
    # Validate configuration
    if HIGHRISE_BOT_TOKEN == "your_highrise_bot_token_here":
        print("❌ Please configure your Highrise bot token in bot_config.py")
        return
    
    if ROOM_ID == "your_room_id_here":
        print("❌ Please configure your room ID in bot_config.py")
        return
    
    # Create and start the bot
    bot = HighriseRadioBot(HIGHRISE_BOT_TOKEN, ROOM_ID, RADIO_API_URL)
    
    # Add default admins
    for admin in DEFAULT_ADMINS:
        if admin not in ["admin_user_id_1", "admin_user_id_2"]:
            bot.admins.add(admin)
    
    print(f"🔗 Radio API: {RADIO_API_URL}")
    print(f"🏠 Room ID: {ROOM_ID}")
    print(f"👑 Admins: {len(bot.admins)}")
    print("=" * 50)
    
    await bot.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"💥 Bot crashed: {e}")
        sys.exit(1)