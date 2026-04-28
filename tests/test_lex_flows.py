from utils import send_lex_message


def test_troubleshoot_internet():
    response = send_lex_message("My internet is slow")

    assert response["sessionState"]["intent"]["name"] == "TroubleshootInternet"
    assert response["sessionState"]["intent"]["state"] in ["InProgress", "Fulfilled"]

    messages = response.get("messages", [])
    assert len(messages) > 0


def test_billing_inquiry():
    response = send_lex_message("I have a billing question")

    assert response["sessionState"]["intent"]["name"] == "BillingInquiry"
    assert response["sessionState"]["intent"]["state"] in ["InProgress", "Fulfilled"]
