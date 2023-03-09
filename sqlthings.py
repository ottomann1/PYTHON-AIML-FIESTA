import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="afdata"
)
cursor = mydb.cursor()

cursor.execute(
    "select id, completion, prompt from openaiprompt where id>10000")
results = cursor.fetchall()
for x in results:
    # sql = "update openaiprompt set completion = %s where id = %s"
    sql = "insert into openaiprompt (completion, id, prompt) values (%s, %s, %s)"
    val = (x[1], x[0]-100000, x[2])

    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted. ")
