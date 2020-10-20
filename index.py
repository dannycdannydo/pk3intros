import fetch_mail
import insert_to_db
import schedule
import time

def process():
    email_data = fetch_mail.get_email_data()
    for i in range(len(email_data)):
        insert_to_db.insert_to_db(email_data[i])

schedule.every(5).seconds.do(process)


while True:
    schedule.run_pending()
    time.sleep(1)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)