// Orchestrator - Email Analysis & Draft Response Generator
// Analyzes emails in Vault/Needs_Action and creates draft responses

const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
    needsActionPath: path.join(__dirname, '../../../Vault/Needs_Action'),
    pendingApprovalPath: path.join(__dirname, '../../../Vault/Pending_Approval'),
    donePath: path.join(__dirname, '../../../Vault/Done'),
    logsPath: path.join(__dirname, '../../../Vault/Logs'),

    // Email categories that require responses
    responseCategories: ['client', 'urgent', 'invoice'],

    // Senders to ignore (automated notifications)
    ignoreSenders: [
        'noreply@',
        'no-reply@',
        'alert@indeed.com',
        'notifications@',
        'newsletter@',
        'donotreply@'
    ],

    // Amazon PPC expertise profile
    expertise: {
        name: 'Amazon PPC Expert',
        specialties: [
            'Amazon PPC campaign optimization',
            'ACOS and TACOS analysis',
            'Bid management strategies',
            'Keyword research and targeting',
            'Product launch campaigns',
            'Attribution modeling',
            'Ad spend optimization'
        ],
        experience: '$2M+ in managed ad spend',
        tone: 'professional, confident, data-driven'
    }
};

// Email analysis engine
class EmailAnalyzer {
    constructor(emailFile) {
        this.emailFile = emailFile;
        this.emailPath = path.join(CONFIG.needsActionPath, emailFile);
        this.emailData = this.parseEmail();
    }

    parseEmail() {
        const content = fs.readFileSync(this.emailPath, 'utf8');
        const lines = content.split('\n');

        const data = {
            subject: '',
            from: '',
            date: '',
            category: '',
            priority: '',
            body: '',
            metadata: {}
        };

        // Parse email metadata
        for (const line of lines) {
            if (line.startsWith('# EMAIL:')) {
                data.subject = line.replace('# EMAIL:', '').trim();
            } else if (line.startsWith('**From:**')) {
                data.from = line.replace('**From:**', '').trim();
            } else if (line.startsWith('**Date:**')) {
                data.date = line.replace('**Date:**', '').trim();
            } else if (line.startsWith('**Category:**')) {
                data.category = line.replace('**Category:**', '').trim();
            } else if (line.startsWith('**Priority:**')) {
                data.priority = line.replace('**Priority:**', '').trim();
            } else if (line.startsWith('## Email Content')) {
                // Capture body content after this marker
                const bodyStart = lines.indexOf(line) + 1;
                const bodyEnd = lines.findIndex((l, i) => i > bodyStart && l.startsWith('## '));
                data.body = lines.slice(bodyStart, bodyEnd > 0 ? bodyEnd : undefined).join('\n').trim();
            }
        }

        return data;
    }

    shouldRespond() {
        // Check if sender is in ignore list
        for (const ignoreSender of CONFIG.ignoreSenders) {
            if (this.emailData.from.toLowerCase().includes(ignoreSender)) {
                return {
                    respond: false,
                    reason: 'Automated notification - no response needed'
                };
            }
        }

        // Check if category requires response
        if (!CONFIG.responseCategories.includes(this.emailData.category)) {
            return {
                respond: false,
                reason: `Category '${this.emailData.category}' does not require response`
            };
        }

        // Check for client inquiry keywords
        const clientKeywords = [
            'proposal', 'quote', 'consultation', 'help with', 'looking for',
            'ppc', 'advertising', 'campaign', 'acos', 'tacos', 'amazon',
            'interested in', 'can you', 'would you', 'need assistance'
        ];

        const bodyLower = this.emailData.body.toLowerCase();
        const hasClientKeyword = clientKeywords.some(kw => bodyLower.includes(kw));

        if (hasClientKeyword) {
            return {
                respond: true,
                reason: 'Client inquiry detected',
                type: 'client_inquiry'
            };
        }

        // High priority emails should be reviewed
        if (this.emailData.priority === 'HIGH') {
            return {
                respond: true,
                reason: 'High priority email',
                type: 'high_priority'
            };
        }

        return {
            respond: false,
            reason: 'No response criteria met'
        };
    }

    generateDraft() {
        const analysis = this.shouldRespond();

        if (!analysis.respond) {
            return null;
        }

        // Determine response type and generate appropriate draft
        let draft = '';

        if (analysis.type === 'client_inquiry') {
            draft = this.generateClientInquiryResponse();
        } else if (analysis.type === 'high_priority') {
            draft = this.generateHighPriorityResponse();
        } else {
            draft = this.generateGenericResponse();
        }

        return {
            to: this.extractEmailAddress(this.emailData.from),
            subject: `Re: ${this.emailData.subject}`,
            body: draft,
            analysis: analysis,
            originalEmail: this.emailFile
        };
    }

    generateClientInquiryResponse() {
        // Amazon PPC expert response template
        return `Hi there,

Thank you for reaching out regarding your Amazon PPC needs.

With over $2M+ in managed ad spend, I specialize in helping Amazon sellers optimize their advertising campaigns and scale profitably. Based on your inquiry, here's how I can help:

**My Expertise:**
• ACOS & TACOS optimization strategies
• Advanced bid management and automation
• Keyword research and negative keyword sculpting
• Product launch campaigns with aggressive scaling
• Attribution modeling and customer journey analysis
• Campaign structure optimization

**Next Steps:**

I'd be happy to schedule a brief consultation call to discuss your specific challenges and goals. During this call, we can:

1. Review your current campaign performance
2. Identify immediate optimization opportunities
3. Discuss a customized strategy for your business

Please let me know your availability for a 30-minute call this week, and I'll send over a calendar invite.

Looking forward to helping you scale your Amazon business profitably.

Best regards,
Amazon PPC Expert

---
📊 Specializing in ACOS/TACOS optimization
💰 $2M+ in managed ad spend
🚀 Data-driven strategies for profitable growth`;
    }

