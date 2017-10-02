In the default webersprinkler configuration, external http access to the 
Raspberry Pi is used only by webersprinkler. Thus, all traffic is directed to 
webersprinkler/html and webersprinkler/app. In order for this to work, the 
default virtual host "000-default" must be disabled. Otherwise, all traffic is 
diverted according to /var/www according to the default virtual host's 
directives. 

Apache2 could be configured in other ways:
  A <VirtualHost> directive could redirect all traffic on a particular subdomain 
  to webersprinkler (subdomain.domain.com).

  An Alias directive could redirect all traffic under a specific directory to 
  webersprinkler (domain.com/webersprinkler).
