import urllib
import os

def retrieve_information(word):
	API_KEY = "de96c"
	action = "/thesaurus/" #Looks for the synonym of the word
	url = "http://api.wordreference.com/" + API_KEY + action + word
	try:
		htmlurl = urllib.urlopen(url)
	except:
		print "Not able to open the URL (maybe it's an API problem or the URL has been renamed"
		raise
	try:
		auxFile = open('auxFile.txt', 'w')
		auxFile.write(htmlurl.read())
		htmlurl.close()
		auxFile.close()
	except:
		print "Not able to create the auxFile to save the results"
		raise

def middle_word(sentence, first, second, lastWord):
	'''
	Given a sentence and two characters/words to look at, it returns
	the word in the middle
	'''
	try:
		beginning = sentence.index(first, lastWord) + len(first)
		ending = sentence.index(second, beginning)
		return (sentence[beginning:ending], ending)
	except ValueError:
		return ("", 0)

def finding_words():
	i = 0 #Numbers of sublists created
	finalsynonyms = []
	lastWord = 0
	finalsynonyms.append([])
	try:
		auxFile = open('auxFile.txt', 'r')
	except:
		print "Not able to open auxFile (did you delete it?)"
		raise
	midword = middle_word(auxFile.read(), 'title="">', '<', lastWord)
	auxFile = open('auxFile.txt', 'r')
	#we look the different meanings the world has
	meaning = middle_word(auxFile.read(), '/i>', '/b>', midword[1])
	while midword[0] != "":
		finalsynonyms[i].append(midword[0])
		lastWord = midword[1]
		if (meaning[1] < midword[1] and meaning[1] != 0):
			#if the word changes the meaning, creates a new list and puts the synonyms inside of it
			auxFile = open('auxFile.txt', 'r')
			meaning = middle_word(auxFile.read(), '/i>', '/b>', lastWord)
			finalsynonyms.append([])
			i = i+1
		auxFile = open('auxFile.txt', 'r')
		midword = middle_word(auxFile.read(), 'title="">', '<', lastWord)
	try:
		os.remove("auxFile.txt")
	except:
		print "Not able to delete the file (did you delete it?)"
		raise
	return finalsynonyms

def find_synonyms(word):
	retrieve_information(word)
	synonyms = finding_words()
	return synonyms

def intersect(a, b):
     return list(set(a) & set(b))

def main():
    word1 = raw_input("enter first word: ")
    word2 = raw_input("enter second word: ")
    result1 = find_synonyms(word1)
    result2 = find_synonyms(word2)
    print "------------------\n###  "+ word1 +"  ###\n------------------"
    print "\n".join(", ".join(map(str,l)) for l in result1)
    print "------------------\n###  "+ word2 +"  ###\n------------------"
    print "\n".join(", ".join(map(str,l)) for l in result2)
    list1 = [item for sublist in result1 for item in sublist]
    list2 = [item for sublist in result2 for item in sublist]
    links = intersect(list1, list2)
    print "------------------\n###  LINKS  ###\n------------------"
    print "\n##################################\n".join(map(str,links))
    return



if __name__=="__main__":
    main()
