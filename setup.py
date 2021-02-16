from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='gitlab-lint',
    version='0.3.0',
    py_modules=['gitlab-lint'],
    author="Elijah Roberts",
    author_email="elijah@elijahjamesroberts.com",
    description="This is a CLI application to quickly lint .gitlab-ci.yml files using the gitlab api",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://github.com/elijah-roberts/gitlab_lint/archive/0.2.1.tar.gz",
    keywords=['GITLAB', 'LINT', 'GIT'],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'Click',
        'Requests'
    ],
    entry_points='''
        [console_scripts]
        gll=gitlab_lint.gll:gll
    ''',
)