    generateHighPriorityResponse() {
        return `Hi,

Thank you for your email. I've received your message and will review it carefully.

I'll get back to you within 24 hours with a detailed response.

Best regards,
Amazon PPC Expert`;
    }

    generateGenericResponse() {
        return `Hi,

Thank you for reaching out. I've received your message and will respond shortly.

Best regards,
Amazon PPC Expert`;
    }

    extractEmailAddress(fromField) {
        // Extract email from "Name <email@domain.com>" format
        const match = fromField.match(/<(.+?)>/);
        if (match) {
            return match[1];
        }
        return fromField;
    }
}

// Draft manager
class DraftManager {
    static saveDraft(draft, emailFile) {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
        const draftFileName = `DRAFT_${emailFile.replace('EMAIL_', '').replace('.md', '')}_${timestamp}.md`;
        const draftPath = path.join(CONFIG.pendingApprovalPath, draftFileName);

        const draftContent = `# EMAIL DRAFT - PENDING APPROVAL

**Status:** 🟡 PENDING APPROVAL
**Created:** ${new Date().toISOString()}
**Original Email:** ${emailFile}

---

## Draft Email

**To:** ${draft.to}
**Subject:** ${draft.subject}

**Body:**

${draft.body}

---

## Analysis

**Response Type:** ${draft.analysis.type || 'N/A'}
**Reason:** ${draft.analysis.reason}
**Requires Approval:** Yes (external communication)

---

## Approval Instructions

To approve and send this email:

\`\`\`bash
# Option 1: Use approval script
node .kiro\\ cli/skills/orchestrator/approve-and-send.js "${draftFileName}"

# Option 2: Tell Claude
"Approve and send ${draftFileName}"
\`\`\`

To reject:

\`\`\`bash
# Move to Done folder with REJECTED prefix
mv "Vault/Pending_Approval/${draftFileName}" "Vault/Done/REJECTED_${draftFileName}"
\`\`\`

---

*Generated by Orchestrator - AI Employee Silver Tier*
*Amazon PPC Expert Profile*
`;

        fs.writeFileSync(draftPath, draftContent);
        console.log(`✓ Draft saved: ${draftFileName}`);

        return draftFileName;
    }

    static moveToProcessed(emailFile) {
        const sourcePath = path.join(CONFIG.needsActionPath, emailFile);
        const destPath = path.join(CONFIG.donePath, `PROCESSED_${emailFile}`);

        fs.renameSync(sourcePath, destPath);
        console.log(`✓ Moved to Done: ${emailFile}`);
    }
}

// Orchestrator main class
class Orchestrator {
    constructor() {
        this.emailsProcessed = 0;
        this.draftsCreated = 0;
        this.emailsSkipped = 0;
    }

    run() {
        console.log('═══════════════════════════════════════════════════════');
        console.log('  Email Orchestrator - Silver Tier');
        console.log('═══════════════════════════════════════════════════════');
        console.log(`Analyzing emails in: ${CONFIG.needsActionPath}`);
        console.log(`Draft output: ${CONFIG.pendingApprovalPath}\n`);

        // Get all email files
        const files = fs.readdirSync(CONFIG.needsActionPath)
            .filter(f => f.startsWith('EMAIL_') && f.endsWith('.md'))
            .sort()
            .reverse(); // Most recent first

        if (files.length === 0) {
            console.log('⊘ No emails found in Needs_Action folder');
            return;
        }

        console.log(`Found ${files.length} email(s) to analyze\n`);

        // Process each email
        for (const file of files) {
            this.processEmail(file);
        }

        // Summary
        console.log('\n═══════════════════════════════════════════════════════');
        console.log('  Orchestration Complete');
        console.log('═══════════════════════════════════════════════════════');
        console.log(`Emails processed: ${this.emailsProcessed}`);
        console.log(`Drafts created: ${this.draftsCreated}`);
        console.log(`Emails skipped: ${this.emailsSkipped}`);
        console.log('\nNext steps:');
        console.log('1. Review drafts in Vault/Pending_Approval/');
        console.log('2. Approve drafts with: "Approve and send [filename]"');
        console.log('3. Approved emails will be sent via Gmail MCP server');
    }

    processEmail(emailFile) {
        console.log(`\n[Processing] ${emailFile}`);

        try {
            const analyzer = new EmailAnalyzer(emailFile);
            const analysis = analyzer.shouldRespond();

            console.log(`  Category: ${analyzer.emailData.category}`);
            console.log(`  Priority: ${analyzer.emailData.priority}`);
            console.log(`  From: ${analyzer.emailData.from}`);

            if (!analysis.respond) {
                console.log(`  ⊘ Skipped: ${analysis.reason}`);
                this.emailsSkipped++;
                this.emailsProcessed++;
                return;
            }

            console.log(`  ✓ Response needed: ${analysis.reason}`);

            // Generate draft
            const draft = analyzer.generateDraft();

            if (draft) {
                const draftFile = DraftManager.saveDraft(draft, emailFile);
                console.log(`  ✓ Draft created: ${draftFile}`);
                this.draftsCreated++;
            }

            this.emailsProcessed++;

        } catch (error) {
            console.error(`  ✗ Error processing ${emailFile}:`, error.message);
        }
    }
}

// Run orchestrator
if (require.main === module) {
    const orchestrator = new Orchestrator();
    orchestrator.run();
}

module.exports = { Orchestrator, EmailAnalyzer, DraftManager };
