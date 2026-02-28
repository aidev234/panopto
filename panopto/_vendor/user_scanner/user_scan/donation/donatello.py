from user_scanner.core.orchestrator import status_validate

def validate_donatello(user):
    url = f"https://donatello.to/{user}"
    show_url = "https://donatello.to"

    return status_validate(url, 404, 200, show_url=show_url)
