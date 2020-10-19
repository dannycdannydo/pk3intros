import fetch_mail
import insert_to_db


def process():
    email_data = fetch_mail.get_email_data()
    print(email_data)
    for i in range(len(email_data)):
        insert_to_db.insert_to_db(email_data)


process()