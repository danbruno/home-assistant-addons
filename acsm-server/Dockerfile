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
ADD calibre_plugin/*.py /calibre_plugin

WORKDIR /data

# Copy root filesystem
COPY rootfs /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
