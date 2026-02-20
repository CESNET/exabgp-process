#!/usr/bin/env python
"""
ExaBGP RabbitMQ API process
This module is process for ExaBGP
https://github.com/Exa-Networks/exabgp/wiki/Controlling-ExaBGP-:-possible-options-for-process

Each command received from the queue is send to stdout and captured by ExaBGP.
"""
import pika
import sys
import signal
import json
from time import sleep


def api(user, passwd, queue, host, port, vhost, logger):

    def callback(ch, method, properties, body):
        try:
            body = body.decode("utf-8")
            route = json.loads(body)
            command = route["command"]
            logger.info(body)
            sys.stdout.write("%s\n" % command)
            sys.stdout.flush()
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except (json.JSONDecodeError, KeyError, UnicodeDecodeError) as e:
            logger.error("Malformed message rejected: {} - {}", type(e).__name__, e)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            logger.error("Unexpected error processing message: {} - {}", type(e).__name__, e)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def shutdown(connection, channel):
        logger.info("Shutting down gracefully")
        try:
            channel.stop_consuming()
            connection.close()
        except Exception:
            pass
        sys.exit(0)

    while True:
        credentials = pika.PlainCredentials(user, passwd)

        parameters = pika.ConnectionParameters(
            host,
            port,
            vhost,
            credentials,
        )

        try:
            connection = pika.BlockingConnection(parameters)
        except pika.exceptions.AMQPConnectionError:
            logger.warning("RabbitMQ unavailable, retrying in 15 seconds")
            sleep(15)
            continue

        channel = connection.channel()

        channel.queue_declare(queue=queue)

        signal.signal(signal.SIGTERM, lambda sig, frame: shutdown(connection, channel))

        channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=False)

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            shutdown(connection, channel)
        except pika.exceptions.AMQPConnectionError:
            logger.warning("RabbitMQ connection lost, retrying in 15 seconds")
            sleep(15)
            continue
        except pika.exceptions.ConnectionClosedByBroker:
            logger.warning("Connection closed by broker, retrying in 15 seconds")
            sleep(15)
            continue
