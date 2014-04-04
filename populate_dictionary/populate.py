from bs4 import BeautifulSoup
import urllib2
import sys


from cmd.models import Nodes
from flask import flash, render_template, request, redirect, url_for

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
        # return definition[0].text+'\n'
        defs = []
        i=1
        for found in definition:
           defs.append( i +": "+ found.text+'\n')
           i=i+1
        return defs
    except IndexError:
        return 'Sorry, no definition was found for ' + word + '.'


def fetch_sentence(word):
    u = "http://www.merriam-webster.com/dictionary/"+word
    try:
        req = urllib2.urlopen(u)
    except urllib2.HTTPError:
        return 'No definition found for ' + word + ', make sure you spelled it correctly.'
    define = req.read()
    soup = BeautifulSoup(define)
    definition = soup.find_all('li','always-visible')
    #definition = soup.find_all("div",attrs={"class":'sblk'})
    try:
        # return definition[0].text+'\n'
        # if you want to print multiple definitions
        defs = []
        i=1
        for found in definition:
           defs.append( i +": "+ found.text+'\n')
           i=i+1
        return defs
    except IndexError:
        return 'Sorry, no definition was found for ' + word + '.'



# from populate_dictionary import app

def index():
    query = Nodes.orderby(Nodes.id, desc=True).select()  # sort by created time
    results = query.execute()
    messages = results.fetchall()
    return render_template('template.html', nodes=messages)



def main():
    word = raw_input("Enter word");
    if word :
        message = Nodes.create(
            word=word, meaning=fetch_def(word), sentence= fetch_sentence(word), x =1, y=2, z = 3)
        if message is not None:  # ok
            flash(dict(type='success', content='New node created'))
        else:  # create failed
            flash(dict(type='error', content='Failed to create new node'))
    else:  # invalid input
        flash(dict(type='warning', content='Empty input'))
    return redirect(url_for('index'))


if __name__ == "__main__" :
    main()