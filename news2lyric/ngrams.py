# -*- coding: utf-8 -*-

from itertools import izip
from phonetics import get_phonemes, num_of_syllables
from utils import flatten


def phonetic_ngrams(line, n=8):
    u"""
    >>> phonetic_ngrams('there was a little guinea pig', n=8)
    [['there', 'was', 'a', 'little', 'guinea', 'pig']]
    """
    # 'if word' will evaluate to True for all non-empty strings
    # So, with 'a  b' -> ['a', '', 'b'] the empty string will be filtered out
    words = [word for word in line.split(' ') if word]
    try:
        # We only take the first element of the list
        # Because all elements will have the same number of syllables
        word_phonemes = [get_phonemes(word)[0] for word in words]
    except IndexError as e:
        # Index error occurs when cmudict cannot return phonemes for a given (unknown) word
        return []
    wordsNum = len(words)
    result = []
    for i in range(wordsNum):
        ngrams = []
        for w, ph in izip(words[i:], word_phonemes[i:]):
            ngrams.append((w, ph))
            syl_num = num_of_syllables(flatten(pair[1] for pair in ngrams))
            # print ngrams, syl_num
            if syl_num == n:
                result.append([pair[0] for pair in ngrams])
                # print result[-1]
            elif syl_num > n:
                break
    return result


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)



