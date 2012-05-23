# -*- coding: utf-8 -*-
from descriptions import *

from BeautifulSoup import BeautifulSoup as bs
from read import readSource 
from findObject import findPath, findObject, soupFromPath
from descr import prepareDescription
from merge import merge, selectElements

def getData(subSoup, fullDescr):
    obligatoryElements = selectElements(fullDescr, 'optional', False)
    usedPaths = []
    allObligatory = True
    data = []
    for element in obligatoryElements:
        elDescr, inSoup, usedPaths = elementInSoup(subSoup, element, usedPaths)
        if not inSoup:
            allObligatory = False
            continue
        data.append(elDescr)

    data.append( visitRestTree(fullDescr, subSoup, usedPaths) )
    
    return data

def elementInSoup(subSoup, element, usedPaths):
    print 'XXXXXXXXXXXXXXXXXXXXXX'
    print element
    subPath = getPath(subSoup)
    if element['keyVisible'] == True:
        findSoup = subSoup.find(text=re.compile(element['key']))
        if findSoup is None:
            return None, False, usedPaths
        findPath = getPath(findSoup)[:len(subPath)]
        if matchPath(element['path'], findPath):
            return {
                'key': element['key'],
                'value': findSoup.text
            }, True, usedPaths + findPath
        else:
            print 'Sciezki sie nie zgadzaja'
            return None, False, usedPaths
    
    else:
        



    return ({'key': u'Reżyseria', 'value': 'Al Bundy'}, True, usedPaths)

def visitRestTree(fullDescr, subSoup, usedPaths):
    return ({'key': u'Reżyseria', 'value': 'Al Bundy'}, subSoup, usedPaths)

def retrieveFrom(name, fullDescr):
    content = readSource(name)
    soup = bs(content)
    keywords = getKeywords(fullDescr)
    usedKeywordPaths, keywordsBestPath = keywordsPath(soup, keywords)

    shift = getBestPathShift(fullDescr, keywordsBestPath, usedKeywordPaths)

    bestPath = keywordsBestPath
    for i in range(shift):
        bestPath.pop()

    return bestPath

def getKeywords(fullDescr):
    keywords = []
    for el in fullDescr:
        if el['keyVisible']:
            keywords.append(el['key'])

    return keywords

def keywordsPath(soup, keywords):
    descrEl = []
    for (i, keyword) in enumerate(keywords):
        descrEl.append({
            'key': '%d_____' % i,
            'value': keyword
        })

    elementPaths, bestPath = findPath(soup, descrEl)

    usedKeywordsPaths = {}
    for (i, el) in enumerate(descrEl):
        if elementPaths[i] != []:
            usedKeywordsPaths[keywords[i]] = elementPaths[i]
    
    return (usedKeywordsPaths, bestPath)

def getBestPathShift(fullDescr, keywordsBestPath, keywordsPaths):
    keywords = keywordsPaths.keys()
    descrPaths = [descr['path'] for descr in fullDescr if descr['key'] in keywordsPaths]
    matchingPath = reduce(matchPath, descrPaths)
    
    print 'mp:', matchingPath
    cutPath = cutAllMatch(matchingPath)
    shift = len(cutPath) - 1
    print 'Matching path shift =', shift
    return shift

def matchPath(path1, path2, strict=False):
    minLength = min(len(path1), len(path2))
    matchingPath = []
    for i in range(minLength):
        p1 = path1[i]
        p2 = path2[i]
        nameCheck = check(p1[0], p2[0], strict)
        indCheck = check(p1[1], p2[1], strict)
        if not nameCheck[0] or not indCheck[0]:
            break
        matchingPath.append((nameCheck[1], indCheck[1]))

    return matchingPath

def cutAllMatch(path):
    pathCopy = path[:]
    while len(pathCopy) > 0 and pathCopy[-1][1] == '_':
        pathCopy.pop()

    return pathCopy


def check(x1, x2, strict=False):
    if strict:
        return (x1 == x2, x1)
    else:
        if x1 == '_' or x2 == '_':
            return (True, '_')
        else:
            return (x1 == x2, x1)



if __name__ == '__main__':
    wstydPaths, wstydSubSoup = findObject('filmy\\wstyd.htm', wstydDes)
    wstydFullDescr = prepareDescription(wstydSubSoup, wstydDes, wstydPaths)

    #cubaPaths, cubaSubSoup = findObject('filmy\\cuba_isla_of_music.htm', cubaDes)
    #cubaFullDescr = prepareDescription(cubaSubSoup, cubaDes, cubaPaths)

    ostatniaPaths, ostatniaSubSoup = findObject('filmy\\ostatnia_milosc_na_ziemi.htm', ostatniaDes)
    ostatniaFullDescr = prepareDescription(ostatniaSubSoup, ostatniaDes, ostatniaPaths)

    descriptions = [wstydFullDescr, ostatniaFullDescr]
    mergedDescription = merge(descriptions)

    for d in mergedDescription:
        print '------'
        for k, v in d.iteritems():
            print k, ':', v
        print '------'

    print '--------------'
    retrievedPath = retrieveFrom('filmy\\zapiski.htm', mergedDescription)
    print retrievedPath
    cnt = readSource('filmy\\zapiski.htm')
    soup = bs(cnt)
    subSoup = soupFromPath(soup, retrievedPath)

    print 'get data'
    print getData(subSoup, mergedDescription)
