// Approve and Send - Sends approved email drafts via Gmail MCP Server
// Usage: node approve-and-send.js "DRAFT_filename.md"

const fs = require('fs');
const path = require('path');
const http = require('http');

// Configuration
const CONFIG = {
    pendingApprovalPath: path.join(__dirname, '../../../Vault/Pending_Approval'),
    donePath: path.join(__dirname, '../../../Vault/Done'),
    logsPath: path.join(__dirname, '../../../Vault/Logs'),

    // Gmail MCP Server settings
    mcpServer: {
        host: 'localhost',
        port: 8809,
        endpoint: '/send_email'
    }
};

class EmailSender {
    constructor(draftFile) {
        this.draftFile = draftFile;
        this.draftPath = path.join(CONFIG.pendingApprovalPath, draftFile);
        this.draftData = this.parseDraft();
    }

    parseDraft() {
        if (!fs.existsSync(this.draftPath)) {
            throw new Error(`Draft file not found: ${this.draftFile}`);
        }

        const content = fs.readFileSync(this.draftPath, 'utf8');
        const lines = content.split('\n');

        const data = {
            to: '',
            subject: '',
            body: '',
            originalEmail: '',
            status: ''
        };

        let inBody = false;
        let bodyLines = [];

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];

            if (line.startsWith('**Status:**')) {
                data.status = line.replace('**Status:**', '').trim();
            } else if (line.startsWith('**Original Email:**')) {
                data.originalEmail = line.replace('**Original Email:**', '').trim();
            } else if (line.startsWith('**To:**')) {
                data.to = line.replace('**To:**', '').trim();
            } else if (line.startsWith('**Subject:**')) {
                data.subject = line.replace('**Subject:**', '').trim();
            } else if (line.startsWith('**Body:**')) {
                inBody = true;
                continue;
            } else if (line.startsWith('---') && inBody) {
                inBody = false;
                break;
            } else if (inBody) {
                bodyLines.push(line);
            }
        }

        data.body = bodyLines.join('\n').trim();

        return data;
    }

    async sendViaGmailMCP() {
        console.log('\n[Sending via Gmail MCP Server]');
        console.log(`To: ${this.draftData.to}`);
        console.log(`Subject: ${this.draftData.subject}`);

        const payload = {
            tool: 'send_email',
            params: {
                to: this.draftData.to,
                subject: this.draftData.subject,
                body: this.draftData.body,
                html: false
            }
        };

        return new Promise((resolve, reject) => {
            const postData = JSON.stringify(payload);

            const options = {
                hostname: CONFIG.mcpServer.host,
                port: CONFIG.mcpServer.port,
                path: CONFIG.mcpServer.endpoint,
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Content-Length': Buffer.byteLength(postData)
                }
            };

            const req = http.request(options, (res) => {
                let data = '';

                res.on('data', (chunk) => {
                    data += chunk;
                });

                res.on('end', () => {
                    if (res.statusCode === 200) {
                        try {
                            const response = JSON.parse(data);
                            resolve(response);
                        } catch (e) {
                            resolve({ status: 'sent', message_id: 'unknown' });
                        }
                    } else {
                        reject(new Error(`MCP Server returned status ${res.statusCode}: ${data}`));
                    }
                });
            });

            req.on('error', (error) => {
                reject(new Error(`Failed to connect to MCP server: ${error.message}`));
            });

            req.write(postData);
            req.end();
        });
    }

    async sendViaGmailAPI() {
        console.log('\n[Sending via Gmail API directly]');
        console.log('Note: This requires gmail-sender-token.json');

        // Fallback: Use Gmail API directly if MCP server is not available
        // This would require the Gmail API client library
        throw new Error('Direct Gmail API sending not implemented. Please start the MCP server.');
    }

    updateDraftStatus(status, messageId = null) {
        const content = fs.readFileSync(this.draftPath, 'utf8');

        let updatedContent = content.replace(
            /\*\*Status:\*\* 🟡 PENDING APPROVAL/,
            `**Status:** ${status === 'sent' ? '✅ SENT' : '❌ FAILED'}`
        );

        if (messageId) {
            updatedContent += `\n\n## Send Details\n\n**Message ID:** ${messageId}\n**Sent At:** ${new Date().toISOString()}\n`;
        }

        fs.writeFileSync(this.draftPath, updatedContent);
    }

    moveToDone(status) {
        const prefix = status === 'sent' ? 'SENT' : 'FAILED';
        const destFile = `${prefix}_${this.draftFile}`;
        const destPath = path.join(CONFIG.donePath, destFile);

        fs.renameSync(this.draftPath, destPath);
        console.log(`✓ Moved to Done: ${destFile}`);
    }

    logSend(status, messageId = null, error = null) {
        const timestamp = new Date().toISOString();
        const logEntry = {
            timestamp,
            draft_file: this.draftFile,
            to: this.draftData.to,
            subject: this.draftData.subject,
            status,
            message_id: messageId,
            error: error ? error.message : null
        };

        const logFile = path.join(CONFIG.logsPath, 'email-sends.log');
        const logLine = `${timestamp} | ${status.toUpperCase()} | to:${this.draftData.to} | subject:${this.draftData.subject} | msg_id:${messageId || 'N/A'}\n`;

        fs.appendFileSync(logFile, logLine);

        // Also save detailed JSON log
        const jsonLogFile = path.join(CONFIG.logsPath, 'email-sends.json');
        let logs = [];
        if (fs.existsSync(jsonLogFile)) {
            logs = JSON.parse(fs.readFileSync(jsonLogFile, 'utf8'));
        }
        logs.push(logEntry);
        fs.writeFileSync(jsonLogFile, JSON.stringify(logs, null, 2));
    }

    async send() {
        console.log('═══════════════════════════════════════════════════════');
        console.log('  Approve and Send - Email Sender');
        console.log('═══════════════════════════════════════════════════════');
        console.log(`Draft: ${this.draftFile}\n`);

        // Verify draft is pending
        if (!this.draftData.status.includes('PENDING')) {
            console.log('⚠️  Warning: Draft status is not PENDING');
            console.log(`Current status: ${this.draftData.status}`);

            const readline = require('readline').createInterface({
                input: process.stdin,
                output: process.stdout
            });

            return new Promise((resolve) => {
                readline.question('Continue anyway? (yes/no): ', (answer) => {
                    readline.close();
                    if (answer.toLowerCase() !== 'yes') {
                        console.log('✗ Send cancelled');
                        resolve(false);
                        return;
                    }
                    this.proceedWithSend().then(resolve);
                });
            });
        }

        return this.proceedWithSend();
    }

    async proceedWithSend() {
        console.log('Draft Details:');
        console.log(`  To: ${this.draftData.to}`);
        console.log(`  Subject: ${this.draftData.subject}`);
        console.log(`  Body length: ${this.draftData.body.length} characters\n`);

        try {
            // Try MCP server first
            console.log('Attempting to send via Gmail MCP Server...');
            const response = await this.sendViaGmailMCP();

            console.log('\n✓ Email sent successfully!');
            console.log(`Message ID: ${response.message_id || 'N/A'}`);

            // Update draft status
            this.updateDraftStatus('sent', response.message_id);

            // Log the send
            this.logSend('sent', response.message_id);

            // Move to Done folder
            this.moveToDone('sent');

            console.log('\n═══════════════════════════════════════════════════════');
            console.log('  SUCCESS: Email Sent');
            console.log('═══════════════════════════════════════════════════════');

            return true;

        } catch (error) {
            console.error('\n✗ Failed to send email');
            console.error(`Error: ${error.message}`);

            if (error.message.includes('connect to MCP server')) {
                console.log('\n⚠️  Gmail MCP Server is not running');
                console.log('\nTo start the server:');
                console.log('  cd .kiro\\ cli/skills/email-sender/scripts');
                console.log('  bash start-email-server.sh');
                console.log('\nOr use the email-sender skill to configure and start it.');
            }

            // Update draft status
            this.updateDraftStatus('failed');

            // Log the failure
            this.logSend('failed', null, error);

            // Keep in Pending_Approval for retry
            console.log('\n✗ Draft remains in Pending_Approval for retry');

            return false;
        }
    }
}

// Main execution
async function main() {
    const args = process.argv.slice(2);

    if (args.length === 0) {
        console.log('Usage: node approve-and-send.js "DRAFT_filename.md"');
        console.log('\nExample:');
        console.log('  node approve-and-send.js "DRAFT_Client_Request_2026-03-17.md"');
        process.exit(1);
    }

    const draftFile = args[0];

    try {
        const sender = new EmailSender(draftFile);
        const success = await sender.send();
        process.exit(success ? 0 : 1);
    } catch (error) {
        console.error('Error:', error.message);
        process.exit(1);
    }
}

if (require.main === module) {
    main();
}

module.exports = { EmailSender };
