#!/usr/bin/env python3
# script to validate .gitlab-ci.yml

import sys

import click
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


@click.command()
@click.option("--domain", "-d", envvar='GITLAB_LINT_DOMAIN', default="gitlab.com",
              help="Gitlab Domain. You can set envvar GITLAB_LINT_DOMAIN")
@click.option("--project", "-r", envvar='GITLAB_LINT_PROJECT',
              help="Gitlab Project ID. You can set envvar GITLAB_LINT_PROJECT")
@click.option("--token", "-t", envvar='GITLAB_LINT_TOKEN',
              help="Gitlab Personal Token. You can set envvar GITLAB_LINT_TOKEN")
@click.option("--path", "-p", default=".gitlab-ci.yml", help="Path to .gitlab-ci.yml, defaults to local directory",
              type=click.Path(exists=True, readable=True, file_okay=True))
@click.option("--verify", "-v", default=False, is_flag=True,
              help="Enables HTTPS verification, which is disabled by default to support privately hosted instances")
def gll(domain, project, token, path, verify):
    data = get_validation_data(path, domain, project, token, verify)
    generate_exit_info(data)


def get_validation_data(path, domain, project, token, verify):
    """
    Creates a post to gitlab ci/lint  api endpoint
    Reference: https://docs.gitlab.com/ee/api/lint.html
    :param path: str path to .gitlab-ci.yml file
    :param domain: str gitlab endpoint defaults to gitlab.com, this can be overriden for privately hosted instances
    :param project: str gitlab project id. If specified, used to validate .gitlab-ci.yml file with a namespace
    :param token: str gitlab token. If your .gitlab-ci.yml file has includes you may need it to authenticate other repos
    :param verify: bool flag to enable/disable https checking. False by default to support privately hosted instances
    :return: data json response data from api request
    """

    if not verify:
        # mask error message for not verifying https if verify is False
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    params = {'private_token': token} if token else None
    project_id = f"projects/{project}/" if project else ""


    with open(path) as f:
        r = requests.post(f"https://{domain}/api/v4/{project_id}ci/lint", json={'content': f.read()}, params=params, verify=verify)
    if r.status_code != 200:
        raise click.ClickException(
            f"API endpoint returned invalid response: \n {r.text} \n confirm your `domain`, `project`, and `token` have been set correctly")
    data = r.json()
    return data


def generate_exit_info(data):
    """
    Parses response data and generates exit message and code
    :param data: json gitlab API ci/lint response data
    """
    valid = None

    # for calling the lint api
    if 'status' in data:
        valid = data['status'] == 'valid'

    # for calling the lint api in the project context
    if 'valid' in data:
        valid = data['valid']

    if not valid:
        print("GitLab CI configuration is invalid")
        for e in data['errors']:
            print(e, file=sys.stderr)
        sys.exit(1)
    else:
        print("GitLab CI configuration is valid")
        sys.exit(0)


if __name__ == '__main__':
    gll()
