import fetch_mail


def process():
    email_data = fetch_mail.get_email_data()
    print(email_data)


process()