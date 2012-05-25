# -*- coding: utf-8

from read import readSource
import re
import os

def findPredecessor(sources, names):
    siteTexts = [readSource(source) for source in sources] 

    predecessors = {
        'unigram': {},
        'bigram': {},
        'trigram': {}
    }

    for (i, text) in enumerate(siteTexts):
        nohtmlText = re.sub('<[^<>]*>', ' ', text)
        plainText = re.sub('\s+', ' ', nohtmlText)

        print 'search site:', sources[i]
        for name in names:
            print 'search name:', name
            nameIndexes = findIndexes(plainText, name)

            for index in nameIndexes:
                partialText = plainText[:index]
                words = findThreeLastWords(predecessors, partialText)

                if words[0][-1] == ',':
                    textWithOmitted = omitPrevious(partialText, 4)
                    words = findThreeLastWords(predecessors, textWithOmitted)
                    for word in words:
                        for key in predecessors.iterkeys():
                            if word in predecessors[key]:
                                predecessors[key][word] += 1
                else:
                    fillPredecessors(predecessors, words)

    
    bestName = chooseBestName(predecessors)
    showPredecessors(predecessors)
    return cleanName(bestName)

def fillPredecessors(predecessors, words):
    unigram = words[0]
    bigram =  words[1] + ' ' + unigram
    trigram = words[2] + ' ' + bigram

    try:
        predecessors['unigram'][unigram] += 1
    except:
        predecessors['unigram'][unigram] = 1
    try:
        predecessors['bigram'][bigram] += 1
    except:
        predecessors['bigram'][bigram] = 1
    try:
        predecessors['trigram'][trigram] += 1
    except:
        predecessors['trigram'][trigram] = 1

def omitPrevious(text, maxCheck):
    checksRemaining = maxCheck
    lastSpace = len(text) - 2
    lastGoodStop = len(text) - 1
    while checksRemaining > 0:
        lastSpace = text.rfind(' ', 0, lastSpace - 1)
        checksRemaining -= 1
        if text[lastSpace - 1] == ',':
            checksRemaining = maxCheck
            lastGoodStop = lastSpace - 1

    preLastGoodStop = text.rfind(' ', 0, lastGoodStop)

    return text[:preLastGoodStop]

def findIndexes(text, searchText):
    indexes = []
    index = text.find(searchText)
    while index != -1:
        indexes.append(index)
        index = text.find(searchText, index + 1)

    return indexes

def findThreeLastWords(predecessors, text):
    regexp = re.compile(r'(?P<threeBefore>[^\s]+)\s(?P<twoBefore>[^\s]+)\s(?P<oneBefore>[^\s]+)\s*$')
    
    lastWords = regexp.search(text)
    if lastWords is None:
        return None

    first = lastWords.group('oneBefore')
    second = lastWords.group('twoBefore')
    third = lastWords.group('threeBefore')
    words = [first, second, third]

    return words

def chooseBestName(predecessors):
    bestUnigram = countNgrams(predecessors['unigram'])
    bestBigram = countNgrams(predecessors['bigram'])
    bestTrigram = countNgrams(predecessors['trigram'])

    if bestUnigram['total'] < 3:
        return None

    bestName = None
    if bestUnigram['bestCount'] > 0.5 or (bestUnigram['bestCount'] > 2*bestUnigram['secondCount']):
        bestName = bestUnigram['ngram']

    if bestBigram['bestCount'] > 0.3 and 1.5 * bestBigram['bestCount'] > bestUnigram['bestCount']:
        bestName = bestBigram['ngram']

    if bestTrigram['bestCount'] > 0.25 and 1.5 * bestTrigram['bestCount'] > bestBigram['bestCount']\
        and 3 * bestTrigram['bestCount'] > bestUnigram['bestCount']:
        bestName = bestTrigram['ngram']

    print bestUnigram
    print bestBigram
    print bestTrigram

    return bestName
        

def countNgrams(ngrams):
    total = sum(ngrams.itervalues())

    pairs = sorted( zip(ngrams.itervalues(), ngrams.iterkeys()) )
    bestCount, bestNgram = pairs[-1]
    try:
        secondBestCount = pairs[-2][0]
    except IndexError:
        secondBestCount = 0

    return {
        'ngram': bestNgram,
        'bestCount': float(bestCount) / total,
        'secondCount': float(secondBestCount) / total,
        'total': total
    }

