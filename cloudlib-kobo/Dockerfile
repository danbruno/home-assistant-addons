# syntax=docker/dockerfile:1

ARG BUILD_FROM
FROM $BUILD_FROM

# Install Python packages on system level
ENV PIP_BREAK_SYSTEM_PACKAGES=1

# Install requirements for add-on
RUN \
  apk add --no-cache \
    python3 py3-pip
    && pip3 install cherrypy cherrypy_jinja2 configparser requests

RUN mkdir -p /templates

# Execute during the build of the image
ADD *.py /
ADD templates/*.html /templates/
ADD run.sh /

RUN sed -i '/^default = default_sect/a legacy = legacy_sect' /etc/ssl/openssl.cnf
RUN sed -i '/^\[default_sect\]/a activate = 1' /etc/ssl/openssl.cnf
RUN echo "[legacy_sect]" >> /etc/ssl/openssl.cnf
RUN echo "activate = 1" >> /etc/ssl/openssl.cnf

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
