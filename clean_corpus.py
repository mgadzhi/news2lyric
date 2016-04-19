# -*- coding: utf-8 -*-
import re
import sys
from urlparse import urlparse


def contains_number(line):
    match = re.search('[0-9]+', line)
    return match is not None


def contains_url(line):
    pattern = '(://)?.*\.[a-zA-Z]{2,3}/?'
    match = re.search(pattern, line)
    return match is not None

def replace_and(line):
    return line.replace('&', ' and ')

def delete_punctuation(line):
    pattern = '[\.?!\-#£\*%,&_<>°]+'
    new_line = re.sub(pattern, '', line)
    return new_line


def deal_with_apostrophe(line):
    pass


def lowercase(line):
    return line.lower()


def main():
    lines = (line for line in sys.stdin if not contains_number(line))
    lines_without_url = (line for line in lines if not contains_url(line))
    output_replace_and = (replace_and(line) for line in lines_without_url)
    output_delete_punctuation = (delete_punctuation(line) for line in output_replace_and)


if __name__ == '__main__':
    main()