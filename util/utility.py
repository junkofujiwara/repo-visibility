#!/usr/bin/env python3
# -*- coding: utf_8 -*-
"""common.py"""
import csv
import getopt
import logging
import sys

def init():
    """init"""
    try:
        github_org = None
        github_token = None
        script = sys.argv[0]
        usage_text = (f"Usage: {script} [list|compare|update]"
                "-o <organization_name> -t <github_personal_token>")
        operation = sys.argv[1]
        opts, _args = getopt.getopt(
            sys.argv[2:], "o:t:h", ["org=", "token=", "help"]
        )
        for opt, arg in opts:
            if opt in ("-o", "--org"):
                github_org = arg
            if opt in ("-t", "--token"):
                github_token = arg
            elif opt in ("-h", "--help"):
                logging.info(usage_text)
                sys.exit()
        if github_org is None:
            logging.info(usage_text)
            sys.exit()
        if github_token is None:
            logging.info(usage_text)
            sys.exit()
        return github_org, github_token, operation
    except (getopt.GetoptError, IndexError) as exception:
        logging.error(exception)
        logging.info(usage_text)
        sys.exit(1)

def write_file(data, file_name):
    """write file"""
    try:
        file = open(file_name, 'a+', encoding="utf8", newline ='')
        with file:
            writer = csv.writer(file)
            writer.writerows(data)
        return len(data)
    except (OSError, IOError) as exception:
        logging.error(exception)
        sys.exit(1)

def read_file(file_name):
    """read file"""
    try:
        file = open(file_name, 'r', encoding="utf8", newline ='')
        with file:
            reader = csv.reader(file, delimiter=',')
            return list(reader)
    except (OSError, IOError) as exception:
        logging.error(exception)
        sys.exit(1)

def compare_data(source, target):
    """compare data"""
    result = []
    for target_row in target:
        expected_value = ''
        found = target_row in source
        if not found:
            expected_value = find_value(source, target_row[0])
        target_row.extend([str(found), expected_value])
        result.append(target_row)
    return result

def find_value(source, repo):
    """find value"""
    try:
        expected_value = 'NOT FOUND'
        for source_row in source:
            if source_row[0] == repo:
                expected_value = source_row[1]
                break
        return expected_value
    except KeyError as exception:
        logging.error(exception)
    return None
