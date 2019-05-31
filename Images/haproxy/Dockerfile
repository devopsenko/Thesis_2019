# Our base image
FROM haproxy:1.7
MAINTAINER Ihor Matsapura <matsapura98@gmail.com>

# Creating variable
ENV HAPROXY_USER haproxy

# Adding haproxy user and group
RUN groupadd --system ${HAPROXY_USER} && \
    useradd --system --gid ${HAPROXY_USER} ${HAPROXY_USER} && \
    mkdir --parents /var/lib/${HAPROXY_USER} && \
    chown -R ${HAPROXY_USER}:${HAPROXY_USER} /var/lib/${HAPROXY_USER}

# Creating directory for certificates
RUN mkdir /usr/local/etc/haproxy/certs/

# Running haproxy process
CMD ["haproxy", "-db", "-f", "/usr/local/etc/haproxy/haproxy.cfg"]

