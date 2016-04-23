#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import codecs
import sys
from news2lyric.ngrams import phonetic_ngrams


def main():
    # We assume the corpus is already cleaned
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--ngrams', type=int, default=8, help="Number of syllables for verse line")
    args = parser.parse_args()

    source = codecs.getreader('utf-8')(sys.stdin)
    sink = codecs.getwriter('utf-8')(sys.stdout)
    for line in source:
        n_syllable_line = phonetic_ngrams(line.strip(), args.ngrams)
        for ngram in n_syllable_line:
            sink.write(u' '.join(ngram) + u'\n')


if __name__ == "__main__":
    main()
