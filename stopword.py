import mysql.connector
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="afdata"
)
cursor = mydb.cursor()

cursor.execute(
    "select * from small_prompt_object")
results = cursor.fetchall()
for x in results:
    print(x[0])
    if x[12] == 'en':
        stop_words = set(stopwords.words('english'))
    if x[12] == 'sv':
        stop_words = set(stopwords.words('swedish'))
    jobtext = x[4]
    text_tokens = word_tokenize(jobtext)

    filtered_sentence = [
        w for w in text_tokens if not w.lower() in stop_words]
    filtered_sentence = []

    for w in text_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    complete_string = ''
    for word in filtered_sentence:
        complete_string = complete_string + word + ' '
    sql = "UPDATE small_prompt_object SET description = %s WHERE id = %s"
    val = (complete_string, x[0])
    cursor.execute(sql, val)
    mydb.commit()
