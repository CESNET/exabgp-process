import os
import configparser
from loguru import logger
import click
import exabgp_process.rabbit as rabbit
import exabgp_process.http as http


# @TODO move comments to extra lines
def generate_config_template():
    template = """
[api]
type = rabbitmq

[logging]
# Path where logs will be stored
log_dir = /var/log/myapp
# Log file name
log_file = myapp.log
# Log format
log_format = %(asctime)s:  %(message)s

[rabbitmq]
# RabbitMQ host address
host = localhost
# RabbitMQ port
port = 5672
# RabbitMQ user
user = apiuser
# RabbitMQ password
password = securepassword
# RabbitMQ vhost
vhost = /
# RabbitMQ queue name
queue = apiqueue

[http]
# HTTP API host address
host = 0.0.0.0
# HTTP API port
port = 5000
    """
    return template


def load_config():
    config = configparser.ConfigParser()
    locations = [
        "api.conf",
        "process.conf",
        "/etc/exabgp_process/process.conf",
        "/etc/exabgp/process.conf",
        "/usr/local/etc/exabgp_process/process.conf",
    ]
    config.read(filenames=locations)  # Ensure this is in the correct location
    return config


@click.command()
@click.option("--generate-config", is_flag=True, help="Generate a configuration file")
def main(generate_config):
    """
    ExaBGP process
    This module is process for ExaBGP
    https://github.com/Exa-Networks/exabgp/wiki/Controlling-ExaBGP-:-possible-options-for-process

    Each command received by this listener is send to stdout and captured by ExaBGP.
    The process is either RabbitMQ (preffered) or HTTP. API type is defined in configuration file.
    """
    if generate_config:
        print(generate_config_template())
        return
    # Load configuration
    config = load_config()
    log_dir = config.get("logging", "log_dir", fallback="/var/log/exabgp")
    log_file = config.get("logging", "log_file", fallback="exabgp_process.log")
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
