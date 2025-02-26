# ExaBGP Process Package

This application is a simple API that interfaces with the [ExaBGP service](https://github.com/Exa-Networks/exabgp/tree/main).

Each time this app receives a new command, it forwards the command to ExaBGP via stdout. The registered ExaBGP service monitors the stdout of this API application.

### Installation
You can install the package using pip:
```
pip install exabgp_process
```

### Configuration
Generate the configuration file and copy it to `/etc/exabgp/process.conf`. Be sure to set up the log directory and file in the config, and ensure the directory exists and is writable by the ExaBGP process:
```
exabgp-process --generate-config >> process.conf
mv process.conf /etc/exabgp/process.conf
```

### Add to ExaBGP Configuration
Include the following in your ExaBGP configuration:
```
process flowspec {
    run /usr/local/exabgp-process;
    encoder json;
}
```

The preferred setup uses RabbitMQ for message passing.

### Development and Testing
For development and testing, there is also an HTTP version available. However, please note that this web app lacks any security layer. Therefore, it's recommended to restrict access to localhost only.

For more information, refer to the [ExaBGP documentation](https://github.com/Exa-Networks/exabgp/wiki/Controlling-ExaBGP-:-possible-options-for-process).


### Changelog
1.0.4 - fixed template for config file
1.0.3 - new format of message from server - json with keys: author, source, command. Author and source are for logging purposes, command is send to the process.
1.0.2 - switch to pyproject.toml for better description
