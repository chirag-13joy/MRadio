#!/usr/bin/env python3
"""
Test script for Highrise Radio Bot
"""

import asyncio
import aiohttp
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from highrise_radio_bot import HighriseRadioBot

async def test_bot():
    """Test bot functionality"""
    print("🧪 Testing Highrise Radio Bot...")
    print("=" * 50)
    
    # Create a test bot instance
    bot = HighriseRadioBot("test_token", "test_room", "http://localhost:9126/api")
    bot.session = aiohttp.ClientSession()
    
    # Add a test admin
    bot.admins.add("test_admin")
    
    try:
        # Test commands
        test_commands = [
            {"user": "test_admin", "message": "!help", "is_admin": True},
            {"user": "test_user", "message": "!current", "is_admin": False},
            {"user": "test_admin", "message": "!queue", "is_admin": True},
            {"user": "test_user", "message": "!skip", "is_admin": False},  # Should fail
            {"user": "test_admin", "message": "!admin test_user2", "is_admin": True},
        ]
        
        print("📝 Testing commands...")
        for i, cmd in enumerate(test_commands, 1):
            print(f"\n{i}. Testing: {cmd['message']} (User: {cmd['user']})")
            await bot.handle_message(cmd)
            await asyncio.sleep(1)
        
        print("\n✅ All tests completed!")
        print(f"👑 Current admins: {list(bot.admins)}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        await bot.session.close()

async def test_radio_connection():
    """Test radio server connection"""
    print("\n🔗 Testing Radio Server Connection...")
    
    try:
        async with aiohttp.ClientSession() as session:
            # Test if radio server is running
            async with session.get("http://localhost:9126/api/songs/queue") as response:
                if response.status == 200:
                    print("✅ Radio server is running and responding!")
                    data = await response.json()
                    print(f"📋 Queue length: {len(data) if isinstance(data, list) else 'Unknown'}")
                else:
                    print(f"⚠️ Radio server responded with status: {response.status}")
    except Exception as e:
        print(f"❌ Could not connect to radio server: {e}")
        print("💡 Make sure the radio server is running with: npm start")

if __name__ == "__main__":
    print("🎵 Highrise Radio Bot Test Suite")
    print("=" * 50)
    
    try:
        # Run tests
        asyncio.run(test_radio_connection())
        asyncio.run(test_bot())
        
        print("\n🎉 Test suite completed!")
        
    except KeyboardInterrupt:
        print("\n🛑 Tests stopped by user")
    except Exception as e:
        print(f"💥 Test suite failed: {e}")
        sys.exit(1)