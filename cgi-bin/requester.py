from openai import OpenAI
import os
from request import *

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

user_prompt = "" #"Привет. Пожалуйста, сделай мне карточки ANKI для этих немецких слов/фраз:\n" 


def ask(entries):
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt + entries}
      ]
    )

    return(completion.choices[0].message.content)
