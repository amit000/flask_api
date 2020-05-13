from typing import List
from requests import Response, post
import os

FROM_TITLE = "amit"
FROM_EMAIL = "amit.ganojekar@gmail.com"


def send_conf_email(email: List[str], subject: str, text: str, html) -> Response:

    return post(
        f"https://api.mailgun.net/v3/{os.environ.get('MAILGUN_DOMAIN')}/messages",
        auth=("api", os.environ.get("MAILGUN_API_KEY")),
        data={
            "from": f"{FROM_TITLE} <{FROM_EMAIL}>",
            "to": email,
            "subject": subject,
            "text": text,
            "html": html,
        },
    )
