@echo off
echo ============================================================
echo FACEBOOK INTEGRATION - QUICK FIX GUIDE
echo ============================================================
echo.
echo Your access token has EXPIRED. Follow these steps:
echo.
echo STEP 1: Get New Access Token
echo -----------------------------------------------------------
echo 1. Open: https://developers.facebook.com/tools/explorer/
echo 2. Select your app
echo 3. Click "Generate Access Token"
echo 4. Select permissions:
echo    - pages_show_list
echo    - pages_read_engagement
echo    - pages_manage_posts (REQUIRED!)
echo    - pages_manage_engagement
echo    - instagram_basic
echo    - instagram_manage_messages
echo 5. Copy the token
echo.
echo STEP 2: Make Token Long-Lived (60 days)
echo -----------------------------------------------------------
echo 1. Open: https://developers.facebook.com/tools/debug/accesstoken/
echo 2. Paste your token
echo 3. Click "Extend Access Token"
echo 4. Copy the NEW token
echo.
echo STEP 3: Get Your Page ID
echo -----------------------------------------------------------
echo 1. Go to your Facebook Page
echo 2. Click "About"
echo 3. Find "Page ID" at bottom
echo 4. Copy the number
echo.
echo STEP 4: Update .env File
echo -----------------------------------------------------------
echo Edit: .env
echo.
echo Replace line 29:
echo INSTAGRAM_ACCESS_TOKEN=YOUR_NEW_TOKEN_HERE
echo.
echo Replace line 38:
echo FACEBOOK_PAGE_ID=YOUR_PAGE_ID_HERE
echo.
echo STEP 5: Verify Setup
echo -----------------------------------------------------------
echo Run: python verify-facebook-setup.py
echo.
echo ============================================================
echo Press any key to open Graph API Explorer...
pause >nul
start https://developers.facebook.com/tools/explorer/
