from openai import OpenAI
import os
from request import *
import json
import sys

from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

system_prompt = """
You are a language teaching assistant highly proficient in German and Russian, you help a Russian speaker by generating Cloze ANKI cards to learn German.
You only reply in json format following this template for every entry:
{
    "Ger": "<the German word or phrase to be translated, do not enclose in brackets>",
    "Rus": "<up to 3 translations into Russian, separated with commas, do not enclose in brackets>",
    "GerEx1": "<example of the usage of the word/phrase in a German sentence with the word in cloze {{c1::[word/phrase]}} brackets>",
    "GerEx2": "<different example of the usage of the word/phrase in a German sentence with the word/phrase in cloze brackets>",
    "RusEx1": "<translation of GerEx1 into Russian with the translated word/phrase in the html bold <b>[word/phrase]</b> tags>",
    "RusEx2": "<different example of the usage of the word/phrase in a German sentence with the translated word/phrase in html bold>"
}

Enclose the to be translated word/phrase in the cloze {{c1:: }} brackets in the German sentences and
enclose the translated word/phrase in bold tags <b> </b> in the Russian sentences.

If the word is a noun, then include the article in the brackets only if it's standalone, as in
"{{c1::dem Mann}}", however, don't include it if it's bound to a preposition as in "zum {{c1::Mann}}".

All the entries should be separated with commas and enclosed in [] as a json list.

The sentences should be relatively complex and contain connectors like 'nevertheless' or 'however', they should also incorporate other words from the requests when appropriate to make it easier to memorize them.

The user also inputs their request in json form.

Here is an example of a request-response pair:
    User's request:
    {'Word': 'Feiern', Note': 'как существительное', 'Example': 'Das Feiern dauerte bis zum frühen Morgens'}
    Response:
    [
        {
             "Ger": "das Feiern",
             "Rus": "празднование, праздник",
             "GerEx1": "Ich weiß nicht, wie es bei Ihnen ist, aber in Schottland fängt erst an Heilig Abend {{c1::das Feiern}} an",
             "GerEx2": "Dies wird ein großartiger Tag und ein Grund zum {{c1::Feiern}} sein.",
             "RusEx1": "Не знаю, как у вас, но в Шотландии <b>празднование</b> начинается только в канун Рождества",
             "RusEx2": "Это будет замечательный день и повод для <b>праздника</b>."
         }
     ]

In this example the user forgot to add the article before the word, so it should be added in the response because the note said to
consider the word as a noun. The user has also provided a usage example to more precisely define what they want.
The note and usage examples are optional and you should try to capture all the meaning of the word in the 3 possible translations (sometimes 3 would be too much i.e. only "собака" is neccessary when translating der Hund).
"""
#OTHER
"""
You're a German and Russian language expert assistant, helping to create German learning Cloze ANKI cards for Russian speakers. Responses are in JSON format, structured as:
[{
"Ger": German word/phrase.
"Rus": Up to 3 Russian translations.
"GerEx1": German sentence with the word/phrase in cloze {{c1:: }}.
"GerEx2": Another German sentence example in cloze format.
"RusEx1": Russian translation of GerEx1, translated word/phrase in bold <b> </b>.
"RusEx2": Russian translation of GerEx2, word/phrase in bold <b> </b>.
},
{
<another entry>
}, ...]

For nouns, include the article in cloze brackets if standalone, exclude it with prepositions. Entries are in a JSON list, make sentences complex with connectors. User requests are in JSON.

Example:

User requests: {'Word': 'Feiern', 'Note': 'noun', 'Example': 'Das Feiern dauerte bis zum frühen Morgens'}
Response:
[{"Ger": "das Feiern","Rus": "празднование, праздник","GerEx1": "Ich weiß nicht, wie es bei Ihnen ist, aber in Schottland fängt erst an Heilig Abend {{c1::das Feiern}} an","GerEx2": "Dies wird ein großartiger Tag und ein Grund zum {{c1::Feiern}} sein.","RusEx1": "Не знаю, как у вас, но в Шотландии <b>празднование</b> начинается только в канун Рождества","RusEx2": "Это будет замечательный день и повод для <b>праздника</b>."} ]

Adjust for noun usage and integrate user-provided examples when available. Aim for precise translation within three options.
"""

user_prompt = "" #"Привет. Пожалуйста, сделай мне карточки ANKI для этих немецких слов/фраз:\n" 


def ask(entriesStr):
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      #response_format={"type": "json_object"},
      messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt + entriesStr}
      ]
    )

    return(completion.choices[0].message.content)

def askInContext(entriesStr, assistantCtxt, userCtxt):
    if(assistantCtxt != "" and userCtxt != ""):
        completion = client.chat.completions.create(
          model="gpt-3.5-turbo",
          #response_format={"type": "json_object"},
          messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt + userCtxt},
            {"role": "assistant", "content": assistantCtxt},
            {"role": "user", "content": "And now some more: " + entriesStr}
          ]
        )
    else:
        completion = client.chat.completions.create(
          model="gpt-3.5-turbo",
          #response_format={"type": "json_object"},
          messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt + entriesStr},
          ]
        )

    return(completion.choices[0].message.content)

def askMany(entries):
    reqThreshold = 11
    contextSize = 2 

    assert reqThreshold >= contextSize

    askAmount = (len(entries) - 1) // reqThreshold + 1

    strRes = ""
    res = []

    userContext =''
    assistantContext=b''

    #print("\n ASKAMOUNT:" + str(askAmount) + "\n", file=sys.stderr)


    for i in range(0, askAmount - 1):
        toAsk = repr(entries[i * reqThreshold:(i + 1) * reqThreshold]) 
        answer = askInContext(toAsk, assistantContext.decode(), userContext)

        res += json.loads(answer)
        #print("\nCONTEXT_USER:\n" + userContext + "\nCONTEXT_ASSISTANT:\n" + assistantContext.decode() + "\nNUM " + str(i) + ":\n" + answer, file=sys.stderr)

        userContext = repr(entries[i * reqThreshold + (reqThreshold - contextSize):(i + 1) * reqThreshold])
        assistantContext = json.dumps(res[-contextSize:], ensure_ascii=False).encode('utf-8')

        #strRes += "NUM " + str(i) + ":  " + answer

    answer = askInContext(repr(entries[(askAmount - 1) * reqThreshold:]), assistantContext.decode(), userContext)

    res += json.loads(answer)
    #strRes += "NUM " + str(askAmount - 1) + ":  " + answer
    #phirint("\nCONTEXT_USER:\n" + userContext + "\nCONTEXT_ASSISTANT: \n" + assistantContext.decode() + " \nNUM " + str((askAmount - 1)) + ":  \n" + answer, file=sys.stderr)
    #print("STRRES: \n: " + strRes, file=sys.stderr)

    return (res, " returned ")

