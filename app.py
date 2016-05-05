# -*- coding: utf-8 -*-
import json
import os

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
    titles = [(t, '_'.join(t.split(' '))) for t in TITLES]
    return render_template("index.html", titles=titles)


@app.route("/poem/<title>")
def poem(title):
    sentence = title.split('_')
    tree = parse_sentence(sentence)
    subj = get_subject(tree)
    verbs = get_verbs(tree)

    print 'Subj = ', subj
    print 'Verbs = ', verbs

    keywords = []
    if subj:
        keywords.append(subj)
    if verbs:
        keywords += verbs

    file_paths = []
    keywords_to_ngrams = {k: set() for k in keywords}
    for dname, _dirs, fnames in os.walk(INDEX_DIR):
        # file_paths = [os.path.join(dname, fname) for fname in fnames if contains_n_lines(os.path.join(dname, fname), 2)]
        for fname in fnames:
            fpath = os.path.join(dname, fname)
            if contains_n_lines(fpath, 2):
                file_paths.append(fpath)
            for word, line, _fname in grep(fpath, *keywords):
                keywords_to_ngrams[word].add((line, _fname))
        break

    p = None
    if subj and verbs and keywords_to_ngrams[subj] & keywords_to_ngrams[verbs[0]]:
        p = produce_poem_with_line(file_paths, guinea_pig[1], list(keywords_to_ngrams[subj] &
                                                                   keywords_to_ngrams[verbs[0]])[0], 'subj&verb')
    if subj and keywords_to_ngrams[subj]:
        p = produce_poem_with_line(file_paths, guinea_pig[1], list(keywords_to_ngrams[subj])[0], 'subj',
                                   list(keywords_to_ngrams[verbs[0]])[0])

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
