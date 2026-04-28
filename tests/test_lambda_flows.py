import json
from utils import invoke_lambda


def test_lambda_troubleshoot_response():
    event = {
        "sessionState": {
            "intent": {
                "name": "TroubleshootInternet"
            }
        },
        "inputTranscript": "My internet is slow"
    }

    response = invoke_lambda(json.dumps(event))
    payload = json.loads(response["Payload"].read())

    assert "messages" in payload
    assert payload["sessionState"]["intent"]["name"] == "TroubleshootInternet"


def test_lambda_fallback_routing():
    event = {
        "sessionState": {
            "intent": {
                "name": "FallbackIntent"
            }
        }
    }

    response = invoke_lambda(json.dumps(event))
    payload = json.loads(response["Payload"].read())

    assert payload["sessionState"]["intent"]["name"] == "SpeakToAgent"
