# -*- coding: utf-8 -*-

from descriptions import *
from findObject import findObject
from descr import prepareDescription

def merge(descriptions):
    mergedDescription = []
    
    allKeys = set()
    for descr in descriptions:
        keys = descr.keys()
        allKeys = allKeys | set(keys)

    for key in allKeys:
        elementDescriptions = []
        for descr in descriptions:
            try:
                elementDescriptions.append(descr[key])
            except KeyError:
                pass

        optional = len(elementDescriptions) < len(descriptions)
        mergedDescription.append(mergeElementsDescritptions(elementDescriptions, optional))
    
    return mergedDescription

def descrKeys(descr):
    return [el['key'] for el in descr]

def mergeElementsDescritptions(elements, optional):
    mergedElement = elements[0]

    for element in elements[1:]:
        if mergedElement['key'] != element['key']:
            raise RuntimeError('Keys are different: %s vs %s' % (mergedElement['key'], element['key']))
        if mergedElement['long'] != element['long']:
            raise RuntimeError('Long parameters are different')

        mergedElement['keyVisible'] = mergedElement['keyVisible'] or element['keyVisible']
        mergedElement['multiple'] = mergedElement['multiple'] or element['multiple']
        if 'separator' in element:
            if element['separator'] not in mergedElement.get('separator', []):
                try:
                    mergedElement['separator'].append(element['separator'])
                except:
                    mergedElement['separator'] = [element['separator']]
        
        
        mergedElement['path'] = mergePaths(mergedElement['path'], element['path'])

    mergedElement['optional'] = optional

    return mergedElement
        
def mergePaths(path1, path2):
    mergedPath = []
    minLength = min(len(path1), len(path2))
    for i in range(minLength):
        p1 = path1[i]
        p2 = path2[i]
        name = p1[0] if p1[0] == p2[0] else '_'
        ind = p1[1] if p1[1] == p2[1] else '_'
        mergedPath.append((name, ind))

    return mergedPath

def selectElements(fullDescr, key, value):
    selectedElements = []
    for d in fullDescr:
        if d[key] == value:
            selectedElements.append(d)

    return selectedElements

if __name__ == '__main__':
    wstydPaths, wstydSubSoup = findObject('filmy\\wstyd.htm', wstydDes)
    wstydFullDescr = prepareDescription(wstydSubSoup, wstydDes, wstydPaths)

    cubaPaths, cubaSubSoup = findObject('filmy\\cuba_isla_of_music.htm', cubaDes)
    cubaFullDescr = prepareDescription(cubaSubSoup, cubaDes, cubaPaths)

    print wstydFullDescr[u'Reżyseria']
    print cubaFullDescr[u'Reżyseria']

    descriptions = [wstydFullDescr, cubaFullDescr]
    mergedDescription = merge(descriptions)
    for d in mergedDescription:
        print '------'
        for k, v in d.iteritems():
            print k, ':', v
        print '------'

