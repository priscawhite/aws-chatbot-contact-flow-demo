import json
import boto3
import re
from boto3.dynamodb.conditions import Key
import random

# DynamoDB setup
TABLE_NAME = "TechWithEaseCustomers"
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

# Amazon Connect client
connect = boto3.client("connect")

CONNECT_INSTANCE_ID = "INSTANCE_ID"
CONTACT_FLOW_ID = "CONTACT_FLOW_ID"

# -----------------------------
# Normalize phone number
# -----------------------------
def normalize_phone(phone):
    digits = re.sub(r"\D", "", phone)

    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]

    return digits

# -----------------------------
# Build Lex response
# -----------------------------
def close(intent_name, state, message, session_attrs=None):
    return {
        "sessionState": {
            "dialogAction": {"type": "Close"},
            "intent": {
                "name": intent_name,
                "state": state
            },
            "sessionAttributes": session_attrs or {}
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ]
    }

# -----------------------------
# Elicit Intent
# -----------------------------
def elicit_intent(message, session_attrs=None):
    session_attrs = session_attrs or {}

    retry_count = int(session_attrs.get("retryCount", "0"))
    retry_count += 1

    session_attrs["retryCount"] = str(retry_count)

    return {
        "sessionState": {
            "dialogAction": {
                "type": "ElicitIntent"
            },
            "sessionAttributes": session_attrs
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ]
    }

# -----------------------------
# Agent Hand-off Function
# -----------------------------
def handoff_to_agent(user_input, phone):
    try:
        response = connect.start_chat_contact(
            InstanceId=CONNECT_INSTANCE_ID,
            ContactFlowId=CONTACT_FLOW_ID,
            ParticipantDetails={
                "DisplayName": phone if phone else "Customer"
            },
            Attributes={
                "issue": user_input,
                "phone": phone if phone else "N/A"
            }
        )

        contact_id = response.get("ContactId", "N/A")

        return f"Connecting you to a live agent now. Your reference ID is {contact_id}."

    except Exception as e:
        print("Connect ERROR:", str(e))
        return "I'm having trouble connecting you to an agent right now, but someone will reach out shortly."

# -----------------------------
# Handlers
# -----------------------------
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

    if not items:
        return close(intent_name, "Failed",
                     f"I couldn't find any records for phone number {raw_phone}. "
                     f"Would you like to speak to an agent?")

    item = sorted(items, key=lambda x: x.get("lastTicketID", ""), reverse=True)[0]

    first_name = item.get("firstName", "")
    ticket_id = item.get("lastTicketID", "N/A")
    ticket_status = item.get("ticketStatus", "Unknown")

    message = (
        f"Hi {first_name if first_name else 'there'}, "
        f"your ticket ({ticket_id}) is currently {ticket_status}. "
        f"If you'd like, I can connect you to an agent for more details."
    )

    return close(intent_name, "Fulfilled", message,
        session_attrs = {
            "customerPhone": phone,
            "customerName": name,
            "ticketId": ticket_id,
            "escalateToAgent": "true",
            "issueType": "ticketStatus"
            }
        )

# -----------------------------
# Billing Help Handler
# -----------------------------
def handle_billing_help(event):
    intent_name = event["sessionState"]["intent"]["name"]

    message = (
        "I can provide you a link to our FAQ page for answers to commonly asked questions or "
        "I can connect you with a billing specialist to help answer questions like charges, invoices, or payments. "
        "Which would you prefer?"
    )

    return close(
        "BillingHelp",
        "Fulfilled",
        "Let me connect you to our billing team.",
        session_attrs={
            "escalateToAgent": "true",
            "issueType": "billing"
        }
    )

