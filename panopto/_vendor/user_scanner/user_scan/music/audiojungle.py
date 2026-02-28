from user_scanner.core.orchestrator import status_validate

def validate_audiojungle(user):
    url = f"https://audiojungle.net/user/{user}"
    show_url = "https://audiojungle.net"

    return status_validate(url, 404, 200, show_url=show_url)
