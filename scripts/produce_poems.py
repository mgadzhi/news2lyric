#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools
import os
import sys
import random

from news2lyric.grammar import parse_sentence, get_subject, get_verbs
from news2lyric.structures import guinea_pig


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


def produce_poem(key_ngrams_dict, rhyme_structure):
    return [random.choice(key_ngrams_dict[k]) for k in rhyme_structure]


def shuffle_keys_ngrams(file_paths, rhyme_structure):
    structure_keys_to_fnames = {}
    for rhyme_k in rhyme_structure:
        if rhyme_k not in structure_keys_to_fnames:
            structure_keys_to_fnames[rhyme_k] = random.choice(file_paths)
    structure_keys_to_ngrams = {}
    for k, v in structure_keys_to_fnames.iteritems():
        if k not in structure_keys_to_ngrams:
            with open(v) as handle:
                structure_keys_to_ngrams[k] = [line.strip() for line in handle.readlines()]
    return structure_keys_to_ngrams


def is_good_enough(poem):
    return len(set(line.split(' ')[-1] for line in poem)) == len(poem)


def produce_poem_with_line(file_paths, rhyme_structure, line_fname, found_words_title, subj_or_verb_line=None):
    print('line_fname = {}'.format(line_fname))
    print('subj_or_verb_l = {}'.format(subj_or_verb_line))
    dirname = os.path.dirname(file_paths[0])
    poem = [line_fname[0]]
    with open(os.path.join(dirname, line_fname[1])) as line_rhymes_file:
        line_rhymes = [l.strip() for l in line_rhymes_file]
    line_rhyme = random.choice(line_rhymes)
    while line_fname[0].split(' ')[-1] == line_rhyme.split(' ')[-1]:
        line_rhyme = random.choice(line_rhymes)
    poem.append(line_rhyme)
    print poem
    if found_words_title == 'subj&verb':
        next_file = random.choice(file_paths)
        with open(next_file) as nf:
            next_line_candidates = [l.strip() for l in nf]
            line3 = random.choice(next_line_candidates)
            line4 = random.choice(next_line_candidates)
            while line3.split(' ')[-1] == line4.split(' ')[-1]:
                line4 = random.choice(next_line_candidates)
        poem.append(line3)
        poem.append(line4)
    if found_words_title == 'subj':
        line3 = subj_or_verb_line[0]
        with open(os.path.join(dirname, subj_or_verb_line[1])) as line_rhymes_file:
            line_rhymes = [l.strip() for l in line_rhymes_file]
        line4 = random.choice(line_rhymes)
        while subj_or_verb_line[0].split(' ')[-1] == line4.split(' ')[-1]:
            line4 = random.choice(line_rhymes)
        poem.append(line3)
        poem.append(line4)
    print poem
    return poem


def main():
    if len(sys.argv) < 3:
        print("Usage: <scriptname> datadir title\ndatadir is the directory with the phonetic indices")
        sys.exit(1)
    datadir = sys.argv[1]
    title = sys.argv[2]

    tree = parse_sentence(title)
    subj = get_subject(tree)
    verbs = get_verbs(tree)

    print subj
    print verbs

    keywords = []
    if subj:
        keywords.append(subj)
    if verbs:
        keywords += verbs
    if not keywords:
        print 'Unable to parse sentence: {}'.format(title)
        sys.exit(1)
    file_paths = []
    keywords_to_ngrams = {k: set() for k in keywords}
    for dname, _dirs, fnames in os.walk(datadir):
        # file_paths = [os.path.join(dname, fname) for fname in fnames if contains_n_lines(os.path.join(dname, fname), 2)]
        for fname in fnames:
            fpath = os.path.join(dname, fname)
            if contains_n_lines(fpath, 2):
                file_paths.append(fpath)
            for word, line, _fname in grep(fpath, *keywords):
                keywords_to_ngrams[word].add((line, _fname))
        break

    #with_subj_and_verbs = keywords_to_ngrams[subj] & keywords_to_ngrams[verbs[0]]
    if keywords_to_ngrams[subj] & keywords_to_ngrams[verbs[0]]:
        p = produce_poem_with_line(file_paths, guinea_pig[1], list(keywords_to_ngrams[subj] &
                                                                   keywords_to_ngrams[verbs[0]])[0], 'subj&verb')
        print '\n'.join(p)
        print '---'
        sys.exit(2)
    if keywords_to_ngrams[subj]:
        p = produce_poem_with_line(file_paths, guinea_pig[1], list(keywords_to_ngrams[subj])[0], 'subj',
                                   list(keywords_to_ngrams[verbs[0]])[0])
        print '\n'.join(p)
        print '---'
        sys.exit(2)
    if not keywords_to_ngrams[subj]:
        print('Poem cannot be generated')
        sys.exit(2)



    if len(file_paths) == 0:
        print("There are no files available")
        sys.exit(2)

    # structure_keys_to_ngrams = shuffle_keys_ngrams(file_paths, guinea_pig[1])
    # poem = produce_poem(structure_keys_to_ngrams, guinea_pig[1])
    # while not is_good_enough(poem):
    #     structure_keys_to_ngrams = shuffle_keys_ngrams(file_paths, guinea_pig[1])
    #     poem = produce_poem(structure_keys_to_ngrams, guinea_pig[1])
    # print '\n'.join(poem)

    # import pprint
    # pprint.pprint(keywords_to_ngrams)

    #p = produce_poem_with_line(file_paths, guinea_pig[1], list(with_subj_and_verbs)[0])
    #print '\n'.join(p)
    #print '---'


if __name__ == '__main__':
    main()
