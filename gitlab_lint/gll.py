#!/usr/bin/env python3
# script to validate .gitlab-ci.yml

import sys
import os

import click
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from gitlab_lint.__init__ import __version__


@click.command(context_settings={"auto_envvar_prefix": "GLL"})
@click.version_option(__version__)
@click.option("--domain", "-d", default="gitlab.com", help="Gitlab domain")
@click.option("--project", "-p", help="Gitlab project ID")
@click.option("--token", "-t", help="Gitlab personal access token")
@click.option(
    "--file",
    "-f",
    default=".gitlab-ci.yml",
    help="Path to .gitlab-ci.yml, starts in local directory",
    type=click.Path(exists=True, readable=True, file_okay=True),
)
@click.option(
    "--insecure",
    "-i",
    default=False,
    is_flag=True,
    help="Enables HTTPS verification, which is disabled by default to support privately hosted instances",
)
@click.option(
    "--reference",
    "-r",
    help="Git reference to use for validation context",
)
def gll(domain, project, token, file, insecure, reference):
    if not token and os.environ.get("GITLAB_PRIVATE_TOKEN"):
        token = os.environ.get("GITLAB_PRIVATE_TOKEN")
    if not token and os.environ.get("CI_JOB_TOKEN"):
        token = os.environ.get("CI_JOB_TOKEN")
    if not reference and os.environ.get("CI_COMMIT_REF_NAME"):
        reference = os.environ.get("CI_COMMIT_REF_NAME")
    if not project and os.environ.get("CI_PROJECT_ID"):
        project = os.environ.get("CI_PROJECT_ID")
    if not domain and os.environ.get("CI_SERVER_HOST"):
        domain = os.environ.get("CI_SERVER_HOST")
    if not file and os.environ.get("CI_CONFIG_PATH"):
        file = os.environ.get("CI_CONFIG_PATH")

    data = get_validation_data(file, domain, project, token, insecure, reference)
    generate_exit_info(data)


def get_validation_data(file, domain, project, token, insecure, reference):
    """
    Creates a post to gitlab ci/lint api endpoint
    Reference: https://docs.gitlab.com/ee/api/lint.html
    :param file: str path to .gitlab-ci.yml file
    :param domain: str gitlab endpoint defaults to gitlab.com, this can be overriden for privately hosted instances
    :param project: str gitlab project id. If specified, used to validate .gitlab-ci.yml file with a namespace
    :param token: str gitlab token. If your .gitlab-ci.yml file has includes you may need it to authenticate other repos
    :param insecure: bool flag to enable/disable https checking. False by default to support privately hosted instances
    :return: data json response data from api request
    """

    if insecure:
        # mask error message for not securing https if insecure is False
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    params = {}
    if token:
        params.update({"private_token": token})
    if reference:
        params.update({"ref": reference})
        params.update({"dry_run": "true"})  # Must be set or ref is ignored
    project_id = f"projects/{project}/" if project else ""

    with open(file) as f:
        r = requests.post(
            f"https://{domain}/api/v4/{project_id}ci/lint",
            json={"content": f.read()},
            params=params,
            verify=not insecure,
        )
    if r.status_code != 200:
        raise click.ClickException(
            (
                f"API endpoint returned invalid response: \n {r.text} \n"
                "confirm your `domain`, `project`, and `token` have been set correctly"
            )
        )
    data = r.json()
    return data


def generate_exit_info(data):
    """
    Parses response data and generates exit message and code
    :param data: json gitlab API ci/lint response data
    """
    valid = None

    # for calling the lint api
    if "status" in data:
        valid = data["status"] == "valid"

    # for calling the lint api in the project context
    if "valid" in data:
        valid = data["valid"]

    if not valid:
        print("GitLab CI configuration is invalid")
        for e in data["errors"]:
            print(e, file=sys.stderr)
        sys.exit(1)
    else:
        print("GitLab CI configuration is valid")
        sys.exit(0)


if __name__ == "__main__":
    gll()
