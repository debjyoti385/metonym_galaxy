# coding=utf8
from bs4 import BeautifulSoup
import urllib2
import sys
from datetime import datetime

from populate_dictionary import app
from populate_dictionary.models import Nodes

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
    #definition = soup.find_all("div",attrs={"class":'sblk'})
    try:
        # return definition[0].text+'\n'
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
    #definition = soup.find_all("div",attrs={"class":'sblk'})
    try:
        # return definition[0].text+'\n'
        # if you want to print multiple definitions
        defs = []
        i=1
        for found in definition:
           defs.append( str(i) +": "+ found.text)
           i=i+1
        return "\n \n".join(defs)
    except IndexError:
        return None






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
    query = Nodes.where(Nodes.word.like(word)).select()
    # query = Nodes.orderby(Nodes.id, desc=True).select()  # sort by created time
    results = query.execute()
    messages = results.fetchall()
    return render_template('template.html', nodes=messages)

@app.route('/create', methods=['POST'])
def create():
    word = request.form['word']

    query = Nodes.where(Nodes.word.like(word)).select()
    results = query.execute()
    count = results.count
    if count > 0 :
        flash(dict(type='warning', content='already exists'))
        return redirect(url_for('word', word=word))

    # meaning = request.form['meaning']
    # sentence = request.form['sentence']
    if word :

        meaning=fetch_def(word)
        if meaning == None :
            flash(dict(type='warning', content='word not found'))
            return redirect(url_for('index'))
        sentence = fetch_sentence(word)

        message = Nodes.create(
            word=word, meaning=meaning, sentence=sentence, x =1, y=2, z = 3)
        if message is not None:  # ok
            flash(dict(type='success', content='Meaning Found'))
        else:  # create failed
            flash(dict(type='error', content='Failed to create new node'))
    else:  # invalid input
        flash(dict(type='warning', content='Empty input'))
    return redirect(url_for('word', word=word))
