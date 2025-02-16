# Django Project
## Following Tutorial
## Set up Local Webserver
### Local Virtual Server / Port Forwarding
* [Startup Script](./startup.sh)
  * This script will create a required `.ps1` file that sets the port forwarding rules
  * These port forwarding rules are for the local windows machine ports to the local WSL ports
* The configuration to allow traffic to hit the running django app is within: [`settings.py`](./mysite/settings.py#L28)
  * We enable the public WAN IP of the local webserver as an `ALLOWED_HOSTS`
#### Local Virtual Server Config
* For the manual DHCP (reserved) IP for the local machine, we enable a port forwarding
  * The port forwarding is set for the manual DHCP IP
  * The external port is set to 8000 (HTTP)
  * The internal port is set to 8000 (HTTP)
  * Service name is HTTP(S)


## To Do
* Set up an Nginx Reverse Proxy
  * With this establish SSL Certificate / encryption
  * Configure Django to work with HTTPS