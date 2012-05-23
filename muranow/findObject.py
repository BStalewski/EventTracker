# -*- coding: UTF-8 -*-

import re
from BeautifulSoup import BeautifulSoup as bs
from read import readSource 

from descriptions import *


# debug purpose
def getSoup(name):
    content = readSource(name)
    soup = bs(content)
    return soup

def findObject(name, descr):
    '''Try to find object on source identified by name (url of file name) using
    description descr. If object can be found, returns tuple containing paths
    to object elements and html subtree with this object, otherwise returns None.'''
    content = readSource(name)
    soup = bs(content)

    try:
        elementsFullPaths, bestPath = findPath(soup, descr)
        cutSize = len(bestPath) - 1
        subPaths = [path[cutSize:] for path in elementsFullPaths]
    except IndexError:
        return None

    return subPaths, soupFromPath(soup, bestPath)

def soupFromPath(soup, path):
    subSoup = soup
    for p in path[1:]:
        ind = 0
        remaining = p[1]
        sibling = subSoup.contents[ind]
        while remaining > 0 or not importantElement(sibling):
            if importantElement(sibling):
                remaining -= 1
            ind += 1
            sibling = subSoup.contents[ind]

        subSoup = sibling

    return subSoup

def findPath(soup, descr):
    initPaths = generatePaths(soup, descr[0]['value'], descr[0]['key'], descr[0].get('class'))
    initPathsCopy = initPaths[:]
    elementsPaths = [[]]
    #print 'initPaths'
    #print initPaths
    for descrEl in descr[1:]:
        for i in range(len(initPaths)):
            cls = descrEl.get('class')
            newPaths = generatePaths(soup, descrEl['value'], descrEl['key'], cls)
            #print 'newPaths', descrEl['key'], descrEl['value']
            #print newPaths
            try:
                nr, tmpPaths = bestMatchPath(initPaths[i], newPaths)
            except:
                elementsPaths.append(None)
            else:
                nr, initPaths[i] = bestMatchPath(initPaths[i], newPaths)
                elementsPaths.append(newPaths[nr])
        #print 'initPaths'
        #print initPaths
    if initPaths == []:
        return [], None

    bestNr, bestPath = sorted(enumerate(initPaths), key=lambda p: len(p[1]))[-1]
    elementsPaths[0] = initPathsCopy[bestNr]

    return elementsPaths, bestPath

def bestMatchPath(path, newPaths):
    mergedPaths = []
    for p in newPaths:
        mergedPaths.append(commonPath(path, p))

    sortedPaths = sorted(enumerate(mergedPaths), key=lambda p: len(p[1]))
    return sortedPaths[-1]

def commonPath(path1, path2):
    minLength = min(len(path1), len(path2))
    commonInd = 0
    for i in range(minLength):
        name1, ind1 = path1[i]
        name2, ind2 = path2[i]
        if name1 != name2 or ind1 != ind2:
            break
        commonInd += 1

    return path1[:commonInd] if commonInd > 0 else []

def generatePaths(soup, text, addText=None, cls=None):
    paths = []
    print text
    print repr(text)
    soupElements = soup.findAll(text=re.compile(text))
    if cls:
        soupElements = filterWithClass(soupElements, cls)

    possiblePaths = [getPath(el) for el in soupElements]
    possiblePaths = filter(lambda p: pathInteresting(p), possiblePaths)

    if addText:
        addElements = soup.findAll(text=re.compile(addText))
        addPossiblePaths = [getPath(el) for el in addElements]
        possiblePathsWithAdd = filter(lambda p: p in addPossiblePaths, possiblePaths)
        if len(possiblePathsWithAdd) > 0:
            possiblePaths = possiblePathsWithAdd

    if possiblePaths == [] and len(text.split()) > 1:
        print 'pp', text
        possiblePaths = getSplitTextPath(soup, text)

    return possiblePaths

def pathInteresting(path):
    for (name, i) in path:
        if name == 'head':
            return False
    return True

def filterWithClass(elements, cls):
    filtered = []
    for el in elements:
        try:
            if el.parent['class'] == cls:
                filtered.append(el)
        except KeyError:
            continue
    return filtered

def getSplitTextPath(soup, text):
    # key jest taki, zeby nie byl znaleziony na stronie,
    splitText = []
    for (i, t) in enumerate(text.split()):
        splitText.append({
            'value': t,
            'key': '%d__' % i
        })

    splitText = [{'value': t, 'key': ''} for t in text.split()]
    wordsFullPaths, bestPath = findPath(soup, splitText)
    print 'wFP:', wordsFullPaths
    print 'bP:', bestPath

    cutEnd = len(bestPath)
    splitStart = wordsFullPaths[0][cutEnd][1]
    splitEnd = wordsFullPaths[0][cutEnd][1]
    for path in wordsFullPaths:
        ind = path[cutEnd][1]
        splitStart = min(splitStart, ind)
        splitEnd = max(splitEnd, ind)

    subtreeTextPaths = [bestPath + [('', i)] for i in range(splitStart, splitEnd+1)] 
    subtreeElements = [soupFromPath(soup, path) for path in subtreeTextPaths]
    subtreeTextSplit = [subtreeContent(element) for element in subtreeElements]
    subtreeText = ' '.join([])
    subtreeWords = subtreeText.split()
    for (i, w) in enumerate(subtreeWords):
        if w != splitText[i]:
            print 'Rozne w i =', i
            return []

    return [bestPath]

def subtreeContent(element):
    try:
        subtreeText = element.text
    except:
        subtreeText = element
    else:
        for child in element.contents:
            subtreeText += subtreeContent(child)

    return subtreeText

def getPath(element):
    path = []
    tmpEl = element
    while tmpEl is not None:
        ind = 0
        sibling = tmpEl.previousSibling 
        while sibling is not None:
            if importantElement(sibling):
                ind += 1
            sibling = sibling.previousSibling
        try:
            name = tmpEl.name
        except:
            name = ''
        path.append((name, ind))
        tmpEl = tmpEl.parent

    path.reverse()
    return path

def importantElement(element, split=False):
    try:
        name = element.name
    except:
        # NavigableString
        return not element.isspace() and element != u''

    if split:
        return name not in ['br', 'hr', 'strong', 'bold']
    else:
        return name not in ['br', 'hr']


if __name__ == '__main__':
    print findObject('filmy\\wstyd.htm', wstydDes)

