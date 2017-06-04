# coding=utf-8
import re
import os


def get_string_between_tags(string, opening_tag, closing_tag):
    """
    Return the substring between two tags. The substring will begins at the first occurrence of the
    opening tag and will finishes at the last occurrence of the closing tag.
    :param string: String in which are the tags
    :param opening_tag: Tag opening the substring
    :param closing_tag: Tag closing the substring
    :return: The substring between the opening tag and the closing tag
    """

    try:
        start = string.index(opening_tag) + len(opening_tag)
        end = string.rindex(closing_tag, start)
        return string[start:end]
    except ValueError:
        return ""


def prepare_tbschema_file(input_file, output_file):
    """
    Convert the output file of the "tbschema [DATABASE] > input_file" command on linux
    to my output_file which will be used by this script. It remove all blank line, all multispaces,
    all comments.
    :param input_file: The result of the tbschema [DATABASE] command
    :param output_file: The converted file
    """

    with open(input_file) as input_file, open("temp.tmp", "w") as temp:
        for line in input_file:
            # 0) Delete line 'Procedures stockees : cette option n'est pas encore implementee'
            if line.startswith('Procedures'):
                continue

            # 1) Delete the comment in braces
            new_line = re.sub('{[^}]+}', '', line)

            # 2) Delete all tabs
            new_line = new_line.strip('\t')

            # 3) Delete all multispaces
            new_line = re.sub(' +', ' ', new_line)

            # 4) Delete all new line character
            new_line = re.sub('\n', '', new_line)

            # 5) Delete all spaces at the beginning and at the end of the line
            new_line = new_line.lstrip(' ')
            new_line = new_line.rstrip(' ')

            # 6) If my line is empty, continue to the next one
            if not new_line.strip():
                continue

            # 7) If the last character of my line is a ';' then I create a new line
            if new_line[-1] == ';':
                new_line += '\n'

            # 8) If the last character of my line is not a '(' nor a ',' then add a space at the end
            if new_line[-1] != '(' and new_line[-1] != '\n':
                new_line += ' '

            # I write this new line on my temporary file
            temp.write(new_line)

    with open("temp.tmp") as temp, open(output_file, "w") as output_file:
        for line in temp:
            # 9) Delete all spaces before the char ')'
            line = re.sub(' [)]', ')', line)

            # I write this line on my output file
            output_file.write(line)

    try:
        os.remove("temp.tmp")
    except OSError:
        pass
