from user_scanner.core.orchestrator import status_validate


def validate_codeberg(user):
    url = f"https://codeberg.org/{user}"
    show_url = "https://codeberg.org"

    return status_validate(url, 404, 200, show_url=show_url, follow_redirects=True)
