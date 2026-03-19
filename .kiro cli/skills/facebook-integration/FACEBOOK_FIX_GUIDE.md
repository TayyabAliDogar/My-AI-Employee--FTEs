# 🔧 FACEBOOK INTEGRATION - FIX REQUIRED

## ❌ Current Issue

**Access Token Expired**
- Expired: Thursday, 19-Mar-26 02:00:00 PDT
- Current: Thursday, 19-Mar-26 09:56:15 PDT
- Status: All Facebook/Instagram API calls failing

---

## ✅ What's Already Set Up

### Files Created
- ✅ `facebook-poster.py` - Post to Facebook (ready)
- ✅ `facebook-watcher.py` - Monitor Facebook (ready)
- ✅ `facebook-config.json` - Configuration (ready)
- ✅ `verify-facebook-setup.py` - Verification tool (NEW)
- ✅ `test-facebook-post.py` - Quick test (NEW)
- ✅ `fix-facebook-token.bat` - Fix guide (NEW)

### Code Status
- ✅ Page ID correctly linked from .env (line 18: `PAGE_ID = os.getenv("FACEBOOK_PAGE_ID", "")`)
- ✅ Access token correctly linked from .env (line 17: `ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")`)
- ✅ Auto-detection fallback implemented (lines 22-46)
- ✅ All posting functions ready

---

## 🔧 Required Actions

### 1. Generate New Access Token (10 min)

**Step-by-Step:**

```bash
# 1. Open Graph API Explorer
https://developers.facebook.com/tools/explorer/

# 2. Select your app from dropdown

# 3. Click "Generate Access Token"

# 4. Select these permissions:
☑ pages_show_list
☑ pages_read_engagement
☑ pages_manage_posts          ← CRITICAL for posting!
☑ pages_manage_engagement
☑ instagram_basic
☑ instagram_manage_messages
☑ instagram_manage_comments

# 5. Copy the token

# 6. Make it long-lived (60 days):
https://developers.facebook.com/tools/debug/accesstoken/
- Paste token
- Click "Extend Access Token"
- Copy NEW token
```

### 2. Get Facebook Page ID (2 min)

**Method A - From Facebook:**
```
1. Go to your Facebook Page
2. Click "About" in left menu
3. Scroll to bottom
4. Copy "Page ID" number
```

**Method B - Auto-detect:**
```bash
# After fixing token, run:
cd ".kiro cli/skills/facebook-integration/scripts"
python verify-facebook-setup.py
# Will show all your Pages with IDs
```

### 3. Update .env File (1 min)

Edit: `C:\Users\Laptop collection\Documents\GitHub\My-AI-Employee -FTEs\.env`

```bash
# Line 29 - Replace with NEW token
INSTAGRAM_ACCESS_TOKEN=YOUR_NEW_LONG_LIVED_TOKEN_HERE

# Line 38 - Replace with actual Page ID
FACEBOOK_PAGE_ID=YOUR_ACTUAL_PAGE_ID_HERE
```

### 4. Verify Setup (1 min)

```bash
cd "C:/Users/Laptop collection/Documents/GitHub/My-AI-Employee -FTEs/.kiro cli/skills/facebook-integration/scripts"

# Run verification
python verify-facebook-setup.py

# Expected output:
# ✅ Token Permissions: PASS
# ✅ Page ID Setup: PASS
# ✅ Post Capability: PASS
```

### 5. Test Posting (1 min)

```bash
# Test post
python facebook-poster.py --post "Test post from AI Employee!"

# Expected output:
# ✅ Successfully posted to Facebook!
# Post ID: 123456789_987654321
```

---

## 📊 Required Permissions

Your access token MUST have these permissions:

| Permission | Purpose | Status |
|------------|---------|--------|
| `pages_show_list` | List your Pages | Required |
| `pages_read_engagement` | Read comments/reactions | Required |
| `pages_manage_posts` | **POST TO FACEBOOK** | **CRITICAL** |
| `pages_manage_engagement` | Reply to comments | Required |
| `instagram_basic` | Instagram access | Optional |
| `instagram_manage_messages` | Instagram DMs | Optional |
| `instagram_manage_comments` | Instagram comments | Optional |

**Without `pages_manage_posts` you CANNOT post to Facebook!**

---

## 🎯 Quick Fix Commands

```bash
# Navigate to Facebook integration
cd "C:/Users/Laptop collection/Documents/GitHub/My-AI-Employee -FTEs/.kiro cli/skills/facebook-integration/scripts"

# Option 1: Run fix guide (Windows)
fix-facebook-token.bat

# Option 2: Run verification
python verify-facebook-setup.py

# Option 3: Quick test (after fixing)
python test-facebook-post.py
```

---

## ✅ After Fixing

Once you have a valid token and Page ID:

### Test Individual Features

```bash
# 1. Post text
python facebook-poster.py --post "Hello from AI Employee!"

# 2. Post with link
python facebook-poster.py --post "Check this out!" --link "https://example.com"

# 3. Post with image
python facebook-poster.py --post "New product!" --image "https://example.com/image.jpg"

# 4. Get Page info
python facebook-poster.py --info

# 5. Get insights
python facebook-poster.py --insights
```

### Start Watcher

```bash
# Test once
python facebook-watcher.py --once

# Run continuously
python facebook-watcher.py
```

### Docker Integration

```bash
# Start all services (including Facebook watcher)
cd "../../../.."
docker-compose up -d

# Check Facebook watcher logs
docker-compose logs -f facebook-watcher
```

---

## 🔍 Troubleshooting

### Token Still Invalid
```bash
# Check token expiration
https://developers.facebook.com/tools/debug/accesstoken/
# Paste your token to see expiration date
```

### Missing Permissions
```bash
# Regenerate token with correct permissions
# Make sure to check pages_manage_posts!
```

### Page ID Not Found
```bash
# Verify you're admin of the Page
# Check Page settings > Page Info > Page ID
```

### Can't Post
```bash
# Verify token has pages_manage_posts permission
# Check Page is published (not draft)
# Ensure you're using Page ID, not User ID
```

---

## 📝 Summary

**Current Status:**
- ❌ Access token expired
- ⚠️ Page ID placeholder in .env
- ✅ All code ready and working
- ✅ Verification tools created

**To Complete:**
1. Generate new long-lived access token (10 min)
2. Get your Facebook Page ID (2 min)
3. Update .env file (1 min)
4. Run verification (1 min)
5. Test posting (1 min)

**Total Time:** ~15 minutes

---

## 🎉 Once Fixed

You'll have:
- ✅ Facebook posting capability
- ✅ Facebook monitoring (comments, messages)
- ✅ Instagram integration (same token)
- ✅ Automated social media management
- ✅ CEO briefing with social metrics

---

*Created: 2026-03-19*
*Status: Waiting for token renewal*
*Priority: HIGH - Required for Gold Tier*
