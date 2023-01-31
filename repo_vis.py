#!/usr/bin/env python3
# -*- coding: utf_8 -*-
"""repo_vis.py"""
import logging
import settings
from util.utility import init, write_file, read_file, compare_data
from util.github_query import list_repos, update_repos

def main():
    """main"""
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s [%(levelname)s] %(message)s",
        handlers = [
            logging.FileHandler("repo_vis.log"),
            logging.StreamHandler()
        ])
    github_org, github_token, operation = init()
    if operation.casefold() == settings.OPERATION_LIST:
        logging.info("List repository name and visibilities")
        repo_count = write_file(list_repos(github_org, github_token), settings.OUTPUT_FILE)
        logging.info("Filed %s repos (%s)", repo_count, settings.OUTPUT_FILE)
    elif operation.casefold() == settings.OPERATION_COMPARE:
        logging.info("Compare repository visibilities")
        base_data = read_file(settings.OUTPUT_FILE)
        logging.info("Found %s repos in base file (%s)", len(base_data), settings.OUTPUT_FILE)
        target_data = list_repos(github_org, github_token)
        repo_count = write_file(target_data, settings.OUTPUT_FILE_TARGET)
        logging.info("Filed %s repos (%s)", repo_count, settings.OUTPUT_FILE_TARGET)
        result = compare_data(base_data, target_data)
        diff_count = write_file(result, settings.OUTPUT_FILE_DIFF)
        logging.info("Filed %s results (%s)", diff_count, settings.OUTPUT_FILE_DIFF)
    elif operation.casefold() == settings.OPERATION_UPDATE:
        logging.info("Update repository visibilities")
        update_data = read_file(settings.OUTPUT_FILE_DIFF)
        update_count = update_repos(github_org, github_token, update_data)
        logging.info("Updated %s repos", update_count)

if __name__ == "__main__":
    main()
