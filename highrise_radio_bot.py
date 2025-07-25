#!/usr/bin/env python3
"""
Highrise Radio Bot - A bot that integrates with the MRadio broadcasting system
"""

import asyncio
import json
import logging
import aiohttp
import websockets
from typing import Dict, Any, Optional
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HighriseRadioBot:
    def __init__(self, bot_token: str, room_id: str, radio_api_url: str = "http://localhost:9126/api"):
        self.bot_token = bot_token
        self.room_id = room_id
        self.radio_api_url = radio_api_url
        self.websocket = None
        self.session = None
        self.current_song = None
        self.admins = set()  # Set of admin user IDs
        
        # Bot commands
        self.commands = {
            "!play": self.cmd_play,
            "!skip": self.cmd_skip,
            "!current": self.cmd_current,
            "!queue": self.cmd_queue,
            "!search": self.cmd_search,
            "!volume": self.cmd_volume,
            "!help": self.cmd_help,
            "!radio": self.cmd_radio_status,
            "!add": self.cmd_add_song,
            "!remove": self.cmd_remove_song,
            "!admin": self.cmd_admin,
        }
    
    async def start(self):
        """Start the bot"""
        logger.info("Starting Highrise Radio Bot...")
        self.session = aiohttp.ClientSession()
        
        try:
            await self.connect_to_highrise()
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
        finally:
            if self.session:
                await self.session.close()
    
    async def connect_to_highrise(self):
        """Connect to Highrise WebSocket"""
        # Note: This is a simplified WebSocket connection
        # In a real implementation, you'd use the actual Highrise WebSocket API
        uri = f"wss://highrise-websocket-url/rooms/{self.room_id}"
        
        try:
            # For demonstration, we'll simulate the connection
            logger.info("Simulating Highrise connection...")
            await self.simulate_bot_activity()
        except Exception as e:
            logger.error(f"WebSocket connection failed: {e}")
    
    async def simulate_bot_activity(self):
        """Simulate bot activity for demonstration"""
        logger.info("Bot is now active and listening for commands...")
        
        # Simulate some user messages
        test_messages = [
            {"user": "user123", "message": "!help", "is_admin": True},
            {"user": "user456", "message": "!current", "is_admin": False},
            {"user": "user123", "message": "!search despacito", "is_admin": True},
            {"user": "user789", "message": "!queue", "is_admin": False},
        ]
        
        # Add admin
        self.admins.add("user123")
        
        for msg in test_messages:
            await asyncio.sleep(2)
            await self.handle_message(msg)
            
        # Keep the bot running
        while True:
            await asyncio.sleep(10)
            await self.check_radio_status()
    
    async def handle_message(self, message_data: Dict[str, Any]):
        """Handle incoming messages"""
        user_id = message_data.get("user")
        message = message_data.get("message", "").strip()
        is_admin = message_data.get("is_admin", False)
        
        if not message.startswith("!"):
            return
        
        command_parts = message.split()
        command = command_parts[0].lower()
        args = command_parts[1:] if len(command_parts) > 1 else []
        
        if command in self.commands:
            try:
                await self.commands[command](user_id, args, is_admin)
            except Exception as e:
                logger.error(f"Error executing command {command}: {e}")
                await self.send_message(f"Error executing command: {str(e)}")
        else:
            await self.send_message(f"Unknown command: {command}. Type !help for available commands.")
    
    async def send_message(self, message: str):
        """Send a message to the Highrise room"""
        logger.info(f"[BOT]: {message}")
        # In a real implementation, this would send via Highrise WebSocket
        
    async def radio_api_request(self, endpoint: str, method: str = "GET", data: Dict = None) -> Optional[Dict]:
        """Make a request to the radio API"""
        url = f"{self.radio_api_url}/{endpoint.lstrip('/')}"
        
        try:
            if method == "GET":
                async with self.session.get(url) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"API request failed: {response.status}")
                        return None
            elif method == "POST":
                async with self.session.post(url, json=data) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"API request failed: {response.status}")
                        return None
            elif method == "DELETE":
                async with self.session.delete(url) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"API request failed: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Radio API request error: {e}")
            return None
    
    # Command implementations
    async def cmd_help(self, user_id: str, args: list, is_admin: bool):
        """Show help message"""
        help_text = """
🎵 **Radio Bot Commands** 🎵

**General Commands:**
• !current - Show currently playing song
• !queue - Show song queue
• !radio - Show radio status
• !help - Show this help message

**Music Control** (Admin only):
• !play - Resume playback
• !skip - Skip current song
• !search <query> - Search for songs
• !add <song_name> - Add song to queue
• !remove <index> - Remove song from queue

**Admin Commands:**
• !admin <user_id> - Add user as admin
        """
        await self.send_message(help_text)
    
    async def cmd_current(self, user_id: str, args: list, is_admin: bool):
        """Show currently playing song"""
        result = await self.radio_api_request("songs/current")
        if result:
            song_info = result.get("song", {})
            title = song_info.get("title", "Unknown")
            artist = song_info.get("artist", "Unknown")
            await self.send_message(f"🎵 Now Playing: {title} by {artist}")
        else:
            await self.send_message("❌ Could not get current song info")
    
    async def cmd_queue(self, user_id: str, args: list, is_admin: bool):
        """Show song queue"""
        result = await self.radio_api_request("songs/queue")
        if result and isinstance(result, list):
            if not result:
                await self.send_message("📋 Queue is empty")
                return
            
            queue_text = "📋 **Song Queue:**\n"
            for i, song in enumerate(result[:5], 1):  # Show first 5 songs
                title = song.get("title", "Unknown")
                artist = song.get("artist", "Unknown")
                queue_text += f"{i}. {title} by {artist}\n"
            
            if len(result) > 5:
                queue_text += f"... and {len(result) - 5} more songs"
            
            await self.send_message(queue_text)
        else:
            await self.send_message("❌ Could not get queue info")
    
    async def cmd_radio_status(self, user_id: str, args: list, is_admin: bool):
        """Show radio status"""
        current = await self.radio_api_request("songs/current")
        queue = await self.radio_api_request("songs/queue")
        
        if current and queue is not None:
            song_info = current.get("song", {})
            title = song_info.get("title", "Unknown")
            artist = song_info.get("artist", "Unknown")
            queue_length = len(queue) if isinstance(queue, list) else 0
            
            status_text = f"""
📻 **Radio Status**
🎵 Current: {title} by {artist}
📋 Queue: {queue_length} songs
🔗 Stream: http://localhost:9126/stream
            """
            await self.send_message(status_text)
        else:
            await self.send_message("❌ Could not get radio status")
    
    async def cmd_skip(self, user_id: str, args: list, is_admin: bool):
        """Skip current song (admin only)"""
        if not self.is_admin(user_id):
            await self.send_message("❌ Only admins can skip songs")
            return
        
        result = await self.radio_api_request("songs/skip")
        if result:
            await self.send_message("⏭️ Song skipped!")
        else:
            await self.send_message("❌ Could not skip song")
    
    async def cmd_search(self, user_id: str, args: list, is_admin: bool):
        """Search for songs"""
        if not args:
            await self.send_message("❌ Please provide a search query. Usage: !search <song name>")
            return
        
        query = " ".join(args)
        await self.send_message(f"🔍 Searching for: {query}")
        
        # Note: The radio API might not have a direct search endpoint
        # This is a placeholder for demonstration
        await self.send_message("🎵 Search feature coming soon! Use !add <song_name> to add songs directly.")
    
    async def cmd_add_song(self, user_id: str, args: list, is_admin: bool):
        """Add song to queue (admin only)"""
        if not self.is_admin(user_id):
            await self.send_message("❌ Only admins can add songs")
            return
        
        if not args:
            await self.send_message("❌ Please provide a song name. Usage: !add <song name>")
            return
        
        song_name = " ".join(args)
        data = {"song": song_name, "requestedBy": user_id}
        
        result = await self.radio_api_request("songs/add", "POST", data)
        if result:
            await self.send_message(f"✅ Added '{song_name}' to queue!")
        else:
            await self.send_message(f"❌ Could not add '{song_name}' to queue")
    
    async def cmd_remove_song(self, user_id: str, args: list, is_admin: bool):
        """Remove song from queue (admin only)"""
        if not self.is_admin(user_id):
            await self.send_message("❌ Only admins can remove songs")
            return
        
        if not args or not args[0].isdigit():
            await self.send_message("❌ Please provide a valid queue index. Usage: !remove <index>")
            return
        
        index = int(args[0]) - 1  # Convert to 0-based index
        result = await self.radio_api_request(f"songs/remove/{index}", "DELETE")
        
        if result:
            await self.send_message(f"✅ Removed song at position {args[0]} from queue!")
        else:
            await self.send_message(f"❌ Could not remove song at position {args[0]}")
    
    async def cmd_play(self, user_id: str, args: list, is_admin: bool):
        """Resume playback (admin only)"""
        if not self.is_admin(user_id):
            await self.send_message("❌ Only admins can control playback")
            return
        
        await self.send_message("▶️ Playback resumed!")
    
    async def cmd_volume(self, user_id: str, args: list, is_admin: bool):
        """Control volume (admin only)"""
        if not self.is_admin(user_id):
            await self.send_message("❌ Only admins can control volume")
            return
        
        await self.send_message("🔊 Volume control coming soon!")
    
    async def cmd_admin(self, user_id: str, args: list, is_admin: bool):
        """Add admin (existing admin only)"""
        if not self.is_admin(user_id):
            await self.send_message("❌ Only admins can add other admins")
            return
        
        if not args:
            await self.send_message("❌ Please provide a user ID. Usage: !admin <user_id>")
            return
        
        new_admin = args[0]
        self.admins.add(new_admin)
        await self.send_message(f"✅ Added {new_admin} as admin!")
    
    def is_admin(self, user_id: str) -> bool:
        """Check if user is admin"""
        return user_id in self.admins
    
    async def check_radio_status(self):
        """Periodically check radio status"""
        try:
            current = await self.radio_api_request("songs/current")
            if current:
                song_info = current.get("song", {})
                if song_info != self.current_song:
                    self.current_song = song_info
                    title = song_info.get("title", "Unknown")
                    artist = song_info.get("artist", "Unknown")
                    await self.send_message(f"🎵 Now Playing: {title} by {artist}")
        except Exception as e:
            logger.error(f"Error checking radio status: {e}")

async def main():
    """Main function to run the bot"""
    # Configuration - replace with your actual values
    BOT_TOKEN = "your_highrise_bot_token"
    ROOM_ID = "your_room_id"
    RADIO_API_URL = "http://localhost:9126/api"
    
    bot = HighriseRadioBot(BOT_TOKEN, ROOM_ID, RADIO_API_URL)
    await bot.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")