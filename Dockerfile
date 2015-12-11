FROM debian:stable

RUN apt-get update \
 && apt-get install -y \
    python \
    python-dev \
    python-pip \
    python-setuptools \
    apache2 \
    apache2-prefork-dev \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    r-base \
    r-base-dev \
    python-rpy2 \
    python-mysqldb \
    git-core

RUN pip install \
    mod_wsgi \
    Flask==0.10.1 \
    SQLAlchemy==0.9.9 \
    flask-cors==2.0.1 \
    flask-sqlalchemy==2.0 \
    nose==1.3.4 \
    numpy==1.9.2 \
    requests==2.6.0 \
    scipy==0.15.1 \
    pandas==0.16.2 \
    singledispatch==3.4.0.3 \
    six==1.9.0 \
    sklearn==0.0 \
    wsgiref==0.1.2 \
    git+git://github.com/MaayanLab/substrate.git@master

RUN apt-get clean

EXPOSE 80

ADD . /g2e

CMD /g2e/boot.sh