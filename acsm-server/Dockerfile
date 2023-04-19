# syntax=docker/dockerfile:1

ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for add-on
RUN \
  apk add --no-cache \
    python3 py3-pip \
    && pip3 install pycryptodomex lxml cherrypy oscrypto

# Execute during the build of the image
ADD *.py /
ADD run.sh /

RUN sed -i '/^default = default_sect/a legacy = legacy_sect' /etc/ssl/openssl.cnf
#RUN sed -i '/^\[default_sect\]/a activate = 1' /etc/ssl/openssl.cnf
RUN echo "[legacy_sect]" >> /etc/ssl/openssl.cnf
RUN echo "activate = 1" >> /etc/ssl/openssl.cnf

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
