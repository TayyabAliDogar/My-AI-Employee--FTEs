# 🎬 AI EMPLOYEE - MASTER DEMO GUIDE

## 📹 3-Minute Technical Demonstration
**Submission:** Forms.gle/JR9T1SJq5rmQyGkGA

---

## 🚀 QUICK START (For Video Recording)

### Windows:
```bash
# Double-click or run:
run-demo.bat
```

### Linux/Mac:
```bash
chmod +x run-demo.sh
./run-demo.sh
```

### Manual Python:
```bash
python demo-master.py
```

---

## 📊 WHAT THE DEMO SHOWS

### 🥉 **BRONZE TIER** (30 seconds)
**Core Infrastructure & Setup Check**
- ✓ Python environment verification
- ✓ Environment variables check
- ✓ Directory structure validation
- ✓ Dependencies verification
- ✓ Real-time status display

### 🥈 **SILVER TIER** (60 seconds)
**API Connections & Watcher Initialization**
- ✓ Instagram API connection test
- ✓ Facebook API connection test
- ✓ Odoo connection verification
- ✓ Watcher scripts validation
- ✓ Live API responses shown

### 🏆 **GOLD TIER** (90 seconds)
**Autonomous Agent - Live Action**
- ✓ AI decision-making process
- ✓ **LIVE Instagram post creation**
- ✓ Real-time API calls visible
- ✓ Success confirmation with Post ID
- ✓ Autonomous action completed

---

## 🎥 RECORDING TIPS

### Before Recording:
1. **Maximize terminal window** for better visibility
2. **Ensure .env file has valid credentials** (Instagram/Facebook tokens)
3. **Close unnecessary applications** to avoid notifications
4. **Test run once** to ensure everything works

### During Recording:
1. Start recording software (OBS, Loom, etc.)
2. Run `run-demo.bat` (Windows) or `./run-demo.sh` (Linux/Mac)
3. Let the demo run completely (auto-progresses through all tiers)
4. Show the final success dashboard
5. Optional: Open Instagram to show the live post

### Narration Script:
```
"This is my AI Employee system demonstrating Bronze, Silver, and Gold tiers.

Bronze Tier validates the core infrastructure - you can see all checks passing.

Silver Tier connects to live APIs - Instagram, Facebook, and Odoo are all connected.

Gold Tier is the autonomous agent in action - watch as it creates a real Instagram
post without any manual intervention. There's the Post ID - this is live on Instagram
right now.

All three tiers complete - this is a fully autonomous AI employee managing social
media, business operations, and customer interactions 24/7."
```

---

## 📋 REQUIREMENTS

### Essential:
- Python 3.8+
- `requests` library
- `python-dotenv` library
- `.env` file with credentials

### Optional (for full demo):
- Instagram API credentials (for live posting)
- Facebook API credentials (for API test)
- Odoo running (docker-compose up -d)

**Note:** Demo will run in simulation mode if credentials are missing, but live posting requires valid Instagram tokens.

---

## 🔧 TROUBLESHOOTING

### "Instagram credentials not configured"
- Check `.env` file has `INSTAGRAM_ACCESS_TOKEN` and `INSTAGRAM_ACCOUNT_ID`
- Ensure tokens have `instagram_content_publish` permission

### "Module not found"
```bash
pip install requests python-dotenv
```

### "Odoo not running"
- This is optional for the demo
- To start Odoo: `docker-compose up -d`

### Demo runs too fast
- Edit `demo-master.py` and increase `time.sleep()` values

---

## 📁 FILES INCLUDED

```
My-AI-Employee -FTEs/
├── demo-master.py          # Main demo orchestrator
├── run-demo.bat            # Windows launcher
├── run-demo.sh             # Linux/Mac launcher
├── DEMO_GUIDE.md           # This file
└── .env                    # Your credentials (not in git)
```

---

## 🎯 DEMO FEATURES

### Visual Dashboard
- Real-time tier status updates
- Color-coded success/failure indicators
- Timestamp for each action
- Clean, professional terminal output

### Autonomous Actions
- Live Instagram posting
- API connection verification
- Infrastructure validation
- Success metrics display

### Recording-Friendly
- Auto-progression (no manual input needed)
- Clear visual feedback
- Professional formatting
- Submission URL displayed at end

---

## 📤 AFTER RECORDING

1. Upload video to YouTube/Loom/Drive
2. Submit at: **Forms.gle/JR9T1SJq5rmQyGkGA**
3. Include:
   - Video link
   - GitHub repository link
   - Brief description of your implementation

---

## 💡 TIPS FOR BEST RESULTS

1. **Run in fullscreen terminal** - easier to see in video
2. **Use dark theme** - looks more professional
3. **Increase font size** - better visibility in recording
4. **Test before recording** - ensure all APIs work
5. **Keep it under 3 minutes** - as per submission requirements

---

## 🏆 SUCCESS CRITERIA

Your demo should show:
- ✅ All Bronze Tier checks passing
- ✅ API connections successful (Silver Tier)
- ✅ Live autonomous action (Gold Tier)
- ✅ Real Instagram post created (or simulated)
- ✅ Final success dashboard displayed

---

**Good luck with your submission!** 🚀

*For issues or questions, check the main README.md or repository documentation.*
