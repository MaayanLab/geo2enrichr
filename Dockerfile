FROM debian:stable

RUN apt-get update
RUN apt-get install -y python python-dev python-pip python-setuptools
RUN apt-get install -y apache2 apache2-prefork-dev
RUN apt-get install -y gfortran libopenblas-dev liblapack-dev
RUN apt-get install -y r-base r-base-dev python-rpy2
RUN pip install mod_wsgi Flask==0.10.1 SQLAlchemy==0.9.9 mysql-connector-python==2.0.3 nose==1.3.4 --allow-external mysql-connector-python
RUN pip install numpy==1.9.2 requests==2.6.0 scipy==0.15.1 singledispatch==3.4.0.3 six==1.9.0 wsgiref==0.1.2
RUN apt-get clean

EXPOSE 80

ADD . /g2e

CMD /g2e/boot.sh
