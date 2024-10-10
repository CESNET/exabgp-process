# ExaAPI application

This application is simple API process for [ExaBGP service](https://github.com/Exa-Networks/exabgp/tree/main). 

Every time this app gets a new command, it replicates the command to the ExaBPG through the stdout. The registered service is watching the stdout of this API app.

Install with pip
```
pip install exabgp_api
```
Generate and setup the config file and then copy the config to /etc/exabgp/api.conf.
Setup log dir and file in the config and make sure, that dir exists and its writable for ExaBGP process.
```
exabgp-api --generate-config >> api.conf
mv api.conf /etc/exabgp/api.conf
```

Add this to your ExaBGP config
```
process flowspec {
         run /usr/local/exabgp-api;
         encoder json;
    }
```
The prefered version is using RabbitMQ for message passing. 

For development and testing purposes, there is also a HTTP version. However there is no security layer in this web app.  You should limit the access only from the localhost.

See [ExaBPG docs](https://github.com/Exa-Networks/exabgp/wiki/Controlling-ExaBGP-:-possible-options-for-process) for more information.


