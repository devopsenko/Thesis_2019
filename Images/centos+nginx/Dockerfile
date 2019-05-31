# Our base image
FROM centos:centos7
MAINTAINER Ihor Matsapura <matsapura98@gmail.com>

# Installing the necessary software
RUN yum -y install epel-release
RUN yum -y install nginx && yum clean all

# Creating directory for nginx config files
RUN mkdir -p /etc/nginx/my-conf

# Adding option in nginx.conf
RUN sed -is '/^    include \/etc\/nginx\/conf.d\/\*.conf/a\ \ \ \ include /etc/nginx/my-conf/*.conf;' /etc/nginx/nginx.conf

# Running Nginx
CMD ["nginx", "-g", "daemon off;"]
