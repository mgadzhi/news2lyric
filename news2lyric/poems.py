# -*- coding: utf-8 -*-
import os
import random


def produce_poem():
    return 'The poem'


def is_good_enough(poem):
    return len(set(line.split(' ')[-1] for line in poem)) == len(poem)


def produce_poem_with_line(file_paths, rhyme_structure, line_fname, found_words_title, subj_or_verb_line=None):
    dirname = os.path.dirname(file_paths[0])
    poem = [line_fname[0]]
    with open(os.path.join(dirname, line_fname[1])) as line_rhymes_file:
        line_rhymes = [l.strip() for l in line_rhymes_file]
    line_rhyme = random.choice(line_rhymes)
    while line_fname[0].split(' ')[-1] == line_rhyme.split(' ')[-1]:
        line_rhyme = random.choice(line_rhymes)
    poem.append(line_rhyme)
    if found_words_title == 'subj&verb':
        line3 = subj_or_verb_line[0]
        with open(os.path.join(dirname, subj_or_verb_line[1])) as line_rhymes_file:
            line_rhymes = [l.strip() for l in line_rhymes_file]
        line4 = random.choice(line_rhymes)
        while subj_or_verb_line[0].split(' ')[-1] == line4.split(' ')[-1]:
            line4 = random.choice(line_rhymes)
        poem.append(line3)
        poem.append(line4)
    if found_words_title == 'subj':
        next_file = random.choice(file_paths)
        with open(next_file) as nf:
            next_line_candidates = [l.strip() for l in nf]
            line3 = random.choice(next_line_candidates)
            line4 = random.choice(next_line_candidates)
            while line3.split(' ')[-1] == line4.split(' ')[-1]:
                line4 = random.choice(next_line_candidates)
        poem.append(line3)
        poem.append(line4)
    return poem