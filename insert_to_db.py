import pyodbc

def insert_to_db(data):
  cnx = mysql.connector.connect(user='dannycdannydo@surveyorstoolkit.database.windows.net', password='Knifedge',
                                database='Surveyors_Toolkit')

  mycursor = cnx.cursor()
  sql = "INSERT INTO pk3intros (message_body, message_from, message_subject, " \
        "message_recipient_email_1, message_recipient_email_2, message_recipient_email_3" \
        "message_recipients_name_1, message_recipient_name_2, message_recipient_name_3" \
        "message_recipient_org_1, message_recipient_org_2, message_recipient_org_3" \
        "message_date) " \
        "VALUES (%s, %s)"
  val = (data["message_body"], data["message_from"],  data["message_subject"],
         data["message_recipient"][0]['email'], data["message_recipient"][1]['email'], data["message_recipient"][2]['email'],
         data["message_recipient"][0]['name'], data["message_recipient"][1]['name'], data["message_recipient"][2]['name'],
         data["message_recipient"][0]['org'], data["message_recipient"][1]['org'], data["message_recipient"][2]['org'],
         data["message_date"])
  mycursor.execute(sql, val)

  cnx.commit()

  print(mycursor.rowcount, "record inserted.")

