import urllib
import os

def retrieve_information(word):
#	API_KEY = "de96c"
	API_KEY = "f3fd7"
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

def main():
    word = raw_input("enter the word: ")
    result = find_synonyms(word)
    print "------------------\n###  SYNONYMS  ###\n------------------"
    print "\n##################################\n".join("\n------------------\n".join(map(str,l)) for l in result)
    return



if __name__=="__main__":
    main()
