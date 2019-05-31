#!/usr/bin/python
# -*- coding: cp1251 -*-
import configparser, subprocess

config = configparser.ConfigParser()
config.read('/root/Docker/scripts/config.ini')

# Initialization of variables from config.ini
def InitVariables(sectionName): 
    SECTION = config[sectionName]
    global containerName
    containerName =      SECTION['ContainerName']
    global sitename
    sitename =           SECTION['Sitename']
    global ip
    ip =           	 SECTION['IP']
    global dockerImage
    dockerImage =        SECTION['DockerImage']
    global pathToConfig
    pathToConfig =       SECTION['PathToConfig']
    global pathToContent
    pathToContent =      SECTION['PathToContent']
    global pathToCert
    pathToCert =         SECTION['PathToCert']

# Function for running containers
def RunContainer(dockerImage, containerName, pathToContent, sitename, pathToConfig):
    # Print information about running container
    def PrintInfo():
        print ("Container's name: " + containerName)
        print ("Sitename: " + sitename)
        print ("Type of image: " + dockerImage)
        print("Status: " + subprocess.check_output("docker ps --format '{{.Status}}' -f name=" + containerName, shell=True).rstrip())
        print
    if (dockerImage == 'matsapura/cap'):
        print ("You successfully have run the container!")
        subprocess.call("docker run -d --name " + containerName + " -v " + pathToContent + ":/var/www/html/" + sitename + ":rw -v " + pathToConfig + ":/etc/httpd/my-conf:ro " + dockerImage, shell=True)
        PrintInfo()
    elif (dockerImage == 'matsapura/ca'):
        print ("You successfully have run the container!")
        subprocess.call("docker run -d --name " + containerName + " -v " + pathToContent + ":/var/www/html/" + sitename + ":rw -v " + pathToConfig + ":/etc/httpd/my-conf:ro " + dockerImage, shell=True)
        PrintInfo()
    elif (dockerImage == 'matsapura/cnp'):
        print ("You successfully have run the container!")
        subprocess.call("docker run -d --name " + containerName + " -v " + pathToContent + ":/var/www/html/" + sitename + ":rw -v " + pathToConfig + ":/etc/nginx/my-conf:ro " + dockerImage, shell=True)
        PrintInfo()
    elif (dockerImage == 'matsapura/cn'):
        print ("You successfully have run the container!")
        subprocess.call("docker run -d --name " + containerName + " -v " + pathToContent + ":/var/www/html/" + sitename + ":rw -v " + pathToConfig + ":/etc/nginx/my-conf:ro " + dockerImage, shell=True)
        PrintInfo()
    else:
        print "Try again"

# Creation HAProxy config based on containers data 
def CreateHAProxyConf(ip, containerName, sitename, j):
    dockerIP = subprocess.check_output("docker inspect --format '{{ .NetworkSettings.IPAddress }}' " + containerName, shell=True).rstrip()
    subprocess.call("sed -is '/^\ \ \ reqadd X-Forwarded-Proto:/a \ \ \ use_backend " + containerName + " if docker" + str(j) + "' /root/Docker/haproxy/haproxy.cfg", shell=True)
    subprocess.call("sed -is '/^\ \ \ reqadd X-Forwarded-Proto:/a \ \ \ acl docker" + str(j) + " hdr(host) -i " + sitename + " www." + sitename + " " + ip + "' /root/Docker/haproxy/haproxy.cfg", shell=True)    
    subprocess.call("echo >> /root/Docker/haproxy/haproxy.cfg", shell=True)
    subprocess.call("sed -is '$a backend " + containerName + "' /root/Docker/haproxy/haproxy.cfg", shell=True)
#    subprocess.call("sed -is '$a \ \ \ redirect scheme https if !{ ssl_fc }' /root/Docker/haproxy/haproxy.cfg", shell=True) # Redirect to 443 port
    subprocess.call("sed -is '$a \ \ \ balance leastconn' /root/Docker/haproxy/haproxy.cfg", shell=True)
    subprocess.call("sed -is '$a \ \ \ option httpclose' /root/Docker/haproxy/haproxy.cfg", shell=True)
    subprocess.call("sed -is '$a \ \ \ option forwardfor' /root/Docker/haproxy/haproxy.cfg", shell=True)
    subprocess.call("sed -is '$a \ \ \ server node" + str(j) + " " + str(dockerIP) + ":80 weight 1 check inter 2000 rise 2 fall 3' /root/Docker/haproxy/haproxy.cfg", shell=True)

# Run all functions
def RunAll():
    subprocess.call("rm -f /root/Docker/haproxy/haproxy.cfg", shell=True) # Restore default haproxy config
    subprocess.call("cp -f /root/Docker/haproxy/haproxy.cfg.save /root/Docker/haproxy/haproxy.cfg", shell=True)
    for j, section in enumerate(config.sections()):
        InitVariables(section)
        RunContainer(dockerImage, containerName, pathToContent, sitename, pathToConfig)
        CreateHAProxyConf(ip, containerName, sitename, j)
    print ("You successfully have run the HAProxy container!")
    subprocess.call("docker run -d --name haproxy -p 80:80 -p 443:443 -v /root/Docker/haproxy/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro -v /root/Docker/haproxy/certs/:/usr/local/etc/haproxy/certs/:ro matsapura/ha", shell=True)
    print("Container's name: haproxy")
    print(subprocess.check_output("docker ps --format 'Status: {{.Status}}' -f name=haproxy", shell=True).rstrip())
    print(subprocess.check_output("docker ps --format 'Ports: {{.Ports}}' -f name=haproxy", shell=True).rstrip())

# Remove all containers
def RemoveAll():
    subprocess.call("docker stop $(docker ps -a -q) && docker rm $(docker ps -a -q)", shell=True) # Remove all containers

#RemoveAll()
RunAll()
