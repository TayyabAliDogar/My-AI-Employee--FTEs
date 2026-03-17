// Generate LinkedIn auth.json - Automatic Session Saver
// This script opens LinkedIn, waits for you to log in, then automatically saves the session

const { chromium } = require('playwright');
const fs = require('fs');

async function generateAuth() {
    console.log('========================================');
    console.log('LinkedIn Session Generator');
    console.log('========================================\n');

    let browser;
    try {
        console.log('Launching browser...');
        browser = await chromium.launch({
            headless: false,
            args: ['--disable-blink-features=AutomationControlled']
        });

        const context = await browser.newContext({
            userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        });

        const page = await context.newPage();

        console.log('✓ Browser launched\n');
        console.log('Navigating to LinkedIn login page...');
        await page.goto('https://www.linkedin.com/login', {
            waitUntil: 'domcontentloaded',
            timeout: 60000
        });
        console.log('✓ LinkedIn login page loaded\n');

        console.log('========================================');
        console.log('PLEASE LOG IN TO YOUR LINKEDIN ACCOUNT');
        console.log('========================================');
        console.log('1. Enter your email and password');
        console.log('2. Complete any security challenges (2FA, CAPTCHA, etc.)');
        console.log('3. Wait until you see your LinkedIn feed');
        console.log('4. The script will automatically detect and save your session\n');

        console.log('Waiting for you to log in...');
        console.log('(Checking every 3 seconds for up to 5 minutes)\n');

        // Poll for successful login (check every 3 seconds for up to 5 minutes)
        let loggedIn = false;
        let attempts = 0;
        const maxAttempts = 100; // 5 minutes (100 * 3 seconds)

        while (!loggedIn && attempts < maxAttempts) {
            attempts++;
            await page.waitForTimeout(3000);

            const currentUrl = page.url();
            console.log(`[Check ${attempts}] Current URL: ${currentUrl}`);

            // Check if we're on the feed or any authenticated LinkedIn page
            if (currentUrl.includes('/feed') ||
                (currentUrl.includes('linkedin.com') &&
                 !currentUrl.includes('/login') &&
                 !currentUrl.includes('/checkpoint'))) {

                console.log('\n✓ Login detected! You are now on LinkedIn.');
                loggedIn = true;
                break;
            }

            if (attempts % 10 === 0) {
                console.log(`Still waiting... (${attempts * 3} seconds elapsed)`);
            }
        }

        if (!loggedIn) {
            throw new Error('Timeout: Login not detected after 5 minutes. Please try again.');
        }

        console.log('\nWaiting 3 more seconds to ensure session is stable...');
        await page.waitForTimeout(3000);

        console.log('\nSaving session to auth.json...');
        const storageState = await context.storageState();
        fs.writeFileSync('auth.json', JSON.stringify(storageState, null, 2));
        console.log('✓ Session saved to auth.json\n');

        console.log('Taking verification screenshot...');
        await page.screenshot({ path: 'linkedin-session-saved.png' });
        console.log('✓ Screenshot saved as linkedin-session-saved.png\n');

        console.log('========================================');
        console.log('SUCCESS! Auth.json has been generated');
        console.log('========================================');
        console.log('You can now use linkedin-poster.js to post content.\n');

        console.log('Closing browser in 3 seconds...');
        await page.waitForTimeout(3000);

    } catch (error) {
        console.error('\n❌ Error:', error.message);
        process.exit(1);
    } finally {
        if (browser) {
            await browser.close();
            console.log('✓ Browser closed');
        }
    }
}

console.log('\nStarting LinkedIn session generator...\n');
generateAuth();
