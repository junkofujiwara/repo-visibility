#!/usr/bin/env python3
# -*- coding: utf_8 -*-
"""github_query.py"""
import logging
import requests

def list_repos(org, token):
    """list repos"""
    data = []
    next_page = True
    cursor = None
    logging.info("Executing list repo query. org=%s", org)
    while next_page:
        query, variables = build_query(org, cursor)
        result = run_query(query, variables, token)
        if is_error(result):
            return data
        cursor = result["data"]["search"]["pageInfo"]["endCursor"]
        next_page = result["data"]["search"]["pageInfo"]["hasNextPage"]
        for node in result["data"]["search"]["edges"]:
            data.append([node["node"]["name"], node["node"]["visibility"]])
    return data

def update_repos(org, token, data):
    """update repos"""
    counter = 0
    for repo in data:
        name = repo[0] # name of repo
        target = repo[2] # diff result: True/False
        visilibity = repo[3] # expected visibility
        if target == "False" and visilibity != "NOT FOUND":
            counter = counter + update_repo(org, name, visilibity, token)
    return counter

def update_repo(org, repo, visibility, token):
    """update repo"""
    logging.info("Updating visilibity to org=%s, repo=%s, visibility=%s", org, repo, visibility)
    url = f'https://api.github.com/repos/{org}/{repo}'
    value = {'visibility' : visibility.lower()}
    result = run_patch(url, value, token)
    if result is not None and visibility.lower() == result["visibility"]:
        logging.info("Updated visibility to org=%s, repo=%s, visibility=%s",
          org, repo, result["visibility"])
        return 1
    return 0

def is_error(result):
    """is error"""
    try:
        error = result["errors"]
        logging.error(error)
        return True
    except KeyError:
        return False

def run_patch(url, value, token, throw_exception=False):
    """run patch (REST)"""
    try:
        headers = {"Authorization": f"bearer {token}"}
        request = requests.patch(url,
          json=value,
          headers=headers)
        request.raise_for_status()
        return request.json()
    except (requests.exceptions.ConnectionError,
      requests.exceptions.Timeout,
      requests.exceptions.HTTPError) as exception:
        logging.error("Request failed. %s", exception)
        logging.debug("Failed Url: %s, Value: %s", url, value)
        if throw_exception:
            raise SystemExit(exception) from exception
    return None

def run_query(query, variables, token):
    """run query (GraphQL)"""
    try:
        headers = {"Authorization": f"bearer {token}"}
        request = requests.post('https://api.github.com/graphql',
          json={'query': query, "variables": variables},
          headers=headers)
        request.raise_for_status()
        return request.json()
    except (requests.exceptions.ConnectionError,
      requests.exceptions.Timeout,
      requests.exceptions.HTTPError) as exception:
        logging.error("Request failed. %s", exception)
        logging.debug("Failed Query: %s", query)
        raise SystemExit(exception) from exception

def build_query(org, cursor):
    """build query"""
    if cursor is None:
        variables = VARIABLES_TEMPLATE_INIT.format(org=org)
    else:
        variables = VARIABLES_TEMPLATE.format(org=org, cursor=cursor)
    return QUERY_TEMPLATE, variables

VARIABLES_TEMPLATE = """
{{
  "queryString": "org:{org}",
  "cursor" : "{cursor}"
}}
"""
VARIABLES_TEMPLATE_INIT = """
{{
  "queryString": "org:{org}",
  "cursor" : null
}}
"""

QUERY_TEMPLATE = """
  query($queryString: String!, $cursor: String) {
    search(query: $queryString, after: $cursor, type: REPOSITORY, first: 10) {
      repositoryCount
      pageInfo {
          endCursor
          hasNextPage
        }
      edges {
        node {
          ... on Repository {
            name,
            visibility
          }
        }
      }
    }
  }
"""
