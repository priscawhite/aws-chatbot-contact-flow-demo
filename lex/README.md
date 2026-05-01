# **Amazon Lex Chatbot Configuration**

## Overview
This project uses an Amazon Lex chatbot to provide automated customer support and troubleshooting assistance. The bot is designed to handle common user inquiries, guide users through issue resolution, and seamlessly escalate to a live agent when necessary.

The chatbot integrates with AWS Lambda for backend logic and Amazon Connect for live agent handoff.

---

## **Bot Architecture**

### **Core Components**
- **Amazon Lex V2 Bot**
  - Natural language understanding (NLU)
  - Intent recognition
  - Slot management
- **AWS Lambda**
  - Fulfillment logic
  - Dynamic response handling
- **Amazon Connect**
  - Live agent escalation
- **CloudWatch Logs**
  - Debugging and monitoring

---

## **Bot Configuration**

### **Bot Details**
| Property           | Value            |
|--------------------|------------------|
| Bot Name           | TechWithEaseBot  |
| Runtime            | Lex V2           |
| Locale             | en_US            |
| Voice (optional)   | Danielle         |
| Session Timeout    | 5 minutes        |

---

## **Intents**

### 1. TroubleshootInternet
**Purpose:** Guides users to open a support ticket.

| Slot Name        | Type   | Required |
|------------------|--------|----------|
| CustomerEmail    | Custom | Yes      |
| CustomerName     | Custom | Yes      |
| CustomerPhone    | Custom | Yes      |
| IssueDescription | Custom | Yes      |

**Sample Utterances:**
- "my internet is not working"
- "wifi is slow"
- "connection keeps dropping"

**Fulfillment:**
- Invokes Lambda function
- Returns ticket confirmation

---

### 2. TicketStatus
**Purpose:** Gathers customer info for ticket status query.

| Slot Name     | Type   | Required |
|---------------|--------|----------|
| TicketNumber  | Custom | Yes      |
| CustomerPhone | Custom | Yes      |

**Sample Utterances:**
- "what is the status of my ticket?"
- "is my ticket being worked on?"
- "when will my issue be fixed?"

**Fulfillment:**  
- Invokes Lambda function  
- Retrieves ticket status from database

---

### 3. SpeakToAgent
**Purpose:** Transfers the user to a live agent.

**Sample Utterances:**
- "talk to an agent"
- "I need a representative"
- "customer support please"

**Fulfillment:**
- Triggers Amazon Connect flow
- Passes session attributes

---

### 4. FallbackIntent
**Purpose:** Handles unrecognized input.

**Behavior:**
- Automatically triggered when no intent matches
- Routes user to live agent via SpeakToAgent logic

---

## **Dialog Management**

### Slot Elicitation
- Required slots are prompted dynamically
- Validation handled via Lambda (if configured)

### Confirmation Prompts
- Used for critical actions (optional)
- Example: Confirm escalation to agent

---

## **Lambda Integration**

### Function Name
TechWithEaseBot

### Responsibilities
- Process intent requests
- Validate slot values
- Generate dynamic responses
- Route escalation requests

---

## **Live Agent Handoff**

### Integration with Amazon Connect
- Triggered via:
  - SpeakToAgent intent
  - FallbackIntent

### Flow Behavior
1. User requests agent or fallback is triggered
2. Lex passes control to Lambda
3. Lambda signals Connect contact flow
4. Chat session is transferred to live agent

---

## **Testing**

### Local Testing
Use sample test events:
- event_TroubleshootInternet.json
- event_SpeakToAgent.json
- event_FallbackIntent.json

Update test harness with:
```
with open("event_INTENTNAME.json") as f:
    event = json.load(f)

response = lambda_handler(event, None)
print(json.dumps(response, indent=2))
```
### In Console
- Use Lex test chat window
- Validate:
  - Intent recognition
  - Slot elicitation
  - Lambda responses

---

## **Logging & Monitoring**

### CloudWatch Logs
- Captures:
  - Incoming requests
  - Lambda execution logs
  - Errors and exceptions

### Metrics
- Intent success rate
- Fallback frequency
- Escalation rate

---

## **Deployment Notes**

- Export bot configuration as JSON for version control
- Use IAM roles with least privilege
- Enable versioning and aliases for safe updates

---

## **Related Files in Repo**
```
📂 lex/
│── bot-definition.json
│── README.md
│── 📂 intents/
│   └── 📂 BillingHelp/
│       ├── BillingHelp.json
│       └── 📂 Slots/
│           ├── CustomerName.json
│           └── BillingIssue.json
│   └── 📂 FallbackIntent/
│       ├── FallbackIntent.json
│   └── 📂 SpeakToAgent/
│       ├── SpeakToAgent.json
│       └── 📂 Slots/
│           ├── CustomerName.json
│           ├── CustomerPhone.json
│           └── IssueDescription.json
│   └── 📂 TicketStatus/
│       ├── ConversationFlow.json
│       ├── TicketStatus.json
│       └── 📂 Slots/
│           ├── CustomerPhone.json
│           └── TicketNumber.json
│   └── 📂 TroubleshootInternet/
│       ├── ConversationFlow.json
│       ├── TroubleshootInternet.json
│       └── 📂 Slots/
│           ├── CustomerEmail.json
│           ├── CustomerName.json
│           ├── CustomerPhone.json
│           └── IssueDescription.json
│── 📂 lambda/
│   └── techwitheasebot.py
│── 📂 SlotTypes/
│   ├── ContactPreferences.json
│   └── CustomerTiers.json
│── 📂 test-events/
│   ├── event_CheckTicketStatus.json
│   ├── event_SpeakToAgent.json
│   └── event_TroubleshootInternet.json
```
---

## **Future Enhancements**
- Integrate sentiment analysis (Amazon Kinesis --> CloudWatch dashboards)
- Add multilingual support (i.e. Spanish)
- Amazon Kendra indexes for Billing FAQ and agent assistance
