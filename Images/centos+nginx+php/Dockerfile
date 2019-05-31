# Our base image
FROM centos:centos7
MAINTAINER Ihor Matsapura

RUN yum -y install epel-release

# Installing the necessary software
RUN yum -y install nginx php php-gd php-devel php-xml php-fpm supervisor && yum clean all

# Creating directory for nginx config files
RUN mkdir -p /etc/nginx/my-conf/

# Adding option in nginx.conf
RUN sed -is '/^    include \/etc\/nginx\/conf.d\/\*.conf/a\ \ \ \ include /etc/nginx/my-conf/*.conf;' /etc/nginx/nginx.conf

# Adding supervisord.conf to container
ADD supervisord.conf /etc/supervisord.conf

# Running supervisord
CMD ["/usr/bin/supervisord", "-n", "-c",  "/etc/supervisord.conf"]
