from panopto.threat_signals import extract_threat_and_selector_signals


def test_capability_matches_require_proximity():
    far_text = "I want to travel next month. The gun show is downtown."
    near_text = "I want to buy a gun this weekend."

    far = extract_threat_and_selector_signals(far_text)
    near = extract_threat_and_selector_signals(near_text)

    assert "Possible Indicators of Capability" not in far["threat_signal_categories"]
    assert "Possible Indicators of Capability" in near["threat_signal_categories"]
    assert "gun" in [item.lower() for item in near["threat_matches"]]


def test_ideological_categories_follow_telerecon_indicators():
    text = "white genocide narrative from globalists and clown world posting"
    payload = extract_threat_and_selector_signals(text)

    assert "Indicators - White Identity Motivated Extremism" in payload["threat_categories"]
    assert "Indicators - Conspiratorial Ideation" in payload["threat_categories"]
