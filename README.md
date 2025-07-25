# 🎵 Highrise Radio Bot

A powerful Highrise bot that integrates with the MRadio broadcasting system, allowing users to control music playback directly from a Highrise room.

## 🚀 Features

- **🎵 Music Control**: Play, skip, and manage music queue
- **📋 Queue Management**: View and modify the music queue
- **👑 Admin System**: Role-based permissions for bot commands
- **🔄 Real-time Updates**: Auto-announce new songs
- **🎯 Easy Commands**: Simple command system with help
- **⚡ Async Architecture**: High-performance async/await implementation

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Node.js (for the radio server)
- Virtual environment (recommended)

### Setup

1. **Clone or download the project files**

2. **Set up Python environment**:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install aiohttp requests websockets
```

3. **Start the Radio Server**:
```bash
# Make sure the MRadio server is running
npm install
npm start
```

4. **Configure the bot**:
   - Edit `bot_config.py`
   - Add your Highrise bot token
   - Add your room ID
   - Add admin user IDs

5. **Run the bot**:
```bash
python start_bot.py
```

## 🎮 Commands

### General Commands (All Users)
- `!help` - Show available commands
- `!current` - Show currently playing song
- `!queue` - Show music queue
- `!radio` - Show radio status

### Admin Commands
- `!play` - Resume playback
- `!skip` - Skip current song
- `!add <song_name>` - Add song to queue
- `!remove <index>` - Remove song from queue
- `!search <query>` - Search for songs (coming soon)
- `!admin <user_id>` - Add user as admin

## ⚙️ Configuration

### Bot Configuration (`bot_config.py`)

```python
# Highrise Bot Configuration
HIGHRISE_BOT_TOKEN = "your_bot_token"
ROOM_ID = "your_room_id"

# Radio Server Configuration
RADIO_API_URL = "http://localhost:9126/api"

# Default Admins
DEFAULT_ADMINS = ["user_id_1", "user_id_2"]
```

### Environment Variables

You can also use environment variables:
- `HIGHRISE_BOT_TOKEN`
- `HIGHRISE_ROOM_ID`
- `RADIO_API_URL`

## 🔧 Radio Server Setup

The bot integrates with the MRadio broadcasting system. Make sure it's running:

1. **Install dependencies**:
```bash
npm install
```

2. **Create required directories**:
```bash
mkdir -p data config media/tracks media/fallback cache
```

3. **Set up environment**:
```bash
# Create .env file with your API keys
echo "PORT=9126" > .env
echo "NODE_ENV=development" >> .env
```

4. **Start the server**:
```bash
npm start
```

## 📡 API Integration

The bot communicates with the radio server via REST API:

- **GET** `/api/songs/current` - Get currently playing song
- **GET** `/api/songs/queue` - Get music queue
- **GET** `/api/songs/skip` - Skip current song
- **POST** `/api/songs/add` - Add song to queue
- **DELETE** `/api/songs/remove/{index}` - Remove song from queue

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Highrise      │    │   Radio Bot      │    │   MRadio        │
│   Users         │◄──►│   (Python)       │◄──►│   Server        │
│                 │    │                  │    │   (Node.js)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
        │                        │                        │
        │                        │                        │
        ▼                        ▼                        ▼
   Chat Commands           WebSocket/HTTP            Audio Stream
   (!play, !skip)          Communication            (localhost:9126)
```

## 🛠️ Development

### Project Structure
```
├── highrise_radio_bot.py  # Main bot implementation
├── bot_config.py          # Configuration settings
├── start_bot.py           # Startup script
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── server/               # Radio server files
    ├── index.js
    ├── api/
    ├── lib/
    └── services/
```

### Adding New Commands

1. Add command to `self.commands` dict in `HighriseRadioBot`
2. Implement the command method following the pattern:
```python
async def cmd_your_command(self, user_id: str, args: list, is_admin: bool):
    # Your command implementation
    await self.send_message("Response message")
```

### Extending API Integration

Add new endpoints in `bot_config.py`:
```python
RADIO_ENDPOINTS = {
    "your_endpoint": "api/your/endpoint",
}
```

## 🎯 Usage Examples

### Basic Usage
```
User: !current
Bot: 🎵 Now Playing: Despacito by Luis Fonsi

User: !queue
Bot: 📋 Song Queue:
     1. Shape of You by Ed Sheeran
     2. Blinding Lights by The Weeknd
     3. Levitating by Dua Lipa

Admin: !skip
Bot: ⏭️ Song skipped!

Admin: !add bohemian rhapsody
Bot: ✅ Added 'bohemian rhapsody' to queue!
```

### Admin Management
```
Admin: !admin user123
Bot: ✅ Added user123 as admin!

New Admin: !remove 2
Bot: ✅ Removed song at position 2 from queue!
```

## 🔒 Security

- **Admin-only commands**: Sensitive operations require admin privileges
- **Input validation**: All user inputs are validated
- **Error handling**: Graceful error handling prevents crashes
- **Rate limiting**: Built-in protection against spam (configurable)

## 🐛 Troubleshooting

### Common Issues

1. **Bot not responding**:
   - Check if radio server is running on port 9126
   - Verify bot token and room ID in config
   - Check network connectivity

2. **API errors**:
   - Ensure MRadio server is properly configured
   - Check server logs for errors
   - Verify API endpoints are accessible

3. **Permission errors**:
   - Make sure admin user IDs are correctly configured
   - Check user permissions in Highrise

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📜 License

This project is open source. Feel free to modify and distribute according to your needs.

## 🆘 Support

For support and questions:
- Check the troubleshooting section
- Review server logs
- Open an issue with detailed information

## 🚀 Future Features

- [ ] Song search functionality
- [ ] Volume control
- [ ] Playlist management
- [ ] User song requests
- [ ] Advanced queue management
- [ ] Music recommendations
- [ ] Statistics and analytics
- [ ] Custom command aliases
- [ ] Multi-room support

---

**Happy Broadcasting! 🎵**