def showPredecessors(predecessors):
    for gram, value in predecessors.iteritems():
        print '----------------'
        print gram
        print '----------------'
        for k,v in value.iteritems():
            print '*' * v, k

def cleanName(name):
    cleanedName = name.strip().strip(',.:')
    return cleanedName

def testLearning():
    sites = [
         'jiro.htm',
         'kropka.htm',
         'nietykalni.htm',
         'milosc.htm',
         'bestia.htm',
         #'http://muranow.gutekfilm.pl/film.php?category=2800&id=c0c4cdb61205efa&page=1&type=current', # Jiro
         #'http://muranow.gutekfilm.pl/film.php?category=2800&id=f0a033a89d37695&page=1&type=current', # kropka
         #'http://muranow.gutekfilm.pl/film.php?category=2800&id=3c5cd7ea56a5b61&page=1&type=current', # Nietykalni
         #'http://muranow.gutekfilm.pl/film.php?category=2800&id=e42818047d0de21&page=1&type=current', # Milosc jezyk
         #'http://muranow.gutekfilm.pl/film.php?category=2800&id=14e5854da575ece&page=1&type=current', # Bestia z
    ]
    sitesPaths = [os.path.join('nowe_filmy', 'learn', site) for site in sites]
    searchedNames = {
        'directors': [
            'David Gelb',
            'Dervis Zaim',
            'Olivier Nakache',
            'Eric Toledano',
            'lksen Basarır',
            'Coleman Francis',
        ],
        'photographers': [
            'David Gelb',
            'Ercan Yılmaz',
            'Mathieu Vadepied',
            'Hayk Kirakosyan',
        ],
        'screenwriters': [
            'Dervis Zaim',
            'Eric Toledano',
            'Olivier Nakache',
            'Mert Fırat',
            'lksen Basarır',
        ],
        'countries': [
            'Japonia',
            'Turcja',
            'Turcja',
            'USA',
        ],
        'times': [
            '81min',
            '85min',
            '112min',
            '98min',
            '53min',
        ],
        'years': [
            '2011',
            '2008',
            '2011',
            '2009',
            '1961',
        ]
    }

    learnResults = learn(sitesPaths, searchedNames)
    print '*' * 80

    print 'Best director:', learnResults['directors']
    print 'Best photograph:', learnResults['photographers']
    print 'Best screenwriter:', learnResults['screenwriters']
    print 'Best country:', learnResults['countries']
    print 'Best time:', learnResults['times']
    print 'Best year:', learnResults['years']

    return learnResults

def learn(sites, searchedNames):
    print 'Przeprowadzenie uczenia na stronach:'
    for site in sites:
        print site,
    print ''

    precedingNames = {}

    for nameType, names in searchedNames.iteritems():
        print 'Szukanie dla klasy:', nameType
        print 'Z wartosci:,'
        for name in names:
            print name,
        print ''
        
        proposedName = findPredecessor(sites, names)
        if proposedName is None:
            print 'Nie mozna bylo wybrac zadnej nazwy.'
        else:
            print 'Nazwa to:', proposedName
            precedingNames[nameType] = {
                'name': proposedName,
                'start': findCommonStart(names),
                'end': findCommonEnd(names)
            }

    return precedingNames

def findCommonStart(words, reverse=False):
    if len(words) < 4:
        return None

    for word in words:
        if len(word) < 2:
            return None

    commonText = ''
    try:
        for (i, w) in enumerate(words):
            ind = i if not reverse else (-i)
            letters = [w[ind] for w in words]
            if max(letters) == min(letters):
                commonText = commonText + letters[0] if not reverse else letters[0] + commonText
    except IndexError:
        pass

    return commonText if len(commonText) > 1 else None

def findCommonEnd(words):
    return findCommonStart(words, reverse=True)

        
