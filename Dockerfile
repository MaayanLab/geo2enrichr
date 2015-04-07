# docker -it -v ~/g2e:/app <image>

FROM debian:stable

RUN apt-get update

RUN apt-get -y install python
RUN apt-get -y install python-dev
RUN apt-get -y install python-pip
RUN apt-get -y install python-setuptools

RUN apt-get -y install apache2
RUN apt-get -y install apache2-prefork-dev
RUN pip install mod_wsgi

RUN pip install -Iv Flask==0.10.1
RUN pip install -Iv SQLAlchemy==0.9.9
RUN pip install -Iv mysql-connector-python==2.0.3
RUN pip install -Iv nose==1.3.4
RUN pip install -Iv numpy==1.9.2
RUN pip install -Iv requests==2.6.0
RUN apt-get -y install gfortran libopenblas-dev liblapack-dev
RUN pip install -Iv scipy==0.15.1
RUN pip install -Iv singledispatch==3.4.0.3
RUN pip install -Iv six==1.9.0
RUN pip install -Iv wsgiref==0.1.2
RUN apt-get -y install r-base r-base-dev
RUN apt-get -y install python-rpy2

#RUN mod_wsgi-express start-server wsgi.py --port=80 --user www-data --group www-data --server-root=/etc/app
#RUN /etc/app/apachectl start
