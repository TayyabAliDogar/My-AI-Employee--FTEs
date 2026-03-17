// Create Test Emails - Generates sample client inquiry emails for testing orchestrator

const fs = require('fs');
const path = require('path');

const needsActionPath = path.join(__dirname, '../../../Vault/Needs_Action');

const testEmails = [
    {
        filename: 'EMAIL_Client_PPC_Consultation_Request_2026-03-17_TEST.md',
        content: `# EMAIL: Amazon PPC Consultation Request

**From:** Sarah Johnson <sarah.johnson@ecommercestore.com>
**Date:** Mon, 17 Mar 2026 09:15:00 +0000
**Category:** client
**Priority:** HIGH

## Email Content

Hi,

I came across your LinkedIn profile and was impressed by your Amazon PPC expertise. I'm currently running an Amazon store selling kitchen appliances, and I'm struggling with my advertising costs.

My ACOS is sitting at 45%, and I'm spending about $5,000/month on ads but not seeing the returns I expected. I've tried adjusting bids manually, but it feels like I'm just guessing.

I'd love to schedule a consultation to discuss:
- How to bring my ACOS down to a profitable level
- Whether my campaign structure is optimized
- If I should be using Sponsored Brands or just Sponsored Products

Are you available for a call this week? I'm flexible with timing.

Looking forward to hearing from you.

Best regards,
Sarah Johnson
Founder, Kitchen Essentials Co.
sarah.johnson@ecommercestore.com

## Suggested Actions

- [ ] Review email content
- [ ] Draft response
- [ ] Take appropriate action based on category

## Metadata

- Email ID: test001
- Labels: UNREAD, INBOX
- Thread ID: test001
- Processed: 2026-03-17 10:00:00

---

*Test email for Orchestrator*
*Silver Tier - AI Employee*
`
    },
    {
        filename: 'EMAIL_Urgent_Campaign_Help_Needed_2026-03-17_TEST.md',
        content: `# EMAIL: URGENT: Campaign Performance Dropped 60%

**From:** Mike Chen <mike@brandboost.com>
**Date:** Mon, 17 Mar 2026 08:30:00 +0000
**Category:** urgent
**Priority:** HIGH

## Email Content

Hi there,

I need urgent help. My main product campaign performance has dropped 60% in the last week, and I can't figure out why.

Details:
- Product: Wireless Earbuds
- Previous ACOS: 22%
- Current ACOS: 58%
- Daily spend: $800
- Sales dropped from 40 units/day to 15 units/day

I've checked and nothing changed on my end - same bids, same keywords, same product listing. But suddenly my ads are barely converting.

Can you take a look ASAP? I'm losing money every day this continues.

Please let me know if you can help and what your rates are for emergency optimization.

Thanks,
Mike Chen
Brand Boost LLC
mike@brandboost.com
(555) 123-4567

## Suggested Actions

- [ ] Review email content
- [ ] Draft response
- [ ] Take appropriate action based on category

## Metadata

- Email ID: test002
- Labels: UNREAD, IMPORTANT, INBOX
- Thread ID: test002
- Processed: 2026-03-17 10:00:00

---

*Test email for Orchestrator*
*Silver Tier - AI Employee*
`
    },
    {
        filename: 'EMAIL_Product_Launch_Strategy_Inquiry_2026-03-17_TEST.md',
        content: `# EMAIL: Product Launch - Need PPC Strategy

**From:** Jennifer Martinez <jennifer@newproductlaunch.com>
**Date:** Mon, 17 Mar 2026 07:45:00 +0000
**Category:** client
**Priority:** MEDIUM

## Email Content

Hello,

I'm launching a new product on Amazon next month (premium yoga mats) and want to make sure I have a solid PPC strategy from day one.

I've heard that the first few weeks are critical for ranking, and I don't want to waste money on ineffective campaigns.

My budget is $10,000 for the first month. I'm looking for someone who can:

1. Set up the initial campaign structure
2. Handle keyword research and targeting
3. Monitor and optimize daily during the launch phase
4. Help me understand TACOS vs ACOS (I keep seeing conflicting advice)

Do you offer product launch services? If so, what's your process and pricing?

I'd also love to see a case study or example of a successful launch you've managed.

Thanks!
Jennifer Martinez
New Product Launch Consulting
jennifer@newproductlaunch.com

## Suggested Actions

- [ ] Review email content
- [ ] Draft response
- [ ] Take appropriate action based on category

## Metadata

- Email ID: test003
- Labels: UNREAD, INBOX
- Thread ID: test003
- Processed: 2026-03-17 10:00:00

---

*Test email for Orchestrator*
*Silver Tier - AI Employee*
`
    }
];

console.log('Creating test emails for orchestrator...\n');

for (const email of testEmails) {
    const filePath = path.join(needsActionPath, email.filename);
    fs.writeFileSync(filePath, email.content);
    console.log(`✓ Created: ${email.filename}`);
}

console.log('\n✓ Test emails created successfully!');
console.log('\nNext steps:');
console.log('1. Run orchestrator: node orchestrator.js');
console.log('2. Review drafts in Vault/Pending_Approval/');
console.log('3. Approve drafts with: node approve-and-send.js "DRAFT_filename.md"');
