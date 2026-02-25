from user_scanner.core.orchestrator import status_validate


def validate_osu(user):
    url = f"https://osu.ppy.sh/users/{user}"
    show_url = "https://osu.ppy.sh"

    return status_validate(
        url, 404, [200, 302], show_url=show_url, follow_redirects=True
    )
