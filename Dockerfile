FROM debian:stable

WORKDIR /usr/src

# Uname from Lambda container
# sysname='Linux', nodename='ip-10-37-47-226', release='4.4.51-40.60.amzn1.x86_64', 
# version='#1 SMP Wed Mar 29 19:17:24 UTC 2017', machine='x86_64'

RUN apt-get update
RUN apt-get -y install wget bzip2 gcc make xz-utils zlib1g-dev

# Install Python 3.6.1 
RUN wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tar.xz
RUN tar xf Python-3.6.1.tar.xz
RUN cd Python-3.6.1; ./configure ; make install
RUN export PATH=${PATH}:/usr/local/bin

# Install PostgreSQL 9.6.2
RUN wget https://ftp.postgresql.org/pub/source/v9.6.2/postgresql-9.6.2.tar.bz2
RUN tar jxvf postgresql-9.6.2.tar.bz2
WORKDIR /usr/src/postgresql-9.6.2/
RUN ./configure --without-zlib --without-readline; make install
WORKDIR /usr/src

# Psycopg 2.7
RUN wget http://initd.org/psycopg/tarballs/PSYCOPG-2-7/psycopg2-2.7b2.tar.gz
RUN tar zxvf psycopg2-2.7b2.tar.gz; 
WORKDIR /usr/src/psycopg2-2.7b2/
RUN sed -i 's/static_libpq = 0/static_libpq = 1/g' setup.cfg
RUN sed -i 's/pg_config =/pg_config = \/usr\/local\/pgsql\/bin\/pg_config/g' setup.cfg
RUN python3 setup.py build
