from utils import send_lex_message, wait_for_log


def test_lambda_logs_for_troubleshoot():
    send_lex_message("My internet is slow")

    assert wait_for_log("TroubleshootInternet"), \
        "Expected TroubleshootInternet log not found"


def test_fallback_logs():
    send_lex_message("asdf1234 ???")

    assert wait_for_log("FallbackIntent"), \
        "Fallback intent log not found"


def test_agent_handoff_logs():
    send_lex_message("speak to agent")

    assert wait_for_log("SpeakToAgent"), \
        "Agent handoff log not found"
