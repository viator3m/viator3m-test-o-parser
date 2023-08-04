FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install -r /requirements.txt


COPY ./infra/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./ ./