# -----------------------------
# Speak To Agent Handler
# -----------------------------
def handle_speak_to_agent(event):
    intent_name = event["sessionState"]["intent"]["name"]

    user_input = event.get("inputTranscript", "").lower()

    # -----------------------------
    # Conditional Routing
    # -----------------------------

    # Ticket Status Routing
    if "ticket" in user_input or "status" in user_input:
        return elicit_intent(
            "Ok, I can help you get connected to an agent about the status of your ticket"
        )

    # Internet Troubleshooting Routing
    elif any(word in user_input for word in ["internet", "wifi", "connection"]):
        return elicit_intent(
            "It appears you're having an issue with your internet connection. "
            "I can open a support ticket so that a technician can begin troubleshooting your issue."
        )

    # -----------------------------
    # Otherwise: Default Hand-off
    # -----------------------------
    slots = event.get("sessionState", {}).get("intent", {}).get("slots", {})
    phone_slot = slots.get("CustomerPhone")

    phone = None
    if phone_slot and "value" in phone_slot:
        phone = normalize_phone(phone_slot["value"].get("interpretedValue"))

    message = handoff_to_agent(user_input, phone)

        return close(intent_name, "Fulfilled", message)
        return close(intent_name, "Fulfilled", message,
            session_attrs = {
                "escalateToAgent": "true",
                "customerPhone": phone or "",
                "issueType": "agent_request"
                }
            )

# -----------------------------
# Troubleshooting Handler
# -----------------------------
def handle_troubleshoot_internet(event):
    intent_name = event["sessionState"]["intent"]["name"]
    slots = event.get("sessionState", {}).get("intent", {}).get("slots", {})

    # Extract slots
    name_slot = slots.get("CustomerName")
    phone_slot = slots.get("CustomerPhone")
    email_slot = slots.get("CustomerEmail")
    issue_slot = slots.get("IssueDescription")

    if not all([name_slot, phone_slot, email_slot, issue_slot]):
        return close(intent_name, "Failed",
                     "I'm missing some information. Please provide your name, phone, email, and issue description.")

    # Get values
    full_name = name_slot["value"]["interpretedValue"]
    raw_phone = phone_slot["value"]["interpretedValue"]
    email = email_slot["value"]["interpretedValue"]

    normalized_phone = normalize_phone(raw_phone)

    # Split the name
    name_parts = full_name.strip().split()
    first_name = name_parts[0] if len(name_parts) > 0 else ""
    last_name = name_parts[-1] if len(name_parts) > 1 else ""

    # Generate ticket ID (TCK-2XXX)
    ticket_id = f"TCK-2{random.randint(100, 999)}"

    # Ticket status
    ticket_status = "Open, New"

    # Save to DynamoDB
    table.put_item(
        Item={
            "phoneNumber": normalized_phone,
            "firstName": first_name,
            "lastName": last_name,
            "emailAddress": email,
            "accountType": "Personal",
            "subscriptionLevel": "Standard",
            "lastTicketID": ticket_id,
            "preferredLanguage": "English",
            "ticketStatus": ticket_status,
        }
    )

    message = (
        f"{first_name}, support ticket {ticket_id} has been opened on your behalf with status {ticket_status}. "
        f"Please save this information for future reference. "
        f"A technician will contact you at {raw_phone} to assist you with your issue."
    )

    return close(intent_name, "Fulfilled", message)

# -----------------------------
# Fallback Handler
# -----------------------------
def handle_fallback(event):
    attrs = event["sessionState"].get("sessionAttributes", {})
    retry = int(attrs.get("retryCount", "0"))

    if retry >= 2:
        return close(
            "FallbackIntent",
            "Something went wrong. Let me connect you to an agent for further assistance",
            {"escalateToAgent": "true"}
        )

    return elicit_intent(
        "I didn’t quite understand that. Can you tell me how I can help?",
        attrs
    )

# -----------------------------
# Intent Router (MAIN)
# -----------------------------
def lambda_handler(event, context):
    try:
        print("FULL EVENT:", json.dumps(event, indent=2))

        intent_name = event["sessionState"]["intent"]["name"]

        if intent_name == "TicketStatus":
            return handle_ticket_status(event)

        elif intent_name == "BillingHelp":
            return handle_billing_help(event)

        elif intent_name == "SpeakToAgent":
            return handle_speak_to_agent(event)

        elif intent_name == "TroubleshootInternet":
            return handle_troubleshoot_internet(event)

        else:
            return handle_fallback(event)
