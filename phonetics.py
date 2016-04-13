# -*- coding: utf-8 -*-

from nltk.corpus import cmudict


stress_dict = cmudict.dict()


def get_phonemes(word):
    """
    >>> get_phonemes("hello")
    [[u'HH', u'AH0', u'L', u'OW1'], [u'HH', u'EH0', u'L', u'OW1']]
    >>> get_phonemes("world")
    [[u'W', u'ER1', u'L', u'D']]
    >>> get_phonemes("Capitalized") is None
    True
    >>> get_phonemes("Anneleen") is None
    True
    """
    return stress_dict.get(word)


def is_vowel(phoneme):
    """
    >>> is_vowel(u'AH0')
    True
    >>> is_vowel(u'W')
    False
    """
    return phoneme[-1].isdigit()


def is_consonant(phoneme):
    """
    >>> is_consonant(u'AH0')
    False
    >>> is_consonant(u'W')
    True
    """
    return not is_vowel(phoneme)


def num_of_syllables(phonemes):
    """
    >>> num_of_syllables([u'W', u'ER1', u'L', u'D'])
    1
    """
    return sum(1 for p in phonemes if is_vowel(p))


def is_stressed(phoneme):
    """
    >>> is_stressed(u'ER1')
    True
    >>> is_stressed('AH0')
    False
    """
    return phoneme[-1] == '1'


def is_rhyme(phonemes1, phonemes2):
    """
    >>> is_rhyme([u'B', u'IH1', u'G'], [u'P', u'IH1', u'G'])
    True
    """
    vowels = [(i, phoneme) for i, phoneme in enumerate(phonemes1) if is_vowel(phoneme)]
    if vowels:
        idx, last_vowel = vowels[-1]
        return phonemes1[-(idx + 1):] == phonemes2[-(idx + 1):]
    else:
        return False


def stress_mask(phonemes):
    """
    >>> stress_mask([u'DH', u'EH0', u'R', u'W', u'AA1', u'Z', u'AH0', u'L', u'IH1', u'T', u'AH0', u'L', u'G', u'IH1', u'N', u'IY0', u'P', u'IH1', u'G'])
    [False, True, False, True, False, True, False, True]
    """
    return [is_stressed(ph) for ph in phonemes if is_vowel(ph)]


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)