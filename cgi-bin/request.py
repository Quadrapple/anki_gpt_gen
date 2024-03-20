from enum import Enum

class ContentType(Enum):
    WORD = 0
    PHRASE = 1

    def getType(string):
        lstring = string.lower();
        if not ' ' in lstring:
            return ContentType.WORD

        if len(lstring) < 3:
            return ContentType.PHRASE

        if lstring[0:3] in ('der', 'die', 'das'):
            return ContentType.WORD

        return ContentType.PHRASE



class Request:
    _type = None
    content = None
    note = None
    example = None

    def __init__(self, content, note=None, example=None):
        
        self._type = ContentType.getType(content)

        self.content = content
        self.note = note
        self.example = example

    def __repr__(self):
        result = {}
        result.update({"Word": self.content} if self._type == ContentType.WORD else {"Phrase": self.content})
        if self.note != None:
            result.update({"Note": self.note })
        if self.example != None:
            result.update({"Example": self.example})

        return repr(result)


