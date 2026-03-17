// LinkedIn Poster - Node.js with Playwright
// Posts content to LinkedIn using saved auth.json
// Enhanced with retry logic and extended timeouts

const { chromium } = require('playwright');
const fs = require('fs');

async function dismissPopups(page) {
    // Try to dismiss any pop-ups or modals that might appear
    try {
        const dismissButtons = [
            '[aria-label*="Dismiss"]',
            '[aria-label*="Close"]',
            'button[data-test-modal-close-btn]',
            '.artdeco-modal__dismiss'
        ];

        for (const selector of dismissButtons) {
            const button = page.locator(selector).first();
            if (await button.isVisible({ timeout: 2000 }).catch(() => false)) {
                await button.click();
                console.log(`Dismissed pop-up: ${selector}`);
                await page.waitForTimeout(1000);
            }
        }
    } catch (e) {
        // Ignore errors - pop-ups might not exist
    }
}

async function findAndClickStartPost(page, maxRetries = 3) {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        console.log(`\n[STEP] Attempt ${attempt}/${maxRetries}: Looking for "Start a post" button...`);

        // Dismiss any pop-ups first
        console.log('Checking for pop-ups to dismiss...');
        await dismissPopups(page);

        // Try multiple selectors for the "Start a post" area
        const methods = [
            {
                name: 'Share box',
                selector: '.share-box-feed-entry__trigger, [data-test-share-box-trigger]'
            },
            {
                name: 'Aria-label',
                selector: '[aria-label*="Start a post"]'
            },
            {
                name: 'Button text',
                selector: 'button',
                filter: { hasText: /start.*post/i }
            }
        ];

        for (const method of methods) {
            try {
                console.log(`Trying method: ${method.name} with selector: ${method.selector}`);
                let locator = page.locator(method.selector).first();
                if (method.filter) {
                    locator = page.locator(method.selector).filter(method.filter).first();
                }

                console.log('Waiting for element to be visible...');
                await locator.waitFor({ timeout: 60000, state: 'visible' });
                console.log('✓ Element is visible');

                console.log('Clicking button with force...');
                await locator.click({ force: true });
                console.log(`✓ Successfully clicked "Start a post" button (${method.name})`);
                return true;
            } catch (e) {
                console.log(`✗ Method ${method.name} failed: ${e.message}`);
            }
        }

        if (attempt < maxRetries) {
            console.log(`Retrying in 3 seconds...`);
            await page.waitForTimeout(3000);
        }
    }

    console.log('✗ Failed to find "Start a post" button after all attempts');
    return false;
}

async function findAndFillEditor(page, postText, maxRetries = 3) {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        console.log(`\n[STEP] Attempt ${attempt}/${maxRetries}: Looking for text editor...`);

        // Wait for the modal/dialog to fully load
        console.log('Waiting 3 seconds for modal to load...');
        await page.waitForTimeout(3000);
        console.log('✓ Wait completed');

        // Dismiss any pop-ups
        console.log('Checking for pop-ups to dismiss...');
        await dismissPopups(page);

        // Try multiple selectors for the text editor
        const editorSelectors = [
            '[role="textbox"]',
            '[contenteditable="true"]',
            '.ql-editor',
            '[data-placeholder*="share"]'
        ];

        for (const selector of editorSelectors) {
            try {
                console.log(`Trying selector: ${selector}`);
                const editor = page.locator(selector).first();

                // Wait for element to be visible and ready
                console.log('Waiting for element to be visible...');
                await editor.waitFor({ timeout: 60000, state: 'visible' });
                console.log('✓ Element is visible');

                await page.waitForTimeout(1000);

                // Verify it's actually editable
                console.log('Checking if element is editable...');
                const isEditable = await editor.isEditable({ timeout: 5000 }).catch(() => false);
                if (!isEditable) {
                    console.log(`✗ Element found but not editable: ${selector}`);
                    continue;
                }
                console.log('✓ Element is editable');

                // Click to focus with force
                console.log('Clicking editor to focus (with force)...');
                await editor.click({ force: true });
                console.log('✓ Editor focused');

                await page.waitForTimeout(1000);

                // Type the content
                console.log('Typing post content...');
                await editor.fill(postText);
                console.log('✓ Post content entered successfully');

                return true;
            } catch (e) {
                console.log(`✗ Selector ${selector} failed: ${e.message}`);
            }
        }

        if (attempt < maxRetries) {
            console.log(`Retrying in 3 seconds...`);
            await page.waitForTimeout(3000);
        }
    }

    console.log('✗ Failed to find or fill text editor after all attempts');
    return false;
}

async function findAndClickPostButton(page, maxRetries = 3) {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        console.log(`\n[STEP] Attempt ${attempt}/${maxRetries}: Looking for Post button...`);

        const methods = [
            {
                name: 'Button text "Post"',
                selector: 'button',
                filter: { hasText: /^Post$/i }
            },
            {
                name: 'Data attribute',
                selector: '[data-test-share-actions-post-button], .share-actions__primary-action'
            },
            {
                name: 'Submit button',
                selector: 'button[type="submit"]'
            }
        ];

        for (const method of methods) {
            try {
                console.log(`Trying method: ${method.name} with selector: ${method.selector}`);
                let locator = page.locator(method.selector).first();
                if (method.filter) {
                    locator = page.locator(method.selector).filter(method.filter).first();
                }

                console.log('Waiting for Post button to be visible...');
                await locator.waitFor({ timeout: 60000, state: 'visible' });
                console.log('✓ Post button is visible');

                console.log('Clicking Post button with force...');
                await locator.click({ force: true });
                console.log(`✓ Successfully clicked Post button (${method.name})`);
                return true;
            } catch (e) {
                console.log(`✗ Method ${method.name} failed: ${e.message}`);
            }
        }

        if (attempt < maxRetries) {
            console.log(`Retrying in 3 seconds...`);
            await page.waitForTimeout(3000);
        }
    }

    console.log('✗ Failed to find Post button after all attempts');
    return false;
}

