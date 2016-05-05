# -*- coding: utf-8 -*-

from nltk.parse.stanford import StanfordDependencyParser
from nltk.stem.porter import PorterStemmer
porter_stemmer = PorterStemmer()

PATH_TO_JAR = 'stanford/stanford-parser.jar'
PATH_TO_MODELS = 'stanford/stanford-parser-3.5.2-models.jar'


def parse_sentence(sentence):
    parser = StanfordDependencyParser(path_to_jar=PATH_TO_JAR, path_to_models_jar=PATH_TO_MODELS)
    trees = list(parser.parse(sentence))
    if not trees:
        return None
    parsed_tree = trees[0]
    return list(parsed_tree.triples())


def is_subject(relation):
    return 'subj' in relation


def get_subject(triples):
    for object, relation, subject in triples:
        if is_subject(relation):
            return subject[0]


def get_verbs(triples):
    verbs = []
    for object, relation, subject in triples:
        if is_subject(relation):
            verbs.append(object)
    return [v[0] for v in verbs if porter_stemmer.stem(v[0]) not in ('have', 'be', 'will', 'might', 'could', 'can', 'would', 'should')]


def get_keywords(sentence):
    u"""Returns subj + verbs or []"""
    tree = parse_sentence(sentence)
    subj = get_subject(tree)
    verbs = get_verbs(tree)
    keywords = {
        'subj': None,
        'verbs': [],
    }
    if subj:
        keywords['subj'] = subj
    if verbs:
        keywords['verbs'] = verbs
    return keywords

if __name__ == '__main__':
    sentence = 'policeman has rescues poor dog'
    tree = parse_sentence(sentence)
    print get_subject(tree)
    print get_verbs(tree)
