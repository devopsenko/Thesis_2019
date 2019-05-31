# Our base image
FROM centos:7
MAINTAINER Ihor Matsapura

# Installing the necessary software
RUN yum -y install httpd

# Creating directory for httpd config files
RUN mkdir -p /etc/httpd/my-conf

# Adding option in httpd.conf
RUN sed -is '$a IncludeOptional my-conf/*.conf' /etc/httpd/conf/httpd.conf

# Running httpd
CMD ["/usr/sbin/httpd", "-D", "FOREGROUND"]

