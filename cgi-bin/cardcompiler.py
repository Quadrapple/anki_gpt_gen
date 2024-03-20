import genanki

def create_anki_deck(deck_name, notes, output_file=None):
    deck_id = 2285404172
    model_id = 1895704477

    my_model = genanki.Model(
        model_id,
        'Auto-Cloze',
        fields=[
            {'name': 'Text'},
            {'name': 'Back Extra'},
            {'name': 'Translated'},
        ],
        templates=[
            {
                'name': 'Cloze 1',
                'type': '1',
                'qfmt': '<p class="translatedText">{{Translated}}</p><hr><br>{{cloze:Text}}',
                'afmt': ('<p class="translatedText">{{Translated}}</p><hr><br>'
                         '{{cloze:Text}}<br>'
                         '<p class="backText">{{Back Extra}}</p>'),
            },
        ],
        css=(
            '.card {'
            'font-family: arial;'
            'font-size: 20px;'
            'text-align: left;'
            'color: black;'
            'background-color: white;'
            '}'
            ''
            '.translatedText {'
            'color: #0a0a0a;'
            'font-size: 22px;'
            '}'
            ''
            '.cloze {'
            'font-weight: bold;'
            'color: blue;'
            '}'
            ''
            '.nightMode .cloze {'
            'color: lightblue;'
            '}'
            ''
            '.backText{'
            'font-size: 20px;'
            'color: #500050;'
            '}'
        ))

    my_deck = genanki.Deck(deck_id, deck_name)

    for note in notes:
        my_note = genanki.Note(model=my_model, fields=[note['text'], note['back_extra'], note['translated']])
        my_deck.add_note(my_note)

    if not output_file:
        output_file = f"../{deck_name.replace(' ', '_')}.apkg"

    genanki.Package(my_deck).write_to_file(output_file)


def parse_entries(entries):
    notes = []

    for entry in entries:

        tr_word = entry['Rus']
        ger_word = entry['Ger']
        back_extra_lines = []

        text = entry['GerEx1'] + '<br>' + entry['GerEx2']
        back_extra = entry['RusEx1'] + '<br>' + entry['RusEx2']

        notes.append({
            'text': text,
            'back_extra': back_extra,
            'translated': tr_word
        })

    return notes

def convert(input_data):
    deck_name = 'GerRus Auto Cloze'
    notes = parse_entries(input_data)

    create_anki_deck(deck_name, notes)
