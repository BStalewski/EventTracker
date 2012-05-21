# -*- coding: UTF-8 -*-

import re
from BeautifulSoup import BeautifulSoup as bs
from read import readSource 

des = [
    {'key': 'Tytuł', 'value': 'Wstyd'},
    {'key': 'Scenariusz', 'value': 'Steve McQueen'},
    {'key': 'Scenariusz', 'value': 'Abi Morgan'},
    {'key': 'Zdjęcia', 'value': 'Sean Bobbitt'},
    {'key': 'Obsada', 'value': 'Wielka Brytania'},
    {'key': 'Rok', 'value': '2011'},
    {'key': 'Czas trwania', 'value': '101min'},
    {'key': 'Opis', 'value': 'Brandon, 30-latek, atrakcyjny singiel z Nowego Jorku nie potrafi zapanować nad swym życiem erotycznym. Sytuacja jeszcze bardziej wymyka się spod kontroli, kiedy niespodziewanie wprowadza się do niego siostra.'}
]

des = [
    {'key': 'Tytuł', 'value': 'Wstyd'},
    {'key': 'Scenariusz', 'value': 'Steve McQueen'},
    {'key': 'Scenariusz', 'value': 'Abi Morgan'},
    {'key': 'Zdjęcia', 'value': 'Sean Bobbitt'},
    {'key': 'Obsada', 'value': 'Wielka Brytania'},
    {'key': 'Rok', 'value': '2011'},
    {'key': 'Czas trwania', 'value': '101min'},
    {'key': 'Opis', 'value': 'Brandon, 30-latek'}
]


# debug purpose
def getSoup(name):
    content = readSource(name)
    soup = bs(content)
    return soup

def findObject(name, descr):
    content = readSource(name)
    soup = bs(content)
    try:
        elementsPaths, bestPath = findPath(soup, descr)
    except IndexError:
        return None

    return elementsPaths, soupFromPath(soup, bestPath)

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
    initPaths = generatePaths(soup, descr[0]['value'])
    elementsPaths = [[]]
    #print 'initPaths'
    #print initPaths
    for descrEl in descr[1:]:
        for i in range(len(initPaths)):
            newPaths = generatePaths(soup, descrEl['value'])
            #print 'newPaths', descrEl['value']
            #print newPaths
            nr, initPaths[i] = bestMatchPath(initPaths[i], newPaths)
            elementsPaths.append(newPaths[nr])
        #print 'initPaths'
        #print initPaths
    nr, pathsSorted = sorted(enumerate(initPaths), key=lambda p: len(p[1]))[-1]
    elementsPaths[0] = generatePaths(soup, descr[0]['value'])[nr]

    return elementsPaths, pathsSorted

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

def generatePaths(soup, text):
    paths = []
    soupElements = soup.findAll(text=re.compile(text))
    possiblePaths = [getPath(el) for el in soupElements]
    return filter(lambda p: pathInteresting(p), possiblePaths)

def pathInteresting(path):
    for (name, i) in path:
        if name == 'head':
            return False
    return True

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
    print findObject('filmy\\wstyd.htm', des)
