import json
import urllib
import math
import time
import random
import sys

from urllib import FancyURLopener

pwords = ["good", "nice", "excellent", "positive", "fortunate", "correct", "superior"]
nwords = ["bad", "nasty", "poor", "negative", "unfortunate", "wrong", "inferior"]

class MyOpener(FancyURLopener):
  version = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)'

myopener = MyOpener()

dictFile = open('socache.txt', 'r+').read()

if dictFile:
  asaDict = eval(dictFile)
else:
  asaDict = {'testentry':0}

print "asaDict: " + str(asaDict)

def cache(words):
  if words in asaDict:
    return asaDict[words]
  else:
    return False

def doQuery(query, key):
  url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
  search_response = myopener.open(url)
  search_results = search_response.read()
  results = json.loads(search_results)
  time.sleep(7 + random.random()*30)
  try:
    resultCount = float(results['responseData']['cursor']['estimatedResultCount'])
    if resultCount < 1:
      resultCount += .01
    asaDict[key] = resultCount
    dictFile = open('socache.txt', 'w')
    dictFile.write(str(asaDict))
    dictFile.close()
    return resultCount
  except:
    print results
    pauseDur = 7 + random.random()*1000
    print "sleeping for: %d seconds" % pauseDur
    time.sleep(pauseDur)
    return doQuery(query, key)

def getNumberHits(word):
  cachedValue = cache(word)
  if cachedValue:
    return cachedValue
  else:
    query = urllib.urlencode({'q': word + " -asdfasdfkj"})
    return doQuery(query, word)

def getNumberAround(word1, word2, nearness):
  cachedValue = cache(word1+word2+str(nearness))
  if cachedValue:
    return cachedValue
  else:
    query = urllib.urlencode({'q': word1 + " " "AROUND(" + str(nearness) + ")" + " " + word2})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
  return doQuery(query, word1+word2+str(nearness))
    

def pmi(word, pword, nword, nearness):
  hitsNearPword = getNumberAround(word, pword, nearness)
  hitsNearNword = getNumberAround(word, nword, nearness)
  pwordHits = getNumberHits(pword)
  nwordHits = getNumberHits(nword)
  print "aaaaaaa"
  print hitsNearPword
  print hitsNearNword
  print  pwordHits
  result = math.log((hitsNearPword*nwordHits)/(hitsNearNword*pwordHits), 2)
  return result

def sopmi(word, plist, nlist, nearness):
  so = 0
  print plist
  print nlist
  print nearness
  for pword, nword in zip(plist, nlist):
    so += pmi(word, pword, nword, nearness)
  so = so/len(pword)
  return so

def main():
  if (len(sys.argv) > 1):
    for word in sys.argv[1:]:
      print sys.argv[1:]
      print sopmi(word, pwords, nwords, 5)
  else:
    print sopmi("debate", pwords, nwords, 5)

if __name__ == "__main__":
    main()
