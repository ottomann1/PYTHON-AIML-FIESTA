import os
from nltk.tokenize import word_tokenize
import openai
from api_secrets import OPENAI_API_KEY
import mysql.connector
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import functools
import operator


openai.api_key = OPENAI_API_KEY
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="afdata"
)
cursor = mydb.cursor()

cursor.execute(
    "select id, description from small_prompt_object where id > 1531 and id < 3000")
results = cursor.fetchall()

for x in results:
    new = x[1]
    completion = openai.Completion.create(
        model="text-davinci-003",
        prompt=("Tell me only the technologies used in bullet points   Tell me the office location if mentioned   Tell me the industry if mentioned  Text: ### "
                + new + " ###"),
        temperature=0,
        max_tokens=500
    )
    text = completion.choices[0].text
    print(text)

    sql = "INSERT INTO openaiprompt (id, prompt, completion) VALUES (%s, %s, %s)"
    val = (x[0]+100000, new, text)
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
