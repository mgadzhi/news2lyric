#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itertools
import os
import sys
import random

from news2lyric.structures import guinea_pig


def contains_n_lines(fname, n):
    cnt = 0
    with open(fname) as f:
        for _ in f:
            cnt += 1
            if cnt == n:
                return True
    return False


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


def main():
    if len(sys.argv) < 2:
        print("Usage: <scriptname> datadir\ndatadir is the directory with the phonetic indices")
        sys.exit(1)
    datadir = sys.argv[1]
    file_paths = []
    for dname, _dirs, fnames in os.walk(datadir):
        file_paths = [os.path.join(dname, fname) for fname in fnames if contains_n_lines(os.path.join(dname, fname), 2)]
        break
    if len(file_paths) == 0:
        print("There are no files available")
        sys.exit(2)

    structure_keys_to_ngrams = shuffle_keys_ngrams(file_paths, guinea_pig[1])
    poem = produce_poem(structure_keys_to_ngrams, guinea_pig[1])
    while not is_good_enough(poem):
        structure_keys_to_ngrams = shuffle_keys_ngrams(file_paths, guinea_pig[1])
        poem = produce_poem(structure_keys_to_ngrams, guinea_pig[1])
    print '\n'.join(poem)
    print '---'



if __name__ == '__main__':
    main()