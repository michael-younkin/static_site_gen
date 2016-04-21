FROM python:latest
MAINTAINER Michael Younkin

RUN apt-get update
RUN apt-get upgrade -y

RUN pip3 install markdown

RUN apt-get install -y ruby
RUN gem install sass

RUN useradd site_gen
USER site_gen
