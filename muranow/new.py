# -*- coding: utf-8

from read import readSource
import re

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


if __name__ == '__main__':
    sites = [
         'nowe_filmy\\jiro.htm',
         'nowe_filmy\\kropka.htm',
         'nowe_filmy\\nietykalni.htm',
         'nowe_filmy\\milosc.htm',
         'nowe_filmy\\bestia.htm',
         #'http://muranow.gutekfilm.pl/film.php?category=2800&id=c0c4cdb61205efa&page=1&type=current', # Jiro
         #'http://muranow.gutekfilm.pl/film.php?category=2800&id=f0a033a89d37695&page=1&type=current', # kropka
         #'http://muranow.gutekfilm.pl/film.php?category=2800&id=3c5cd7ea56a5b61&page=1&type=current', # Nietykalni
         #'http://muranow.gutekfilm.pl/film.php?category=2800&id=e42818047d0de21&page=1&type=current', # Milosc jezyk
         #'http://muranow.gutekfilm.pl/film.php?category=2800&id=14e5854da575ece&page=1&type=current', # Bestia z
    ]
    directors = [
        'David Gelb',
        'Dervis Zaim',
        'Olivier Nakache',
        'Eric Toledano',
        'lksen Basarır',
        'Coleman Francis',
    ]
    photographers = [
        'David Gelb',
        'Ercan Yılmaz',
        'Mathieu Vadepied',
        'Hayk Kirakosyan',
    ]
    screenwriters = [
        'Dervis Zaim',
        'Eric Toledano',
        'Olivier Nakache',
        'Mert Fırat',
        'lksen Basarır',
    ]
    countries = [
        'Japonia',
        'Turcja',
        'Turcja',
        'USA',
    ]
    times = [
        '81min',
        '85min',
        '112min',
        '98min',
        '53min',
    ]
    years = [
        '2011',
        '2008',
        '2011',
        '2009',
        '1961',
    ]

director = findPredecessor(sites, directors)
photograph = findPredecessor(sites, photographers)
screenwriter = findPredecessor(sites, screenwriters)
country = findPredecessor(sites, countries)
time = findPredecessor(sites, times)
year = findPredecessor(sites, years)


print 'Best director:', director
print 'Best photograph:', photograph
print 'Best screenwriter:', screenwriter
print 'Best country:', country
print 'Best time:', time
print 'Best year:', year


