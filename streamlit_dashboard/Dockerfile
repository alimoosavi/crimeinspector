FROM ubuntu:20.04

RUN apt-get -y update \
  && apt-get --no-install-recommends -y install \
  python3 \
  python3-dev \
  python3-pip \
  build-essential \
  && rm -Rf /var/lib/apt/lists/*


COPY . /var/www/streamlit-dashboard
WORKDIR /var/www/streamlit-dashboard
RUN python3 -m pip install -r requirements.txt


EXPOSE 8501
CMD streamlit run streamlit_dashboard.py --server.port 8501