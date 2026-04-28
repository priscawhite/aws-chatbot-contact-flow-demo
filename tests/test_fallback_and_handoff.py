from utils import send_lex_message


def test_fallback_intent():
    response = send_lex_message("asdf1234 ???")

    intent_name = response["sessionState"]["intent"]["name"]

    assert intent_name in ["FallbackIntent", "AMAZON.FallbackIntent"]


def test_agent_handoff():
    response = send_lex_message("I want to speak to an agent")

    intent_name = response["sessionState"]["intent"]["name"]

    assert intent_name == "SpeakToAgent"

    # Validate dialog action
    dialog_action = response["sessionState"]["dialogAction"]["type"]
    assert dialog_action in ["Close", "ElicitIntent"]
