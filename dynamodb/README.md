# **DynamoDB Configuration & Usage**

## **Overview**
This project uses Amazon DynamoDB as a fully managed NoSQL database to store and retrieve chatbot session data, troubleshooting history, and user interaction metadata.

DynamoDB integrates with AWS Lambda to provide fast, scalable, and serverless data persistence for the Amazon Lex chatbot.

---

## **Table Design**

### Table Name
TechWithEaseCustomers

### Primary Key
| Attribute Name | Type   | Key Type      |
|----------------|--------|---------------|
| phoneNumber    | String | Partition Key |

---

## **Attributes**

| Attribute Name    | Type   | Description |
|-------------------|--------|-------------|
| phoneNumber       | String | Customer phone, session identifier |
| accountType       | String | Personal or Business account |
| emailAddress      | String | Customer email address |
| firstName         | String | Customer first name |
| lastName          | String | Customer last name |
| lastTicketID      | String | Number of current open ticket (TCK-XXXX) |
| preferredLanguage | String | Customer preferred language |
| subscriptionLevel | String | Standard or Premium subscription level |
| ticketStatus      | String | Ticket status (e.g., OPEN, IN PROGRESS, CLOSED) |

---

## **Provisioning**

| Capacity Mode | Alternative |
|---------------|-------------|
| On-demand     | Provisioned capacity with auto-scaling for predictable workloads |

---

## **IAM Permissions**

### Lambda Execution Role Permissions
- `dynamodb:PutItem`
- `dynamodb:GetItem`
- `dynamodb:UpdateItem`
- `dynamodb:Query`

Scope permissions to the specific table ARN for least privilege.

---

## **Data Flow**

1. User interacts with Lex chatbot
2. Lex triggers AWS Lambda function
3. Lambda queries data in DynamoDB using `CustomerPhone` from slot
4. Lambda returns `{ticket_id}` and `{ticket_status}` in messaging to the user
5. On user escalation, chat initiated with agent containing customer and ticket attributes

---

## **Example Event**

```json
{
  "sessionId": "test-session-001",
  "inputTranscript": "Check my ticket status",
  "sessionState": {
    "intent": {
      "name": "CheckTicketStatus",
      "state": "ReadyForFulfillment",
      "slots": {
        "CustomerPhone": {
          "value": {
            "originalValue": "212-555-0019",
            "interpretedValue": "212-555-0019",
            "resolvedValues": ["212-555-0019"]
          }
```

---

## **Lambda Integration Example (Python)**

```python
import boto3
from boto3.dynamodb.conditions import Key

TABLE_NAME = "TechWithEaseCustomers"
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

def handle_ticket_status(event):
    intent_name = event["sessionState"]["intent"]["name"]
    slots = event.get("sessionState", {}).get("intent", {}).get("slots", {})

    phone_slot = slots.get("CustomerPhone")

    if not phone_slot or "value" not in phone_slot:
        return close(intent_name, "Failed",
                     "I didn’t catch your phone number. Please provide it so I can check your ticket.")

    raw_phone = phone_slot["value"].get("interpretedValue")
    normalized_phone = normalize_phone(raw_phone)

    response = table.query(
        KeyConditionExpression=Key("phoneNumber").eq(normalized_phone)
    )

    items = response.get("Items", [])

.....

    message = (
          f"Hi {first_name if first_name else 'there'}, "
          f"your ticket ({ticket_id}) is currently {ticket_status}. "
          f"If you'd like, I can connect you to an agent for more details."
      )

.....

return close(intent_name, "Fulfilled", message,
        session_attrs = {
            "customerPhone": phone,
            "customerName": name,
            "ticketId": ticket_id,
            "escalateToAgent": "true",
            "issueType": "ticketStatus"
            }
        )
```

---

## **Querying Data**

### Get Ticket by phoneNumber

```python
response = table.query(
      KeyConditionExpression=Key("phoneNumber").eq(normalized_phone)
```

---

## **Monitoring**

### CloudWatch Metrics
- Read/Write capacity usage
- Throttled requests
- Latency

### Logging
- Enable detailed logging in Lambda for DynamoDB interactions

---

## **Related Files in Repo**

```
📂 dynamodb/
│── README.md
│── seed-data.json
└── table-definition.json
```

---

## **Future Enhancements**
- Store conversation transcripts
- Add analytics pipeline (e.g., Kinesis/S3/Athena)
- Add Global Secondary Index (GSI) for querying by emailAddress
