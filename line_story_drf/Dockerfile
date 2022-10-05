FROM python:3.10

WORKDIR /usr/src/line_story_drf

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install netcat -y
RUN apt-get upgrade -y && apt-get install -y postgresql gcc python3-dev musl-dev

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
COPY . .

RUN ["chmod", "+x", "/usr/src/line_story_drf/entrypoint.sh"]

ENTRYPOINT ["/usr/src/line_story_drf/entrypoint.sh"]
