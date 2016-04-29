#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import re
import sys



# Sometimes one line contains a whole alinea
def split_on_new_line(line):
    new_line = line.strip('\r\n')
    return new_line.replace('!','\n').replace('.','\n').replace('?','\n').replace(';','\n')


# Enumerations such as 1. (digit + dot) will not be deleted since they can be line endings.
# These sentences will be omitted in contains_number(line)
def delete_enumeration_digit(line):
	pattern = re.search(u'[0-9]{1,2}\)')
	new_line = re.sub(pattern, ' ', line)
	return new_line


def delete_enumeration_character(line):
	pattern = re.search(u'[a-zA-Z]{1}\)')
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
    return re.sub(u' {2,}', ' ', line.strip())


def main():
    source = codecs.getreader(u'utf-8')(sys.stdin)
    sink = codecs.getwriter(u'utf-8')(sys.stdout)

	# if necessary, split_on_new_line
    lines_without_enumeration_digits = (delete_enumeration_digit(line) for line in source)
	lines_without_enumeration_charachters = (delete_enumeration_character(line) for line in lines_without_enumeration_digits)
	lines_without_numbers = (line.strip() for line in lines_without_enumeration_charachters if not contains_number(line))
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
