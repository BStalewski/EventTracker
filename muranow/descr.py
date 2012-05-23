from descriptions import *
from findObject import commonPath, soupFromPath, findObject
import string

def prepareDescription(subSoup, des, elementsPaths):
    fullDescr = {}
    merged = mergeDescrPaths(des, elementsPaths)
    for d in merged:
        found, sep = checkMultiple(subSoup, d['path'])
        newDescr = {
            'key': d['key'],
            'path': d['path'],
            'keyVisible': checkKeyVisible(subSoup, d['path'], d['key']),
            'long': checkLong(subSoup, d['path']),
            'multiple': found
        }
        if newDescr['multiple']:
            newDescr['sep'] = sep
        #fullDescr.append(newDescr)
        fullDescr[d['key']] = newDescr

    return fullDescr

def mergeDescrPaths(descr, elementsPaths):
    merged = []
    pathsDict = {}
    for (i, d) in enumerate(descr):
        try:
            pathsDict[d['key']].append(elementsPaths[i])
        except KeyError:
            pathsDict[d['key']] = [elementsPaths[i]]
    
    for key, paths in pathsDict.iteritems():
        merged.append({
            'key': key,
            'path': reduce(commonPath, paths)
        })

    return merged

def checkKeyVisible(soup, path, key):
    subSoup = soupFromPath(soup, path)
    try:
        text = subSoup.text
    except:
        text = subSoup
    
    trimmedText = text.strip()
    return trimmedText.startswith(key)

def checkLong(soup, path):
    def bigLetterWord(word):
        for letter in word:
            if letter.isalpha():
                return letter.isupper()
        return False

    subSoup = soupFromPath(soup, path)
    try:
        text = subSoup.text
    except:
        text = subSoup

    words = text.split(' ')
    bigLetterWords = filter(bigLetterWord, words)
    return len(words) > 10 and len(bigLetterWords) < 0.3 * len(words)

def checkMultiple(soup, path):
    subSoup = soupFromPath(soup, path)
    try:
        text = subSoup.text
    except:
        text = subSoup
    
    words = text.split(' ')
    if len(words) == 1:
        return (False, None)

    if allLongWords(words):
        lastLetters = [w[-1] for w in words]
        found, seqLetter = findSequence(lastLetters)
    else:
        found, seqLetter = findSequence(words)

    return found, seqLetter

def checkSplit(soup, text, path):
    subSoup = soupFromPath(soup, path)
    isFound = subSoup.find(text=re.compile(text))
    if isFound:
        return False
    else:
        return True

def allLongWords(words):
    return all( [(len(w) > 2) for w in words] )

def findSequence(letters):
    separators = {}
    for (i, last) in enumerate(letters):
        try:
            separators[last].append(i)
        except:
            separators[last] = [i]

    for sep in separators:
        indexes =  separators[sep]
        if len(indexes) == 1:
            continue
        diffIndexes = range(len(indexes) - 1)
        diffs = [ (indexes[i+1] - indexes[i]) for i in diffIndexes ]
        if max(diffs) <= min(diffs) + 2:
            return (True, sep)
        
    return (False, None)


if __name__ == '__main__':
    '''
    paths, subSoup = findObject('filmy\\wstyd.htm', wstydDes)
    fullDescr = prepareDescription(subSoup, wstydDes, paths)
    for fd in fullDescr:
        print fd
    '''
    '''
    print '-' * 80
    paths, subSoup = findObject('filmy\\cuba_isla_of_music.htm', cubaDes)
    fullDescr = prepareDescription(subSoup, cubaDes, paths)
    for fd in fullDescr:
        print fd
    
    '''
    '''
    print '-' * 80
    paths, subSoup = findObject('filmy\\ostatnia_milosc_na_ziemi.htm', ostatniaDes)
    fullDescr = prepareDescription(subSoup, ostatniaDes, paths)
    for fd in fullDescr:
        print fd
    '''

    print '-' * 80
    paths, subSoup = findObject('filmy\\ostatnia_milosc_na_ziemi_strong.htm', ostatniaDes)
    fullDescr = prepareDescription(subSoup, ostatniaDes, paths)
    for fd in fullDescr:
        print fd
    
