# coding=utf8
from bs4 import BeautifulSoup
import urllib
import os
import urllib2
import sys
from datetime import datetime

from populate_dictionary import app
from populate_dictionary.models import Nodes, Edges

from flask import flash, render_template, request, redirect, url_for



def fetch_def(word):
    u = "http://www.merriam-webster.com/dictionary/"+word
    try:
        req = urllib2.urlopen(u)
    except urllib2.HTTPError:
        return None
    define = req.read()
    soup = BeautifulSoup(define)
    definition = soup.find_all('span','ssens')
    try:
        defs = []
        i=1
        for found in definition:
           defs.append( str(i) + found.text)
           i=i+1
        return "\n \n".join(defs)
    except IndexError:
        return None


def fetch_sentence(word):
    u = "http://www.merriam-webster.com/dictionary/"+word
    try:
        req = urllib2.urlopen(u)
    except urllib2.HTTPError:
        return None
    define = req.read()
    soup = BeautifulSoup(define)
    definition = soup.find_all('li','always-visible')
    try:
        defs = []
        i=1
        for found in definition:
           defs.append( str(i) +": "+ found.text)
           i=i+1
        return "\n \n".join(defs)
    except IndexError:
        return None

# FIND SYNONYMS #

def retrieve_information(word):
#   API_KEY = "de96c"
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

def get_synonyms(word):
    retrieve_information(word)
    synonyms = finding_words()
    result = [item for sublist in synonyms for item in sublist]
    return result

def populate_synonyms(words, id):
    i=0
    for word in words:
        if word :
            query = Nodes.where(Nodes.word.like(word)).select()
            results = query.execute()

            count = results.count
            if count > 0 :
                for node in results.fetchall():
                    Edges.create(source=id,dest=node.id) 
                continue

            meaning=fetch_def(word)
            if meaning == None :
                # flash(dict(type='warning', content='word not found'))
                continue
            sentence = fetch_sentence(word)

            message = Nodes.create(
                word=word, meaning=meaning, sentence=sentence, x =1, y=2, z = 3)
            Edges.create(source=id,dest=message.id)
            i=i+1
            if i > 5:
                break
    return


@app.route('/', methods=['GET'])
def index():
    query = Nodes.limit(2, offset=1).orderby(Nodes.id, desc=True).select()  # sort by created time
    results = query.execute()
    messages = results.fetchall()
    return render_template('template.html', nodes=messages)

@app.route('/search', methods=['POST'])
def search():
    word = request.form['search_word']
    query = Nodes.where(Nodes.word.like('%'+word+'%')).select()
    # query = Nodes.orderby(Nodes.id, desc=True).select()  # sort by created time
    results = query.execute()
    messages = results.fetchall()
    return render_template('template.html', nodes=messages)

@app.route('/word/<word>')
def word(word):
    node = Nodes.findone(word=word)
    # print node.id
    results = Nodes.where(Nodes.id._in(Edges.where(Edges.source==node.id).distinct().select(Edges.dest))).select().execute()
    messages = results.fetchall()
    results = Nodes.where(Nodes.id==node.id).select().execute()
    messages1 = results.fetchall()
    # print type(messages)
    # print results.fetchone().id
    return render_template('template.html', nodes=messages, nodes1=messages1)

@app.route('/create', methods=['POST'])
def create():
    word = request.form['word']

    query = Nodes.where(Nodes.word.like(word)).select()
    results = query.execute()
    count = results.count

    if count > 0 :
        synonyms = get_synonyms(word)
        print synonyms
        populate_synonyms(synonyms, results.fetchone().id)
        flash(dict(type='success', content='Meaning found '))
        return redirect(url_for('word', word=word))


    if word :
        meaning=fetch_def(word)
        if meaning == None :
            flash(dict(type='warning', content='word not found'))
            return redirect(url_for('index'))
        sentence = fetch_sentence(word)

        message = Nodes.create(
            word=word, meaning=meaning, sentence=sentence, x =1, y=2, z = 3)
        synonyms = get_synonyms(word)
        print synonyms
        populate_synonyms(synonyms, message.id)
        if message is not None:  # ok
            flash(dict(type='success', content='Meaning downloaded'))
            
        else:  # create failed
            flash(dict(type='error', content='Failed to create new node'))
    else:  # invalid input
        flash(dict(type='warning', content='Empty input'))
    return redirect(url_for('word', word=word))
