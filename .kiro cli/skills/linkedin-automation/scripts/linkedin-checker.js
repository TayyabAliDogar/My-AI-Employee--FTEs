// LinkedIn Checker - Node.js with Playwright
// Checks LinkedIn messages and notifications using saved auth.json

const { chromium } = require('playwright');
const fs = require('fs');

async function checkLinkedIn() {
    const results = {
        messages: [],
        notifications: [],
        timestamp: new Date().toISOString()
    };

    let browser;
    try {
        // Check if auth.json exists
        if (!fs.existsSync('auth.json')) {
            console.error('ERROR: auth.json not found');
            process.exit(1);
        }

        // Launch browser with saved authentication
        browser = await chromium.launch({ headless: true });
        const context = await browser.newContext({ storageState: 'auth.json' });
        const page = await context.newPage();

        console.log('Checking LinkedIn messages...');

        // Check messages
        await page.goto('https://www.linkedin.com/messaging/', { waitUntil: 'networkidle' });
        await page.waitForTimeout(2000);

        // Look for unread messages
        const conversations = await page.$$('.msg-conversation-listitem');

        for (let i = 0; i < Math.min(conversations.length, 5); i++) {
            const conv = conversations[i];

            // Check if unread
            const unreadBadge = await conv.$('[data-test-icon="badge-small"]');

            if (unreadBadge) {
                // Get sender name
                const nameElem = await conv.$('.msg-conversation-listitem__participant-names');
                const sender = nameElem ? await nameElem.innerText() : 'Unknown';

                // Get message preview
                const previewElem = await conv.$('.msg-conversation-listitem__message-snippet');
                const preview = previewElem ? await previewElem.innerText() : 'No preview';

                results.messages.push({
                    id: `msg_${sender}_${Date.now()}`,
                    sender: sender.trim(),
                    preview: preview.trim(),
                    title: `New message from ${sender.trim()}`
                });
            }
        }

        console.log(`Found ${results.messages.length} new message(s)`);

        // Check notifications
        console.log('Checking LinkedIn notifications...');
        await page.goto('https://www.linkedin.com/notifications/', { waitUntil: 'networkidle' });
        await page.waitForTimeout(2000);

        const notifItems = await page.$$('.notification-card');

        for (let i = 0; i < Math.min(notifItems.length, 5); i++) {
            const item = notifItems[i];

            // Check if unread
            const className = await item.getAttribute('class');
            const isUnread = className && className.includes('notification-card--unread');

            if (isUnread) {
                const textElem = await item.$('.notification-card__text');
                const text = textElem ? await textElem.innerText() : 'No text';

                results.notifications.push({
                    id: `notif_${Date.now()}_${i}`,
                    title: 'New LinkedIn Notification',
                    content: text.trim()
                });
            }
        }

        console.log(`Found ${results.notifications.length} new notification(s)`);

        // Output results as JSON
        console.log('RESULTS_START');
        console.log(JSON.stringify(results, null, 2));
        console.log('RESULTS_END');

    } catch (error) {
        console.error('Error:', error.message);
        process.exit(1);
    } finally {
        if (browser) {
            await browser.close();
        }
    }
}

checkLinkedIn();
