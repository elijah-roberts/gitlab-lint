# gitlab_lint

This is a CLI application to quickly lint .gitlab-ci.yml files using the gitlab api. This can easily be added as a pre-commit step to locally catch any issues with your configuration prior to pushing your changes.

## Installation
```python3 -m pip install -U gitlab_lint```

## Configuration
You can set the following environmental variables:

`GITLAB_LINT_DOMAIN` - Which allows you to override the default gitlab.com domain, and point at a local instance

`GITLAB_LINT_TOKEN` - If your .gitlab-ci.yml contains any includes, you may need to set a private token to pull data from those other repos

`GITLAB_LINT_PROJECT` - If your .gitlab-ci.yml contains any includes which source from your local repo, you may set your project ID. If your repo is private, you must set your token as well.

 I would recommend adding these to your ~/.profile or ~/.bash_profile

## Parameters

| Flag | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| --domain | Gitlab Domain. You can set envvar `GITLAB_LINT_DOMAIN` | string | `gitlab.com` | no |
| --project | Gitlab Project ID. You can set envvar `GITLAB_LINT_PROJECT` | string | `None` | no |
| --token | Gitlab Personal Token. You can set envvar `GITLAB_LINT_TOKEN`  | string | `None`| no |
| --path | Path to .gitlab-ci.yml, defaults to local directory | string | `.gitlab-ci.yml` | no |
| --verify | Enables HTTPS verification, which is disabled by default to support privately hosted instances | Flag | `False` | no |

## Example Usage
If your .gitlab-ci.yml is in the current directory it is as easy as:
```
$ gll
GitLab CI configuration is valid

```

Failures will appear like so:
```
$ gll
GitLab CI configuration is invalid
(<unknown>): could not find expected ':' while scanning a simple key at line 26 column 1
```

If you need to you can specify the path:
```
$ gll --path path/to/.gitlab-ci.yml
GitLab CI configuration is valid

```

If you choose not to set the envvars for domain and token you can pass them in as flags:
```
$ gll --path path/to/.gitlab-ci.yml --domain gitlab.mycompany.com --project 1234 --token <gitlab personal token>
GitLab CI configuration is valid

```


Https verification is disabled by default to support privately hosted instances, if you would like to enable pass the `--verify | -v` flag

```
$ gll --verify
GitLab CI configuration is valid

```
 ## Development

### Bug Reports & Feature Requests

Please use the submit a issue to report any bugs or file feature requests.

### Developing

If you are interested in being a contributor and want to get involved in developing this CLI application feel free to reach out

In general, PRs are welcome. We follow the typical trunk based development Git workflow.

 1. **Branch** the repo
 2. **Clone** the project to your own machine
 3. **Commit** changes to your branch
 4. **Push** your work back up to your branch
 5. Submit a **Merge/Pull Request** so that we can review your changes

**NOTE:** Be sure to merge the latest changes from "upstream" before making a pull request!

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
        args: [-d, my.private.repo, -r, project_id, -t, private_token]
```
(or remove the `args` line for gitlab.com).
