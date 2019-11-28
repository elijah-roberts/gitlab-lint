#!/usr/bin/env python3
# script to validate .gitlab-ci.yml
#

import sys
import requests
import json
import click
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


@click.command()
@click.option("--domain", envvar='GITLAB_LINT_DOMAIN', default="gitlab.com", help="Gitlab Domain. You can set envvar GITLAB_LINT_DOMAIN")
@click.option("--token", envvar='GITLAB_LINT_TOKEN', help="Gitlab Personal Token. You can set envvar GITLAB_LINT_TOKEN")
@click.option("--path", default=".gitlab-ci.yml", help="Path to .gitlab-ci.yml, defaults to local directory")
def main(domain, token, path):
    confirm_path(path)
    url = get_url(domain, token)
    data = get_validation_data(path, url)
    if data['status'] != 'valid':
        print("GitLab CI configuration is invalid")
        for e in data['errors']:
            print(e, file=sys.stderr)
        sys.exit(1)
    else:
        print("GitLab CI configuration is valid")
        sys.exit(0)


def confirm_path(path):
    """
    Confirms that the path exists, and if not raises exception and provides helpful hints
    :param path: str path to .gitlab-ci.yml file
    """
    if not os.path.exists(path):
        if path == ".gitlab-ci.yml":
            raise click.ClickException(
                "No ./gitlab-ci.yml found in the current directory\n Try again and use the `--path` arguement")
        else:
            raise click.ClickException("No ./gitlab-ci.yml found at that path, confirm and try again")


def get_validation_data(path, url):
    """
    Creates a post to gitlab ci/lint  api endpoint
    Reference: https://docs.gitlab.com/ee/api/lint.html
    :param path: str path to .gitlab-ci.yml file
    :param url: str url for gitlab endpoint, this can be overriden to work with privately hosted gitlab instances
    :return: data json response data from api request
    """
    with open(path) as f:
        r = requests.post(url, json={'content': f.read()}, verify=False)
    if r.status_code != 200:
        raise click.ClickException(f"API endpoint returned invalid response: \n {r.text} \n confirm your `domain` and `token` have been set correctly")
    data = r.json()
    return data


def get_url(domain, token):
    """
    Generates a url based of the domain and token variables
    :param domain: name of the gitlab domain defaults to gitlab.com, but can be overriden for privately hosted instances
    :param token: str option gitlab token, which can be used if you are including other gitlab files that require auth
    :return: url: str compiled url for api request
    """
    if token:
        url = f"https://{domain}/api/v4/ci/lint?private_token={token}"
    else:
        url = f"https://{domain}/api/v4/ci/lint"
    return url


if __name__ == '__main__':
    main()
