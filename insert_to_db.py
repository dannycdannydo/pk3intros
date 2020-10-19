import mysql.connector

def insert_to_db(data):
  mydb = mysql.connector.connect(
    host="surveyorstoolkit.database.windows.net",
    user="dannycdannydo",
    password="Kn1fedge",
    database="mydatabase"
  )

  mycursor = mydb.cursor()
  get_insert_statement
  sql = "INSERT INTO pk3intros (name, address) VALUES (%s, %s)"
  val = ("John", "Highway 21")
  mycursor.execute(sql, val)

  mydb.commit()

  print(mycursor.rowcount, "record inserted.")

def get_insert_statement(data):
  statement = ''
