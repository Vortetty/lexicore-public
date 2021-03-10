import re
import itertools
import operator

# https://stackoverflow.com/a/16448506
def createSubstrings(s, k):
    for i in range(0, len(s) - k):
        yield s[i:i+k]

# https://stackoverflow.com/a/16448575
def commonSubstrings(a, b, k):
  substrs = set(a[i:i+k] for i in range(len(a)-k+1))
  for substr in (b[i:i+k] for i in range(len(b)-k+1)):
    if substr in substrs:
      return substr

def compress(string, iters=1000, debug=False):
    replaces = []
    origstring = string

    i = 0x20
    itersdone = 0

    for x in range(iters):
        try:
            counts = []

            for y in sum(((list(createSubstrings(string, i)), print("Thing:", i))[0] for i in range(2, 21)), []):
                counts.append(
                    [
                        string.count(y),
                        y
                    ]
                )

            counts.sort(key=lambda x:(~len(x[1]), x[0]), reverse=True)
            counts = list(k for k,_ in itertools.groupby(list(k if k[0] > 3 else [0, ""] for k,_ in itertools.groupby(counts))))
            
            while chr(i) in string:
                i += 1
            
            tempString = string.replace(counts[0][1], chr(i))
            if len(tempString) < len(string):
                replaces.append([counts[0][1], chr(i)])
                print(counts[0][1], "->", chr(i), f"({i})", counts, "\n") if debug else None
                string = tempString
            else:
                break
        except:
            itersdone = x
            break

    return string, origstring, replaces, len(string)/len(origstring)

def decompress(string, replaces):
    for i in reversed(replaces):
        string = string.replace(i[1], i[0])
    return string