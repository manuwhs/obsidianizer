import datetime as dt
import email
import os
from typing import Any, List, Optional, Tuple

import html2text

DATETIME_FORMAT_EMAIL = "%a, %d %b %Y %H:%M:%S %z"

EmailMessageType = Any  # mail.message.Message ## Somehow this fails when running cli


def get_email_datetime(email_message: EmailMessageType) -> dt.datetime:
    datetime_str = email_message["Date"]
    datetime = dt.datetime.strptime(datetime_str, DATETIME_FORMAT_EMAIL)
    return datetime


def get_first_text_block(
    email_message: EmailMessageType, plain_text: bool = True
) -> str:
    """Gets an email message as input and returns its text content
    Notice the format of returned text has peculiarities like added \n
    from gmail formatting. These probably should be removed along the pipeline"""

    maintype = email_message.get_content_maintype()
    payload = b""

    if maintype == "multipart":
        for part in email_message.get_payload():
            if part.get_content_maintype() == "text":
                # We get the last version of the email
                payload = part.get_payload(decode=True)
    elif maintype == "text":
        payload += email_message.get_payload(decode=True)

    if plain_text:
        return html2text.html2text(payload.decode("utf-8"))
    else:
        return payload.decode("utf-8")


def get_email_from_to(
    email_message: EmailMessageType,
) -> Tuple[Optional[List[Tuple[str, str]]], Tuple[str, str]]:
    """Returns the from and to email addresses of the message"""
    email_to = email_message["To"]
    email_from = email.utils.parseaddr(email_message["From"])  # type: ignore

    return email_to, email_from


def download_attachments(
    email_message: EmailMessageType, download_filedir: str
) -> None:
    """Download all the attachments of a given email"""
    for part in email_message.walk():
        # this part comes from the snipped I don't understand yet...
        if part.get_content_maintype() == "multipart":
            continue
        if part.get("Content-Disposition") is None:
            continue
        filename = part.get_filename()
        if bool(filename):
            filePath = os.path.join(download_filedir, filename)
            if not os.path.isfile(filePath):
                fp = open(filePath, "wb")
                fp.write(part.get_payload(decode=True))
                fp.close()
                print(f"Downloaded {filename}")
