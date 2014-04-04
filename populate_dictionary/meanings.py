
from bs4 import BeautifulSoup
import urllib2
import sys

def fetch_def(word):
    u = "http://www.merriam-webster.com/dictionary/"+word
    try:
        req = urllib2.urlopen(u)
    except urllib2.HTTPError:
        return 'No definition found for ' + word + ', make sure you spelled it correctly.'
    define = req.read()
    soup = BeautifulSoup(define)
    definition = soup.find_all('span','ssens')
    #definition = soup.find_all("div",attrs={"class":'sblk'})
    try:
        return word+' -> '+definition[0].text+'\n'
        #if you want to print multiple definitions
        #defs = []
        #for found in definition:
        #    defs.append(word+' -> '+found.text+'\n')
        #return defs
    except IndexError:
        return 'Sorry, no definition was found for ' + word + '.'

def main():
    print("**************************************")
    print("WELCOME TO THE COMMAND LINE DICTIONARY")
    print("*********INPUT 'QUIT' TO EXIT*********")
    print("**************************************")
    print("\n")

    while True:
        print("What word would you like to define?")
        prompt = '> '
        word = raw_input(prompt)
        if word == 'QUIT':
            break
        print fetch_def(word)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for word in sys.argv[1:]:
            print fetch_def(word)
    else:
        main()
