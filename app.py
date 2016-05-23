# -*- coding: utf-8 -*-
import codecs
import json
import os
from itertools import izip
from stop_words import get_stop_words
en_stopwords = get_stop_words('en')

import news2lyric.clean as clean

from flask import Flask
from flask import render_template

from news2lyric.grammar import get_keywords, parse_sentence, get_subject, get_verbs
from news2lyric.poems import produce_poem, produce_poem_with_line
from news2lyric.structures import guinea_pig

app = Flask(__name__)
app.debug = True

INDEX_DIR = 'data/rhymes_index/0-1-0-1-0-1-0-1'

TITLES = (
    'apple presented new iphone',
    'obama signed contract',
    # 'putin declared war',
    # 'anne kissed mango',
    # 'mango did not kiss anne',
)

TITLES_FILE = 'data/titles.txt'


def clean_titles(source):
    lines_without_enumeration_digits = (clean.delete_enumeration_digit(line) for line in source)
    lines_without_enumeration_charachters = (clean.delete_enumeration_character(line) for line in
                                             lines_without_enumeration_digits)
    lines_without_url = (line for line in lines_without_enumeration_charachters if not clean.contains_url(line))
    output_replace_and = (clean.replace_and(line) for line in lines_without_url)
    #output_delete_punctuation = (clean.delete_punctuation(line) for line in output_replace_and)
    output_delete_dots_end_sentence = (clean.delete_dots_end_sentence(line) for line in output_replace_and)
    output_deal_with_apostrophe = (clean.deal_with_apostrophe(line) for line in output_delete_dots_end_sentence)
    output_deal_with_dash = (clean.deal_with_dash(line) for line in output_deal_with_apostrophe)
    output_lowercase = (clean.lowercase(line) for line in output_deal_with_dash)
    output_doublespaces = [clean.remove_doublespace(line) for line in output_lowercase]
    return output_doublespaces


def read_titles():
    with open(TITLES_FILE) as tf:
        source = codecs.getreader(u'utf-8')(tf)
        return source.readlines()



def contains_n_lines(fname, n):
    cnt = 0
    with open(fname) as f:
        for _ in f:
            cnt += 1
            if cnt == n:
                return True
    return False


def grep(fpath, *words):
    with open(fpath) as source:
        for line in source:
            line = line.strip()
            for word in words:
                if word in line.split(' '):
                    yield word, line, os.path.basename(fpath)


@app.route("/")
def index():
    raw_titles = read_titles()
    titles = clean_titles(raw_titles)
    titles_view = [(raw, '_'.join(clean.split(' '))) for raw, clean in izip(raw_titles, titles)]
    return render_template("index.html", titles=titles_view[:50])


@app.route("/poem/<title>")
def poem(title):
    sentence = title.split('_')
    print type(sentence[0])
    tree = parse_sentence(sentence)
    subj = get_subject(tree)
    verbs = get_verbs(tree)
    stopped_tokens = [i for i in sentence if not i in en_stopwords]
    remaining_lexical_items = [i for i in stopped_tokens if i != subj and i not in verbs]
    number_RLI = len(remaining_lexical_items)
    print('subj: {}, type: {}'.format(subj, type(subj)))
    print ('verbs: {}, type: {}'.format(verbs, type(verbs)))
    print ('stopped tokens: {}'.format(stopped_tokens))
    print ('remaining lexical items: {}'.format(remaining_lexical_items))
    keywords = []
    if subj:
        keywords.append(subj)
    if verbs:
        keywords += verbs
    if remaining_lexical_items:
        keywords += remaining_lexical_items
    file_paths = []
    keywords_to_ngrams = {k: set() for k in keywords}
    for dname, _dirs, fnames in os.walk(INDEX_DIR):
        # file_paths = [os.path.join(dname, fname) for fname in fnames if contains_n_lines(os.path.join(dname, fname), 2)]
        for fname in fnames:
            fpath = os.path.join(dname, fname)
            if contains_n_lines(fpath, 10):
                file_paths.append(fpath)
            for word, line, _fname in grep(fpath, *keywords):
                keywords_to_ngrams[word].add((line, _fname))
        break
    p = None

    if subj and remaining_lexical_items[0] and keywords_to_ngrams[subj] & keywords_to_ngrams[remaining_lexical_items[0]]:
        print 'NUMBER 1'
        p = produce_poem_with_line(file_paths, guinea_pig[1],
                                   list(keywords_to_ngrams[subj])[0], '2items',
                                   list(keywords_to_ngrams[remaining_lexical_items[0]])[0])
        pass
    elif subj and remaining_lexical_items[number_RLI-1] and keywords_to_ngrams[subj] & keywords_to_ngrams[remaining_lexical_items[number_RLI-1]]:
        print 'NUMBER 2'
        p = produce_poem_with_line(file_paths, guinea_pig[1],
                                   list(keywords_to_ngrams[subj])[0], '2items',
                                   list(keywords_to_ngrams[remaining_lexical_items[number_RLI-1]])[0])
        pass
    elif subj and verbs and keywords_to_ngrams[subj] and keywords_to_ngrams[verbs[0]]:
        print 'NUMBER 4'
        p = produce_poem_with_line(file_paths, guinea_pig[1],
                                   list(keywords_to_ngrams[subj])[0], '2items',
                                   list(keywords_to_ngrams[verbs[0]])[0])
        pass
    elif verbs and remaining_lexical_items[0] and keywords_to_ngrams[verbs[0]] and keywords_to_ngrams[remaining_lexical_items[0]]:
        print 'NUMBER 5'
        p = produce_poem_with_line(file_paths, guinea_pig[1],
                                   list(keywords_to_ngrams[verbs[0]])[0], '2items',
        list(keywords_to_ngrams[remaining_lexical_items[0]])[0])
    elif subj and keywords_to_ngrams[subj]:
        print 'NUMBER 3'
        p = produce_poem_with_line(file_paths, guinea_pig[1],
                                   list(keywords_to_ngrams[subj])[0], 'subj')
        pass
    elif number_RLI > 1:
        if remaining_lexical_items[number_RLI-1] and remaining_lexical_items[0] and keywords_to_ngrams[remaining_lexical_items[number_RLI-1]] and keywords_to_ngrams[
        remaining_lexical_items[0]]:
            print 'NUMBER 5'
            p = produce_poem_with_line(file_paths, guinea_pig[1],
                                list(keywords_to_ngrams[remaining_lexical_items[number_RLI-1]])[0], '2items',
                                list(keywords_to_ngrams[remaining_lexical_items[0]])[0])
    #if stopped_tokens and keywords_to_ngrams[stopped_tokens[0]]:

    if p:
        response = {
            'status': 'SUCCESS',
            'poem': '<br />'.join(p),
        }
        return json.dumps(response)
    else:
        response = {
            'status': 'FAILURE',
            'message': 'Failed to produce a poem',
        }
        return json.dumps(response)


if __name__ == '__main__':
    app.run()
