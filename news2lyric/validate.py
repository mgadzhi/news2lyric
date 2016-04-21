# -*- coding: utf-8 -*-
from functools import partial
from itertools import chain, izip_longest
from utils import combinations, flatten

import phonetics as ph


#This function should be moved somewhere else in the future
def get_phonetic_combinations(words):
    line_phonemes = []
    for word in words:
        word_phonemes = ph.get_phonemes(word)
        if len(word_phonemes) == 1:
            if ph.num_of_syllables(word_phonemes[0]) == 1:
                word_phonemes.append(
                    [sound if not ph.is_stressed(sound) else sound.replace('1', '0') for sound in word_phonemes[0]])
        line_phonemes.append(word_phonemes)
    return combinations(*line_phonemes)


def validate_line(phonemes, structure):
    return ph.stress_mask(phonemes) == structure


def validate_couplet(couplet, structure):
    # for line in couplet:
    ph_combinations = (get_phonetic_combinations(line.split(' ')) for line in couplet)
    ph_lines = (map(flatten, line) for line in ph_combinations)
    stress_lines = (map(ph.stress_mask, phonemes) for phonemes in ph_lines)
    lines_masks_zip = izip_longest(stress_lines, structure)
    return all(b in a for a, b in lines_masks_zip)


