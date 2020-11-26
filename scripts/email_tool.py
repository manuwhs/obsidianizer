import click
from obsidianizer.email_tools.email_handler import EmailHandler


@click.group(
    help="""Tool to download and delete emails from folders in your email service provider. Example usage: 

    1) List the available folders in your account:\n
        python email_tool.py folders -u your_email@gmail.com

    2) Download the emails within an email folder in latex format:\n
        python email_tool.py download -u your_email@gmail.com -f my_folder -o ./my_emails.txt
    
    3) Detele all the emails in an email folder:\n
        python email_tool.py download -u your_email@gmail.com -f my_folder 
"""
)
def main():
    pass


@main.command(help="List the folders in your email account.")
@click.option("-u", "--user", help="Email address", required=True)
@click.option("-p", "--password", help="Password of the email address", required=True, prompt=True, hide_input=True)
def folders(user: str, password: str):
    my_email_handler = EmailHandler(user, password)
    my_email_handler.login()
    folder_list = my_email_handler.get_folders_list()

    print("List of folders: ")
    for folder in folder_list:
        print(folder)
    my_email_handler.logout()


@main.command(help="Download the emails in a given email folder in latex format.")
@click.option("-u", "--user", help="Email address", required=True)
@click.option("-p", "--password", help="Password of the email address", required=True, prompt=True, hide_input=True)
@click.option("-f", "--email_folder", default="[Gmail]/Kladder", help="Email folder to download")
@click.option(
    "-o", "--output", default="./drafts.txt", help="Filename of the output file where the emails will be stored"
)
def download(user: str, password: str, email_folder: str, output: str):

    my_email_handler = EmailHandler(user, password)
    my_email_handler.login()
    my_email_handler.download_emails_to_latex(email_folder, output)
    my_email_handler.logout()


@main.command(help="Delete the emails in a given email folder.")
@click.option("-u", "--user", help="Email address", required=True)
@click.option("-p", "--password", help="Password of the email address", required=True, prompt=True, hide_input=True)
@click.option("-f", "--email_folder", default="[Gmail]/Kladder", help="Email folder to delete emails from")
def delete(user: str, password: str, email_folder: str):
    my_email_handler = EmailHandler(user, password)
    my_email_handler.login()
    my_email_handler.delete_emails(email_folder)
    my_email_handler.logout()


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
