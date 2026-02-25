import re

from user_scanner.core.helpers import get_random_user_agent
from user_scanner.core.orchestrator import generic_validate
from user_scanner.core.result import Result


def validate_linkedin(user: str) -> Result:
    if not re.match(r"^[a-zA-Z0-9](?:[a-zA-Z0-9-]{1,98}[a-zA-Z0-9])?$", user):
        return Result.error(
            "LinkedIn username must be 3-100 chars, alphanumeric with optional hyphens"
        )

    url = f"https://www.linkedin.com/in/{user}"

    headers = {
        "User-Agent": get_random_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
    }

    def process(response):
        status = response.status_code
        text = response.text.lower()

        if status == 404:
            return Result.available()

        if status in [429, 999]:
            return Result.error(f"[{status}] LinkedIn rate-limited or blocked this request")

        if status == 403:
            return Result.error("[403] Request forbidden, try using proxy or VPN")

        if status == 200:
            # Public profile pages and auth walls can both indicate a real account.
            sign_in_wall = (
                "sign in to view profile" in text
                or "join to view profile" in text
                or "/authwall" in str(response.url).lower()
            )
            markers = (
                f"/in/{user.lower()}" in text
                or f'"publicidentifier":"{user.lower()}"' in text
                or f'"entityuricdn":"urn:li:fsd_profile:{user.lower()}"' in text
            )

            if sign_in_wall or markers:
                return Result.taken()
            return Result.error("Unexpected LinkedIn response")

        return Result.error(f"[{status}] Unexpected status code")

    return generic_validate(
        url,
        process,
        show_url=url,
        headers=headers,
        follow_redirects=True,
        timeout=8.0,
    )
