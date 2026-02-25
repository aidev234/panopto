from user_scanner.core.orchestrator import status_validate


def validate_patreon(user):
    url = f"https://www.patreon.com/{user}"
    show_url = "https://patreon.com"

    return status_validate(
        url, 404, 200, show_url=show_url, timeout=15.0, follow_redirects=True
    )
