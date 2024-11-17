FROM python:3.12-bullseye

RUN apt-get update
RUN pip install --upgrade pip poetry gunicorn

WORKDIR /srv/

ADD poetry.lock /srv/
ADD pyproject.toml /srv/    

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi


ADD manage.py /srv/
ADD project/ /srv/project/


ENTRYPOINT [ "gunicorn", "project.wsgi", "-b", "0.0.0.0:8000", "-w", "16", "--max-requests", "1", "-t", "30" ]