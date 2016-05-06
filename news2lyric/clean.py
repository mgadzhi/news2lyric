# -*- coding: utf-8 -*-

import re


# Enumerations such as 1. (digit + dot) will not be deleted since they can be line endings.
# These sentences will be omitted in contains_number(line)
def delete_enumeration_digit(line):
    pattern = u'[0-9]{1,2}\)'
    new_line = re.sub(pattern, ' ', line)
    return new_line


def delete_enumeration_character(line):
    pattern = u'[a-zA-Z]{1}\)'
    new_line = re.sub(pattern, ' ', line)
    return new_line


# Lines containing numbers will be omittted
def contains_number(line):
    match = re.search(u'[0-9]+', line)
    return match is not None


# Lines containing urls will be omitted
def contains_url(line):
    pattern = u'(://)?.*\.[a-zA-Z]{2,3}/?'
    match = re.search(pattern, line)
    return match is not None


def replace_and(line):
    return line.replace(u'&', u' and ')


def delete_punctuation(line):
    pattern = u'[?!\#£\*%,&_<>°":;\(\)/\[\]“”—]+'
    new_line = re.sub(pattern, ' ', line)
    return new_line


def delete_dots_end_sentence(line):
    pattern = u"[\.]+$"
    new_line = re.sub(pattern, ' ', line)
    return new_line


def deal_with_apostrophe(line):
    pattern = u"^'|\s'|'\s|'$"
    new_line = re.sub(pattern, ' ', line)
    return new_line


def deal_with_dash(line):
    pattern = u"^-|\s-|-\s|-$"
    new_line = re.sub(pattern, ' ', line)
    return new_line


def lowercase(line):
    return line.lower()


def remove_doublespace(line):
    return re.sub(u' {2,}', ' ', line.strip())
