import os
import configparser
from loguru import logger
import click
import exabgp_api.rabbit as rabbit
import exabgp_api.http as http


def generate_config_template():
    template = """
[api]
type = rabbitmq

[logging]
log_dir = /var/log/myapp    # Path where logs will be stored
log_file = myapp.log        # Log file name
log_format = %(asctime)s:  %(message)s    # Log format

[rabbitmq]
host = localhost            # RabbitMQ host address
port = 5672                 # RabbitMQ port
user = apiuser              # RabbitMQ user
password = securepassword   # RabbitMQ password
vhost = /                   # RabbitMQ virtual host
queue = apiqueue            # RabbitMQ queue name

[http]
host = localhost            # HTTP API host address
port = 5000                 # HTTP API port
    """
    return template


def load_config():
    config = configparser.ConfigParser()
    locations = [
        "api.conf",
        "/etc/exabgp_api/api.conf",
        "/etc/exabgp/api.conf",
        "/usr/local/etc/exabgp_api/api.conf",
    ]
    config.read(filenames=locations)  # Ensure this is in the correct location
    return config


@click.command()
@click.option("--generate-config", is_flag=True, help="Generate a configuration file")
def main(generate_config):
    """
    ExaBGP HTTP API process
    This module is process for ExaBGP
    https://github.com/Exa-Networks/exabgp/wiki/Controlling-ExaBGP-:-possible-options-for-process

    Each command received by API listener is send to stdout and captured by ExaBGP.
    API can be RabbitMQ (preffered) or HTTP. API type is defined in configuration file.
    """
    if generate_config:
        print(generate_config_template())
        return
    # Load configuration
    config = load_config()
    log_dir = config.get("logging", "log_dir", fallback="/var/log/exabgp_api")
    log_file = config.get("logging", "log_file", fallback="exabgp_api.log")
    logger.remove()
    logger.add(os.path.join(log_dir, log_file), rotation="1 week")

    api_type = config.get("api", "type", fallback="http")
    if api_type == "rabbit" or api_type == "rabbitmq":
        rabbit.api(
            user=config.get("rabbitmq", "user"),
            passwd=config.get("rabbitmq", "password"),
            queue=config.get("rabbitmq", "queue"),
            host=config.get("rabbitmq", "host"),
            port=config.get("rabbitmq", "port"),
            vhost=config.get("rabbitmq", "vhost"),
            logger=logger,
        )
    elif api_type == "http":
        http.api(
            host=config.get("http", "host", fallback="127.0.0.1"),
            port=config.get("http", "port", fallback=5000),
            logger=logger,
        )
    else:
        logger.error("API type not yet supported")


if __name__ == "__main__":
    main()
