# gitlab_lint

[![Downloads](https://pepy.tech/badge/gitlab-lint)](https://pepy.tech/project/gitlab-lint)

This is a CLI application to quickly lint `.gitlab-ci.yml` files using the GitLab api.
This can easily be added as a pre-commit step to locally catch any issues with your configuration prior to pushing your changes.

## Installation

`$ python3 -m pip install -U gitlab_lint`

## Configuration

### Parameters

Run `gll --help` for full descriptions.
All parameters can be set by environment variable, simply prefix the double-dash or long version with `GLL_`.
These can be added to your ~/.profile or ~/.bash_profile for convenience.
If options/arguments aren't set it, the application will search for GitLab CI variables instead.

## Example Usage

If your .gitlab-ci.yml is in the current directory it is as easy as:

```bash
$ gll
GitLab CI configuration is valid
```

Failures will appear like so:

```bash
$ gll
# GitLab CI configuration is invalid
# (<unknown>): could not find expected ':' while scanning a simple key at line 26 column 1
```

If you need to you can specify the path:

```bash
$ gll --file path/to/.gitlab-ci.yml
# GitLab CI configuration is valid
```

If you choose not to set the envvars for domain and token you can pass them in as flags:

```bash
$ gll --file path/to/.gitlab-ci.yml --domain gitlab.mycompany.com --project 1234 --token <gitlab personal token>
# GitLab CI configuration is valid
```

Https verification is enabled by default, if you wish to disable it pass the `--verify | -v` flag:

```bash
$ gll --verify
# GitLab CI configuration is valid
```

## Development

### Bug Reports & Feature Requests

Please use the submit a issue to report any bugs or file feature requests.

### Developing

<!--- pyml disable-next-line md013-->
If you are interested in being a contributor and want to get involved in developing this CLI application feel free to reach out!

In general, PRs are welcome. We follow the typical trunk based development Git workflow.

1. **Fork** the repo
1. **Clone** the project to your own machine
1. **Run** the devcontainer
1. **Make** and **test** your changes
1. **Commit** changes to your branch using `cz bump`
1. **Push** your work back up to your branch including tags `git push --all`
1. Submit a **Merge/Pull Request** so that we can review your changes

**NOTE:** Be sure to merge the latest changes from upstream before making a pull request!

### Virtual environments

This project supports Poetry for Python virtual environments.
Poetry may be installed via `pip`, and environments can be accessed with `poetry shell` or `poetry run`.

#### Tests

Run tests in root directory with `pytest`

### pre-commit

To use this with pre-commit.com, you can use something like

```yaml
-   repo: https://github.com/mick352/gitlab-lint
    rev: pre-commit-hook
    hooks:
    -   id: gitlab-ci-check
        pass_filenames: false
        args: [-d, my.private.gitlab.com, -p, project_id, -t, private_token]
```

(or remove the `args` line for gitlab.com).

### TODO

Look into automagic release jobs

```Bash
poetry version $(git describe --tags --abbrev=0)
poetry build
```
