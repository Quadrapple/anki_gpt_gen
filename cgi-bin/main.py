from request import *
from requester import *
from cardcompiler import *
import json
import sys


requests = []

def elem(l, i):
    try:
        return l[i]
    except IndexError:
        return None

for line in sys.stdin:
    lineStripped = line.rstrip();
    entry = lineStripped.split(':')
    

    request = Request(elem(entry, 0), elem(entry, 1), elem(entry, 2))
    requests.append(request)

res, strRes = askMany(requests)
print(json.dumps(res))

convert(res)

