import sys
import json
import sqlite3

inp = "";

for line in sys.stdin:
    inp += line.rstrip()

#print(inp, file=sys.stderr)

goodAnswers = json.loads(inp)

con = sqlite3.connect("reviews")
cur = con.cursor()

sqlRequest = "INSERT INTO GoodAnswers (rus, ger, gerEx1, gerEx2, rusEx1, rusEx2) VALUES "
for answer in goodAnswers[:-1]:
    rus = answer["Rus"]
    ger = answer["Ger"]
    gerEx1 = answer["GerEx1"]
    gerEx2 = answer["GerEx2"]
    rusEx1 = answer["RusEx1"]
    rusEx2 = answer["RusEx2"]

    sqlRequest += f"('{rus}', '{ger}', '{gerEx1}', '{gerEx2}', '{rusEx1}', '{rusEx2}'), "

answer = goodAnswers[-1]

rus = answer["Rus"]
ger = answer["Ger"]
gerEx1 = answer["GerEx1"]
gerEx2 = answer["GerEx2"]
rusEx1 = answer["RusEx1"]
rusEx2 = answer["RusEx2"]

sqlRequest += f"('{rus}', '{ger}', '{gerEx1}', '{gerEx2}', '{rusEx1}', '{rusEx2}')"

cur.execute(sqlRequest)
con.commit()
