#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import re
import sys


def contains_number(line):
    match = re.search(u'[0-9]+', line)
    return match is not None


def contains_url(line):
    pattern = u'(://)?.*\.[a-zA-Z]{2,3}/?'
    match = re.search(pattern, line)
    return match is not None


def replace_and(line):
    return line.replace(u'&', u' and ')


def delete_punctuation(line):
    pattern = u'[\.?!\#£\*%,&_<>°":;\(\)/\[\]“”—]+'
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
    return re.sub(u'\s+', ' ', line.strip())


def main():
    source = codecs.getreader(u'utf-8')(sys.stdin)
    sink = codecs.getwriter(u'utf-8')(sys.stdout)

    lines = (line.strip() for line in source if not contains_number(line))
    lines_without_url = (line for line in lines if not contains_url(line))
    output_replace_and = (replace_and(line) for line in lines_without_url)
    output_delete_punctuation = (delete_punctuation(line) for line in output_replace_and)
    output_deal_with_apostrophe = (deal_with_apostrophe(line) for line in output_delete_punctuation)
    output_deal_with_dash = (deal_with_dash(line) for line in output_deal_with_apostrophe)
    output_lowercase = (lowercase(line) for line in output_deal_with_dash)
    output_doublespaces = (remove_doublespace(line) for line in output_lowercase)
    for line in output_doublespaces:
        # sys.stdout.write(line.decode('utf-8'))
        sink.write(line.strip() + u'\n')


if __name__ == '__main__':
    main()
