# gitlab_lint

This is a CLI application to quickly lint .gitlab-ci.yml files using the gitlab api. This can easily be added as a pre-commit step to locally catch any issues with your configuration prior to pushing your changes.

## Installation
```pip install gitlab_lint```

## Parameters

| Flag | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| --domain | Gitlab Domain. You can set envvar `GITLAB_LINT_DOMAIN` | string | `gitlab.com` | no |
| --token | Gitlab Personal Token. You can set envvar `GITLAB_LINT_TOKEN`  | string | `None`| no |
| --path | Path to .gitlab-ci.yml, defaults to local directory | string | `.gitlab-ci.yml` | no |

## Example Usage
```
$ python main.py --path examples/.gitlab-ci.yml 
GitLab CI configuration is valid

```

## Configuration
You can set the following environmental variables:

`GITLAB_LINT_DOMAIN` - Which allows you to override the default gitlab.com domain, and point at a local instance

`GITLAB_LINT_TOKEN` - If your .gitlab-ci.yml contains any includes, you may need to set a private token to pull data from those other repos
 
 
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

