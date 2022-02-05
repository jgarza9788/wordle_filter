
import os,json,re,collections

directory = os.path.dirname(os.path.realpath(__file__))
wordfile = os.path.join(directory,'words.json')
letterfile = os.path.join(directory,'letters.json')

def load(path_to_file):
    try:
        with open(path_to_file,'r') as file:
            return json.load(file)
    except:
        print('file missing')
        return []

def filter_excluded(words,excluded):
    if excluded == None:
        return words

    result = []
    for w in words:
        keep = True
        for l in excluded:
            if l in w.upper():
                keep = False
        if keep:
            result.append(w)

    return result

def filter_included(words,included):
    if included == None:
        return words

    result = []
    for w in words:
        icount = 0 
        for l in included:
            if l in w.upper():
                icount += 1
        if icount == len(included):
            result.append(w)

    return result

def filter_wtt(words,included,limit=10):
    wcounter = collections.Counter()

    for w in words:
        for l in included:
            if l in w.upper():
                wcounter[w] += 1
    
    wcounter = dict(wcounter.most_common(limit))

    result = []
    for k in wcounter.keys():
        result.append({'word':k,'count':wcounter[k]})

    return result


def filter_kp(words,known_positions):
    if known_positions == None:
        return words

    result = []
    for w in words:
        if re.match(known_positions,w,flags=re.IGNORECASE):
            result.append(w)
        else:
            pass
    
    return result

def upperize(cluded):
    if len(cluded) > 0:
        return cluded.upper()
    else:
        return None



def main(excluded=None,included=None,known_positions=None):
    words = load(wordfile)
    letters = load(letterfile)

    words = filter_excluded(words,excluded)
    words = filter_included(words,included)
    words = filter_kp(words,known_positions)

    print(len(words))
    print(words)

    words = load(wordfile)
    testable_letters = letters
    testable_letters = filter_excluded(testable_letters,excluded)
    testable_letters = filter_excluded(testable_letters,included)
    testable_letters = filter_excluded(testable_letters,known_positions)
    testable_letters = ''.join(testable_letters)
    
    words_to_try = filter_wtt(words,testable_letters,10)

    print(testable_letters)
    print(*words_to_try,sep='\n')


if __name__ == "__main__":

    # a string of letters not included in the word
    excluded = 'gndhobicrms'
    excluded = upperize(excluded)
    print('excluded',excluded)

    # a string of letters included in the word
    included = 'a'
    included = upperize(included)
    print('included',included)

    # a string of the letters we know are in the correct position
    # use period for unknown positions 
    known_positions = '.LE.T'
    known_positions = upperize(known_positions)
    print('known_positions',known_positions)

    main(excluded,included,known_positions)

    #typal

