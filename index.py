import fetch_mail
import insert_to_db
import schedule
import time

import os
from flask import Flask
app = Flask(__name__)

@app.route("/")
def process():
    email_data = fetch_mail.get_email_data()
    for i in range(len(email_data)):
        insert_to_db.insert_to_db(email_data[i])
    return "Hello from Python!"

schedule.every(5).seconds.do(process)

while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)