async function postToLinkedIn(postText) {
    let browser;
    try {
        // Check if auth.json exists
        if (!fs.existsSync('auth.json')) {
            console.error('ERROR: auth.json not found');
            process.exit(1);
        }

        console.log('Launching browser with saved authentication...');
        browser = await chromium.launch({
            headless: false,
            args: ['--disable-blink-features=AutomationControlled']
        });
        const context = await browser.newContext({
            storageState: 'auth.json',
            userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        });
        const page = await context.newPage();

        // Add listeners to detect page issues
        page.on('close', () => console.log('⚠️ Page closed unexpectedly'));
        page.on('crash', () => console.log('⚠️ Page crashed'));
        context.on('close', () => console.log('⚠️ Context closed unexpectedly'));

        console.log('Navigating to LinkedIn feed...');
        await page.goto('https://www.linkedin.com/feed/', {
            waitUntil: 'domcontentloaded',
            timeout: 60000
        });
        console.log('✓ Page navigation completed');

        // Try to wait for network to be idle, but don't fail if it times out
        console.log('Waiting for network to be idle (optional)...');
        try {
            await page.waitForLoadState('networkidle', { timeout: 10000 });
            console.log('✓ Network is idle');
        } catch (e) {
            console.log('⚠️ Network still active (this is normal for LinkedIn) - continuing anyway');
        }

        // Hard 5-second sleep to allow LinkedIn's heavy scripts to finish
        console.log('Waiting 5 seconds for LinkedIn scripts to fully load...');
        await page.waitForTimeout(5000);
        console.log('✓ 5-second wait completed');

        // Check current URL to see if we got redirected
        const currentUrl = page.url();
        console.log(`Current URL: ${currentUrl}`);

        // Take screenshot to see what's on the page
        console.log('Taking screenshot of feed...');
        await page.screenshot({ path: 'linkedin-feed.png', fullPage: true });
        console.log('✓ Screenshot saved as linkedin-feed.png');

        // Check if we're actually logged in and on the feed
        if (currentUrl.includes('/login') || currentUrl.includes('/checkpoint')) {
            throw new Error('Session expired or security challenge detected. Please regenerate auth.json');
        }

        // Step 1: Click "Start a post" with retry logic
        console.log('\n[MAIN STEP 1] Attempting to click "Start a post" button...');
        const startPostClicked = await findAndClickStartPost(page);
        if (!startPostClicked) {
            throw new Error('Could not find "Start a post" button after 3 attempts. Check linkedin-feed.png screenshot.');
        }
        console.log('✓ [MAIN STEP 1] Successfully clicked "Start a post" button\n');

        // Step 2: Find and fill the text editor with retry logic
        console.log('[MAIN STEP 2] Attempting to find and fill text editor...');
        const editorFilled = await findAndFillEditor(page, postText);
        if (!editorFilled) {
            console.log('Taking error screenshot...');
            await page.screenshot({ path: 'linkedin-editor-error.png' });
            throw new Error('Could not find or fill text editor after 3 attempts. Check linkedin-editor-error.png screenshot.');
        }
        console.log('✓ [MAIN STEP 2] Successfully filled text editor\n');

        console.log('Waiting 2 seconds before taking preview screenshot...');
        await page.waitForTimeout(2000);

        // Take screenshot of the post before submitting
        console.log('Taking preview screenshot...');
        await page.screenshot({ path: 'linkedin-post-preview.png' });
        console.log('✓ Screenshot saved as linkedin-post-preview.png\n');

        // Step 3: Click the Post button with retry logic
        console.log('[MAIN STEP 3] Attempting to click Post button...');
        const posted = await findAndClickPostButton(page);
        if (!posted) {
            throw new Error('Could not find Post button after 3 attempts. Check linkedin-post-preview.png screenshot.');
        }
        console.log('✓ [MAIN STEP 3] Successfully clicked Post button\n');

        console.log('Waiting 5 seconds for post to publish...');
        await page.waitForTimeout(5000);

        console.log('\n========================================');
        console.log('SUCCESS: Post published to LinkedIn!');
        console.log('========================================');
        console.log(`Posted: "${postText.substring(0, 100)}..."`);

        // Take final screenshot
        console.log('\nTaking final success screenshot...');
        await page.screenshot({ path: 'linkedin-post-success.png' });
        console.log('✓ Final screenshot saved as linkedin-post-success.png');

        // Keep browser open for a few seconds to see the result
        console.log('\nKeeping browser open for 3 seconds...');
        await page.waitForTimeout(3000);
        console.log('✓ Done!');

    } catch (error) {
        console.error('Error:', error.message);
        if (browser) {
            await browser.close();
        }
        process.exit(1);
    } finally {
        if (browser) {
            await browser.close();
        }
    }
}

// Get post text from command line argument or use default
const postText = process.argv[2] || 'Testing my new AI Employee Silver Tier automation! 🚀 #AI #Automation';

console.log('LinkedIn Auto-Poster');
console.log('===================');
console.log(`Post text: "${postText}"`);
console.log('');

postToLinkedIn(postText);
