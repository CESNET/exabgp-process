# ExaAPI application

This application needs to be hooked on ExaBGP daemon. 

Every time this app gets a new command, it replicates the command to the daemon through the stdout. The registered
daemon is watching the stdout of the ExaAPI service.

Add this to your ExaBGP config
```
process flowspec {
         run /usr/bin/python3 /home/deploy/www/exaapi/exa_api.py;
         encoder json;
    }
```
The prefered version is using RabbitMQ for message passing. 

For development and testing purposes, there is also a HTTP version. However there is no security layer in this web app. 
You should limit the access only from the localhost.

See [ExaBPG docs](https://github.com/Exa-Networks/exabgp/wiki/Controlling-ExaBGP-:-possible-options-for-process) for more information.


