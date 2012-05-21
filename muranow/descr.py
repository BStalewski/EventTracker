from findObject import commonPath, soupFromPath
import string

def prepareDescription(subSoup, des, elementsPaths):
    fullDescr = []
    merged = mergeDescrPaths(des, elementsPaths)
    for (i, d) in merged:
        newDescr = {
            'key': d['key'],
            'path': d['path'],
            'keyVisible': checkKeyVisible(subSoup, d['path'], d['key'],
            'long': checkLong(subSoup, d['path']),
            'multiple': checkMultiple
        }

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

    return text.startswith(key)

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
    return len(bigLetterWords) < len(words)

def checkMultiple(soup, path):
    subSoup = soupFromPath(soup, path)
    try:
        text = subSoup.text
    except:
        text = subSoup
    
    words = text.split(' ')
    if allWords(words):
        lastLetters = getLastLetters(words)
    else:
        checkBeetween

def allWords(words):
    return all([w.isalpha() for w in words])

def getLastLetters(words):
    return [w[-1] for w in words]