def test(sites, keywords):
    sitesPaths = [os.path.join('nowe_filmy', 'test', site) for site in sites]

    siteTexts = [readSource(site) for site in sitesPaths] 

    print '*' * 80
    print 'TEST'
    
    filmDescriptions = {}
    newKeywords = []

    for (i, text) in enumerate(siteTexts):
        nohtmlText = re.sub('<[^<>]*>', ' ', text)
        plainText = re.sub('\s+', ' ', nohtmlText)

        print 'search site:', sites[i]
        filmName = sites[i][:-4]  # cut off .htm
        filmDescriptions[filmName] = {}
        '''
        newKeywords = []
        for keyword in keywords:
            nameIndexes = findIndexes(plainText, keyword)
            for index in nameIndexes:
                partialText = omitKeyword(plainText, index, keyword)
                names, foundKeywords = getNames(partialText, 3, keywords)
                filmDescriptions[filmName][keyword] = names
            newKeywords.append(foundKeywords)
        '''
        foundKeywords = fillDescription(filmDescriptions[filmName], plainText, keywords + newKeywords)
        while foundKeywords != []:
            newKeywords += foundKeywords
            foundKeywords = fillDescription(filmDescriptions[filmName], plainText, keywords + newKeywords)

    print 'New keywords:'
    for k in newKeywords:
        print k,
    print ''

    return filmDescriptions

def fillDescription(description, plainText, keywordsInfo):
    newKeywordsInfo = []
    for keyword in keywordsInfo:
        nameIndexes = findIndexes(plainText, keyword['name'])
        for index in nameIndexes:
            partialText = omitKeyword(plainText, index, keyword['name'])
            names, foundKeywords = getNames(partialText, 3, keywordsInfo, keyword)
            description[keyword['name']] = names
            if foundKeywords != []:
                print '1', newKeywordsInfo
                newKeywordsInfo += foundKeywords
                print '2', newKeywordsInfo

    return newKeywordsInfo

def omitKeyword(text, cutStartIndex, keyword):
    cutIndex = cutStartIndex + len(keyword)
    while text[cutIndex] in [':', ' ']:
        cutIndex += 1

    return text[cutIndex:]

def getNames(text, maxCheck, keywords, keyword):
    words = text.split(' ')
    checksRemaining = maxCheck

    start = keyword['start']
    end = keyword['end']

    isNumberType = checkNumberType(words[0])
    names = []
    startNameIndex = 0
    endNameIndex = 0
    newKeywords = []
    keywordNames = [k['name'] for k in keywords]
    while checksRemaining > 0:
        if isNumberType != checkNumberType(words[endNameIndex]):
            newName = makeName( words[startNameIndex:endNameIndex] )
            if newName not in names:
                names.append(newName)
            break

        if checkPoles(words[startNameIndex:endNameIndex + 1], start, end):
            newName = makeName( words[startNameIndex:endNameIndex + 1] )
            names.append(newName)
            checksRemaining = maxCheck
        elif words[endNameIndex][-1] == ',':
            newName = makeName( words[startNameIndex:endNameIndex + 1] )
            newName = newName[:-1] #  cut off ','
            names.append(newName)
            startNameIndex = endNameIndex + 1
            checksRemaining = maxCheck
        elif words[endNameIndex][-1] == ':':
            if makeName( words[endNameIndex: endNameIndex + 1] ) in keywordNames:
                if startNameIndex != endNameIndex - 1:
                    newName = makeName( words[startNameIndex: endNameIndex] )
                    names.append(newName)
            elif makeName( words[endNameIndex - 1: endNameIndex + 1] ) in keywordNames:
                if startNameIndex != endNameIndex - 2:
                    newName = makeName( words[startNameIndex: endNameIndex - 1] )
                    names.append(newName)
            else:
                newName = makeName( words[startNameIndex: endNameIndex] )
                names.append(newName)
                newKey = words[endNameIndex][:-1]
                print 'new key:', newKey
                newKeyDescr = {
                    'name': newKey,
                    'start': None,
                    'end': None
                }
                newKeywords.append(newKeyDescr)
            break

        endNameIndex += 1
        checksRemaining -= 1

    return names, newKeywords

def makeName(words):
    name = ' '.join(words)
    return name[:-1] if name[-1] in [',', ':'] else name

def checkNumberType(word):
    try:
        int(word)
        return True
    except:
        return False

def checkPoles(words, start, end):
    if start is None and end is None:
        return False

    correct = True
    text = makeName(words)
    if start is not None:
        correct = text.startswith(start)
    if end is not None:
        correct = correct and text.endswith(end)

    return correct

if __name__ == '__main__':
    learnResults = testLearning()
    testSites = ['wichrowe.htm', 'ojczyzna.htm', 'zazdrosc.htm']
    
    labels = learnResults.values()
    testResults = test(testSites, labels)
    for filmName, names in testResults.iteritems():
        print 'Film:', filmName
        for name, values in names.iteritems():
            if values != []:
                print name, ':',
                for value in values:
                    print value,
                print ''

