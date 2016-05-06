#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import news2lyric.clean as clean
import sys


# Sometimes one line contains a whole alinea
def split_on_new_line(line):
    new_line = line.strip()
    return new_line.replace('!','\n').replace('.','\n').replace('?','\n').replace(';','\n')


def main():
    source = codecs.getreader(u'utf-8')(sys.stdin)
    sink = codecs.getwriter(u'utf-8')(sys.stdout)
    
    # if necessary, split_on_new_line
    lines_without_enumeration_digits = (clean.delete_enumeration_digit(line) for line in source)
    lines_without_enumeration_charachters = (clean.delete_enumeration_character(line) for line in lines_without_enumeration_digits)
    lines_without_numbers = (line.strip() for line in lines_without_enumeration_charachters if not clean.contains_number(line))
    lines_without_url = (line for line in lines_without_numbers if not clean.contains_url(line))
    output_replace_and = (clean.replace_and(line) for line in lines_without_url)
    output_delete_punctuation = (clean.delete_punctuation(line) for line in output_replace_and)
    output_delete_dots_end_sentence = (clean.delete_dots_end_sentence(line) for line in output_delete_punctuation)
    output_deal_with_apostrophe = (clean.deal_with_apostrophe(line) for line in output_delete_dots_end_sentence)
    output_deal_with_dash = (clean.deal_with_dash(line) for line in output_deal_with_apostrophe)
    output_lowercase = (clean.lowercase(line) for line in output_deal_with_dash)
    output_doublespaces = (clean.remove_doublespace(line) for line in output_lowercase)
    for line in output_doublespaces:
        # sys.stdout.write(line.decode('utf-8'))
        sink.write(line.strip() + u'\n')


if __name__ == '__main__':
    main()