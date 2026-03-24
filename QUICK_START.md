# 🎬 MASTER DEMO - QUICK START GUIDE

## 🚀 FOR YOUR 3-MINUTE VIDEO RECORDING

### STEP 1: Refresh Your Instagram Token (2 minutes)

Your token expired on March 19. Refresh it quickly:

```bash
python refresh-token.py
```

Or manually:
1. Go to: https://developers.facebook.com/tools/explorer/
2. Select app: "My personal AI employee"
3. Click "Generate Access Token"
4. Check permissions: `instagram_content_publish`, `instagram_basic`
5. Copy the new token
6. Update `.env` file:
   ```
   INSTAGRAM_ACCESS_TOKEN=<new_token>
   ```

### STEP 2: Run the Demo (3 minutes)

**Windows:**
```bash
run-demo.bat
```

**Or directly:**
```bash
python demo-master.py
```

### STEP 3: Record Your Video

**What You'll See:**
- ✅ Bronze Tier: 6 infrastructure checks (all pass in ~5 seconds)
- ✅ Silver Tier: API connections + watcher verification (~10 seconds)
- ✅ Gold Tier: **LIVE Instagram post creation** (~15 seconds)
- ✅ Final dashboard with all tiers complete

**Total Runtime:** ~30-40 seconds (perfect for 3-minute video with narration)

---

## 📹 RECORDING TIPS

### Before Recording:
1. ✅ Refresh Instagram token (see Step 1)
2. ✅ Maximize terminal window
3. ✅ Increase font size (Ctrl + Plus)
4. ✅ Use dark theme for professional look
5. ✅ Close other applications

### During Recording:
1. Start screen recording (OBS, Loom, etc.)
2. Run: `python demo-master.py`
3. Let it run completely (auto-progresses)
4. Show final success dashboard
5. Optional: Open Instagram to show the live post

### Narration Script (30 seconds):
```
"This is my AI Employee system demonstrating all three tiers.

Bronze Tier validates core infrastructure - all checks passing.

Silver Tier connects to live APIs - Instagram, Facebook, and Odoo connected.

Gold Tier is the autonomous agent - watch it create a real Instagram post
without any manual intervention. There's the Post ID - live on Instagram now.

All three tiers complete - fully autonomous AI employee running 24/7."
```

---

## 🎯 WHAT THE DEMO SHOWS

### Bronze Tier (5 seconds)
```
[OK] Python Environment: PASSED
[OK] Environment Variables: PASSED
[OK] Vault Directory: PASSED
[OK] Skills Directory: PASSED
[OK] Dependencies: PASSED
```

### Silver Tier (10 seconds)
```
[OK] Instagram API: Connected (@tayyabalidogar512)
[OK] Facebook API: Connected (My personal AI employee)
[OK] Odoo: Connected (http://localhost:8069)
[OK] Watcher Scripts: Verified
```

### Gold Tier (15 seconds)
```
[INFO] Initializing Gold Tier Autonomous Agent...
[AGENT] Agent Decision: Create Instagram post for demo
[INFO] Creating Instagram media container...
[OK] Container created: 18059808065466275
[INFO] Publishing to Instagram...
[SUCCESS] Posted to Instagram! Post ID: 18243669802306892
```

---

## ✅ SUCCESS CRITERIA

Your demo should show:
- ✅ All Bronze Tier checks passing
- ✅ API connections successful (Silver Tier)
- ✅ **Live Instagram post created** (Gold Tier)
- ✅ Post ID displayed
- ✅ Final success dashboard

---

## 🔧 TROUBLESHOOTING

### "Instagram API: Connection failed"
→ Token expired. Run `python refresh-token.py`

### "Odoo: Not running"
→ Optional. Start with: `docker-compose up -d`
→ Or ignore - demo still works without Odoo

### Demo runs too fast
→ Edit `demo-master.py` and increase `time.sleep()` values

---

## 📤 SUBMISSION

After recording:
1. Upload video to YouTube/Loom/Drive
2. Submit at: **Forms.gle/JR9T1SJq5rmQyGkGA**
3. Include:
   - Video link
   - GitHub repo: https://github.com/TayyabAliDogar/My-AI-Employee--FTEs
   - Brief description

---

## 🎬 READY TO RECORD?

```bash
# 1. Refresh token (if needed)
python refresh-token.py

# 2. Run demo
python demo-master.py

# 3. Record and submit!
```

**Good luck with your submission!** 🚀
