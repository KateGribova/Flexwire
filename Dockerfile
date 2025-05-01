FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /flexwire

COPY ./requirements /flexwire/requirements

RUN pip install -r /flexwire/requirements/requirements.txt
RUN pip install -r /flexwire/requirements/requirements_dev.txt

COPY . /flexwire

EXPOSE 8000