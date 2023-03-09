from langdetect import detect
import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="afdata"
)
cursor = mydb.cursor()

cursor.execute("select * from small_prompt_object")
results = cursor.fetchall()
for x in results:
    jobtext = x[4]
    print(x[0])
    lang = detect(jobtext)
    sql = "UPDATE small_prompt_object SET detected_language = %s WHERE id = %s"
    val = (lang, x[0])
    cursor.execute(sql, val)
    mydb.commit()
