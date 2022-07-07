#!/usr/bin/env python3
# script to validate .gitlab-ci.yml

import sys

import click
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


@click.command()
@click.option(
    "--domain", "-d", default="gitlab.com", help="Gitlab domain", envvar="GLL_DOMAIN"
)
@click.option("--project", "-p", help="Gitlab project ID", envvar="GLL_PROJECT")
@click.option("--token", "-t", help="Gitlab personal access token", envvar="GLL_TOKEN")
@click.option(
    "--file",
    "-f",
    default=".gitlab-ci.yml",
    help="Path to .gitlab-ci.yml, starts in local directory",
    type=click.Path(exists=True, readable=True, file_okay=True),
    envvar="GLL_FILE",
)
@click.option(
    "--verify",
    "-v",
    default=True,
    is_flag=True,
    help="Enables HTTPS verification, which is disabled by default to support privately hosted instances",
    envvar="GLL_VERIFY",
)
@click.option(
    "--reference",
    "-r",
    help="Git reference to use for validation context",
    envvar="GLL_REFERENCE",
)
def gll(domain, project, token, file, verify, reference):
    data = get_validation_data(file, domain, project, token, verify, reference)
    generate_exit_info(data)


def get_validation_data(file, domain, project, token, verify, reference):
    """
    Creates a post to gitlab ci/lint  api endpoint
    Reference: https://docs.gitlab.com/ee/api/lint.html
    :param file: str path to .gitlab-ci.yml file
    :param domain: str gitlab endpoint defaults to gitlab.com, this can be overriden for privately hosted instances
    :param project: str gitlab project id. If specified, used to validate .gitlab-ci.yml file with a namespace
    :param token: str gitlab token. If your .gitlab-ci.yml file has includes you may need it to authenticate other repos
    :param verify: bool flag to enable/disable https checking. False by default to support privately hosted instances
    :return: data json response data from api request
    """

    if not verify:
        # mask error message for not verifying https if verify is False
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
            verify=verify,
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
    # auto_envvar_prefix isn't working according to spec
    # https://click.palletsprojects.com/en/8.1.x/options/#values-from-environment-variables
    gll(auto_envvar_prefix="GLL")
