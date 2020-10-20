import pyodbc

def insert_to_db(data):
      print(data)
      import pyodbc
      cnxn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:surveyorstoolkit.database.windows.net,1433;Database=Surveyors_Toolkit;Uid=dannycdannydo;Pwd=Kn1fedge;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
      cursor = cnxn.cursor()
      val = ''
      columns = ''
      if len(data["message_recipient"]) > 2:
            val = (data["message_body"], data["message_from"],  data["message_subject"], data["message_filename"],
            data["message_recipient"][0]['email'], data["message_recipient"][1]['email'], data["message_recipient"][2]['email'],
            data["message_recipient"][0]['name'], data["message_recipient"][1]['name'], data["message_recipient"][2]['name'],
            data["message_recipient"][0]['org'], data["message_recipient"][1]['org'], data["message_recipient"][2]['org'],
            data["message_date"])
            columns = '(message_body, message_from, message_subject, message_filename, message_recipient_email_1, message_recipient_email_2, message_recipient_email_3 message_recipient_name_1, message_recipient_name_2, message_recipient_name_3, message_recipient_org_1, message_recipient_org_2, message_recipient_org_3, message_date)'
      elif len(data["message_recipient"]) == 2:
            val = (data["message_body"], data["message_from"],  data["message_subject"], data["message_filename"],
            data["message_recipient"][0]['email'], data["message_recipient"][1]['email'],
            data["message_recipient"][0]['name'], data["message_recipient"][1]['name'],
            data["message_recipient"][0]['org'], data["message_recipient"][1]['org'],
            data["message_date"])
            columns = '(message_body, message_from, message_subject, message_filename, message_recipient_email_1, message_recipient_email_2, message_recipient_name_1, message_recipient_name_2, message_recipient_org_1, message_recipient_org_2, message_date)'
      elif len(data["message_recipient"]) == 1:
            val = (data["message_body"], data["message_from"],  data["message_subject"], data["message_filename"],
            data["message_recipient"][0]['email'],
            data["message_recipient"][0]['name'],
            data["message_recipient"][0]['org'],
            data["message_date"])
            columns = '(message_body, message_from, message_subject, message_filename, message_recipient_email_1, message_recipient_name_1, message_recipient_org_1, message_date)'
      else:
            val = (data["message_body"], data["message_from"], data["message_subject"], data["message_filename"], data["message_date"])
            columns = '(message_body, message_from, message_subject, message_filename, message_date)'
      print("INSERT INTO pk3intros %s VALUES (%s)" % (columns, val))
      cursor.execute("INSERT INTO pk3intros %s VALUES %s" % (columns, val))
      cnxn.commit()

