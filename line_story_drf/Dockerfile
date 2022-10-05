FROM python:3.10

WORKDIR /usr/src/line_story_drf

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install netcat -y && \
    apt-get upgrade -y && \
    apt-get install -y postgresql gcc python3-dev musl-dev && \
    pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

RUN ["chmod", "+x", "/usr/src/line_story_drf/entrypoint.sh"]

ENTRYPOINT ["/usr/src/line_story_drf/entrypoint.sh"]
