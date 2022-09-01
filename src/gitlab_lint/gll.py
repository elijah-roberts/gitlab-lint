#!/usr/bin/env python3
# script to validate .gitlab-ci.yml

import sys
import os
import logging

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
    help="Disables HTTPS verification, which is enabled by default",
)
@click.option(
    "--reference",
    "-r",
    help="Git reference to use for validation context",
)
@click.option(
    "--verbose",
    "-v",
    default=False,
    is_flag=True,
    help="Enable verbose logging, useful for debugging and CI systems",
)
def gll(**kwargs):
    logger = logging.getLogger(__name__)
    if kwargs.get("verbose"):
        logging.basicConfig(level=logging.DEBUG)
    logger.debug("Received from Click: %s", kwargs)

    # Todo: Confirm CI_JOB_TOKEN has permissions to validate CIs against the API
    #   If it can't it's misleading and should be removed
    # GITLAB_PRIVATE_TOKEN isn't an official convention I don't think, perhaps remove it?
    argument_mapping = {
        "token": "GITLAB_PRIVATE_TOKEN",
        # "token": "CI_JOB_TOKEN",
        "reference": "CI_COMMIT_REF_NAME",
        "project": "CI_PROJECT_ID",
        "domain": "CI_SERVER_HOST",
        "file": "CI_CONFIG_PATH",
    }
    for argument_name, environment_variable_name in argument_mapping.items():
        if not kwargs.get(argument_name) and os.environ.get(environment_variable_name):
            logger.debug(
                "Set %s from environment to %s",
                argument_name,
                environment_variable_name,
            )
            # Can't use setDefault because the key might be there with None
            kwargs[argument_name] = os.environ.get(environment_variable_name)

    # Yoink an argument we no longer need
    kwargs.pop("verbose")

    # Destructure the dictionary to pass it in
    # I would like to convert get_validation_data to be decoupled from the arguments too, eventually
    data = get_validation_data(**kwargs)
    generate_exit_info(data)


def get_validation_data(file, domain, project, token, insecure, reference):
    logger = logging.getLogger(__name__)
    """
    Creates a post to gitlab ci/lint api endpoint
    Reference: https://docs.gitlab.com/ee/api/lint.html
    """
    if insecure:
        logger.debug("Suppressing InsecureRequestWarning in urllib3")
        # Suppress error message for not securing https if insecure is False
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    params = {}
    if token:
        logger.debug("Setting header 'private_token' to %s", token)
        params.update({"private_token": token})
    if reference:
        logger.debug("Setting header 'ref' to %s", reference)
        params.update({"ref": reference})
        logger.debug("Setting header 'dry_run' 'true'")
        params.update({"dry_run": "true"})  # Must be set or ref is ignored
    project_id = f"projects/{project}/" if project else ""
    logger.debug("Project string set to %s", project_id)

    with open(file) as f:
        r = requests.post(
            f"https://{domain}/api/v4/{project_id}ci/lint",
            json={"content": f.read()},
            params=params,
            verify=not insecure,
        )
        logger.debug(r)
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
    logger = logging.getLogger(__name__)
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
            logger.error(e)
        sys.exit(1)
    else:
        print("GitLab CI configuration is valid")
        sys.exit(0)


# Had to add the second one for Poetry's script feature to work
if __name__ in ("__main__", "gitlab_lint.gll"):
    gll()
