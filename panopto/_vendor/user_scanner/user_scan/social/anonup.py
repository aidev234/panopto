from user_scanner.core.orchestrator import status_validate


def validate_anonup(user):
    url = f"https://anonup.com/@{user}"
    show_url = "https://anonup.com"

    return status_validate(url, 302, 200, show_url=show_url)
