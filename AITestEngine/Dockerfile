FROM python:3.6.8
ENV DEBIAN_FRONTEND teletype
MAINTAINER nttdata
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils && apt-get install -y curl
RUN apt-get install libaio1 libaio-dev

#INSTALL ORACLE INSTANT CLIENT
RUN mkdir -p opt/instantclient
ADD ./instantclient /opt/instantclient
ENV LD_LIBRARY_PATH "/opt/instantclient"
RUN echo /opt/instantclient > /etc/ld.so.conf.d/oracle-instantclient.conf
RUN ldconfig



#SETUP ORACLE ENV VARIABLES AND START APP IN SHELL SCRIPT
ENV OCI_HOME /opt/instantclient
ENV OCI_LIB_DIR /opt/instantclient
ENV OCI_INCLUDE_DIR /opt/instantclient/sdk/include
ENV OCI_VERSION 18
RUN echo '/opt/instantclient/' | tee -a /etc/ld.so.conf.d/oracle_instant_client.conf
#RUN cd /opt/instantclient && ln -s /opt/instantclient/libclntsh.so.18.1 libclntsh.so && ln -s /opt/instantclient/libocci.so.18.1 libocci.so

WORKDIR /AITestEngine
COPY ./AITestEngine /AITestEngine
COPY ./nltk_data /root/nltk_data
COPY ./MODEL_DONT_OPEN /root/MODEL_DONT_OPEN
#COPY requirements.txt requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt