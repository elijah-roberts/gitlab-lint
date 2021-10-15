FROM python:3-alpine
ENV PATH=/root/.local/bin:$PATH
ENV GITLAB_LINT_DOMAIN=""
ENV GITLAB_LINT_PROJECT=""
ENV GITLAB_LINT_TOKEN=""
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --user --no-cache-dir -r /requirements.txt && \
    pip3 install --user --no-cache-dir gitlab_lint
ENTRYPOINT [ "gll" ]
CMD [ "--help" ]
