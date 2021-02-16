import pytest
from gitlab_lint.gll import *


def test_successful_validation():
    # results from default linting api
    data = {'status': 'valid', 'errors': [], 'warnings': []}
    with pytest.raises(SystemExit) as e:
        generate_exit_info(data)
    assert e.type == SystemExit
    assert e.value.code == 0

    # results from project-specific api
    data = {'valid': True, 'errors': [], 'warnings': []}
    with pytest.raises(SystemExit) as e:
        generate_exit_info(data)
    assert e.type == SystemExit
    assert e.value.code == 0


def test_error_validation():
    # results from default linting api
    data = {'status': 'invalid',
            'errors': ['(<unknown>): did not find expected key while parsing a block mapping at line 1 column 1'],
            'warnings': []}
    with pytest.raises(SystemExit) as e:
        generate_exit_info(data)
    assert e.type == SystemExit
    assert e.value.code == 1

    # results from project-specific api
    data = {'valid': False,
            'errors': ['(<unknown>): did not find expected key while parsing a block mapping at line 1 column 1'],
            'warnings': []}
    with pytest.raises(SystemExit) as e:
        generate_exit_info(data)
    assert e.type == SystemExit
    assert e.value.code == 1
