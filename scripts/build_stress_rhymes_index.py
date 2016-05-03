#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from news2lyric.phonetics import is_vowel, get_phonemes, stress_mask
from news2lyric.utils import flatten
from news2lyric.structures import guinea_pig
from news2lyric.validate import get_phonetic_combinations


EXCEPTIONS = {
    'to': 'IH0',
    'the': 'AH1',
    'a': 'AH0',
}


def exception_ending(line):
    for e, ending in EXCEPTIONS.iteritems():
        if line.endswith(e):
            return ending


def get_endings(line):
    ph_combinations = map(flatten, get_phonetic_combinations(line.split(' ')))
    result = set()
    for phonemes in ph_combinations:
        vowels = [(i, phoneme) for i, phoneme in enumerate(phonemes) if is_vowel(phoneme)]
        if vowels:
            idx, last_vowel = vowels[-1]
            reverse_idx = len(phonemes) - idx
            result.add(tuple(phonemes[-reverse_idx:]))
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: <scriptname> dirname")
        sys.exit(1)
    dirname = sys.argv[1]
    source = sys.stdin
    ngrams = (line.strip() for line in source)
    index_dirname = os.path.join(dirname, '0-1-0-1-0-1-0-1')
    if not os.path.exists(index_dirname):
        os.makedirs(index_dirname)
    for ngram in ngrams:
        # Working with stresses:
        ph_combinations = map(flatten, get_phonetic_combinations(ngram.split(' ')))
        stresses = map(stress_mask, ph_combinations)
        if guinea_pig[0][0] in stresses:
            # Working with rhymes:
            exc = exception_ending(ngram)
            if exc:
                with open(os.path.join(index_dirname, exc), 'a') as out:
                    out.write(ngram + '\n')
                    continue
            for ending in get_endings(ngram):
                key = '-'.join(ending)
                fname = os.path.join(index_dirname, key)
                with open(fname, 'a') as out:
                    out.write(ngram + '\n')


if __name__ == '__main__':
    main()
