import datetime as dt
import email
import imaplib
from typing import List, Sequence

from obsidianizer.email_tools.utils import (
    EmailMessageType,
    get_email_datetime,
    get_first_text_block,
)
from obsidianizer.latex_tools.utils import (
    LATEX_DOCUMENT_ENDING,
    LATEX_DOCUMENT_HEADER,
    parse_dated_comment_to_latex_item,
)


class EmailHandler(object):
    """Class that provides an interface to establish and interact with an
    email login session.
    """

    def __init__(self, user: str, password: str):
        self.email_user = user
        self.email_pass = password
        self.port = 993
        self.host = "imap.gmail.com"

        self.mail: imaplib.IMAP4_SSL = imaplib.IMAP4_SSL(self.host, self.port)

    def login(self) -> None:
        self.mail.login(self.email_user, self.email_pass)

    def get_folders_list(self) -> Sequence[str]:
        """Returns the list of folders in the email account

        Returns:
            List[str]: [description]
        """
        self.mail.select()
        list_email_folders_bytes: List[bytes] = self.mail.list()[1]  # type: ignore

        list_email_folders = [
            x.decode("utf-8") for x in list_email_folders_bytes if isinstance(x, bytes)
        ]
        cleaned_email_folders = [folder.split('"')[-2] for folder in list_email_folders]

        return cleaned_email_folders

    def search_uids(self, folder: str = "[Gmail]/Drafts") -> List[str]:
        """
        Returns the uids of the emails in the search
        """
        self.mail.select(folder)  # connect to inbox.

        # Search and return uids We dont get the emails themselves.
        result, data = self.mail.uid("search", "ALL")

        if result != "OK":
            print("No uids obtained")

        list_uids_bytes = data[0].split()
        list_uids = [x.decode("utf-8") for x in list_uids_bytes]
        return list_uids

    def read_email(self, uid: str) -> EmailMessageType:
        """Reads an email by its uid.
        It returns its "email library formatted" email_message
        """
        # Fetch the email by uid
        result, data = self.mail.uid("fetch", uid, "(RFC822)")

        if result != "OK":
            print("No email obtained")

        raw_email = data[0][1]
        raw_email_string = raw_email.decode("utf-8")

        # get the email_message formated from the email library !!
        email_message = email.message_from_string(raw_email_string)

        return email_message

    def download_emails_to_latex(
        self, folder: str = "[Gmail]/Drafts", filename: str = "./email_downloads"
    ) -> str:
        """Saves all of the drafts into disk with latex format"""

        draft_uids = self.search_uids(folder=folder)
        n_emails = len(draft_uids)
        all_text = LATEX_DOCUMENT_HEADER

        print("Total emails: ", n_emails)

        for i in range(n_emails):
            if i % 10 == 0:
                print("Processing ", i, "/", n_emails)

            uid = draft_uids[i]
            email_message = self.read_email(uid)
            text = get_first_text_block(email_message)
            datetime = get_email_datetime(email_message)

            text = parse_dated_comment_to_latex_item(text, datetime)
            all_text += text
        all_text += LATEX_DOCUMENT_ENDING

        print("All emails downloaded")
        dump_date = dt.datetime.now()
        fd = open(f"{filename}_({str(dump_date)}).tex", "w+")
        fd.write(all_text)
        fd.close()

        return all_text

    def delete_emails(self, folder: str = "[Gmail]/Drafts"):
        """Delete all the emails in the given email folder"""
        draft_uids = self.search_uids(folder=folder)
        n_emails = len(draft_uids)
        print("Total emails to delete: ", n_emails)
        for i in range(n_emails):
            if i % 10 == 0:
                print("Processing ", i, "/", n_emails)
            uid = draft_uids[i]
            self.mail.uid("store", uid, "+FLAGS", r"(\Deleted)")

    def logout(self) -> None:
        """Logout from the session"""
        if self.mail is None:
            pass
        else:
            self.mail.expunge()
            self.mail.close()
            self.mail.logout()
