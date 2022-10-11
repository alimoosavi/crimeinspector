FROM ubuntu:20.04

RUN apt-get -y update \
  && apt-get --no-install-recommends -y install \
  python3 \
  python3-dev \
  python3-pip \
  build-essential \
  && rm -Rf /var/lib/apt/lists/*

COPY . /var/www/app
WORKDIR /var/www/app

RUN python3 -m pip install -r requirements.txt
#RUN python3 manage.py migrate
EXPOSE 8000
RUN chmod +x start-server.sh
CMD ./start-server.sh