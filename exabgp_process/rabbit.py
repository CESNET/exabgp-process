#!/usr/bin/env python
"""
ExaBGP RabbitMQ API process
This module is process for ExaBGP
https://github.com/Exa-Networks/exabgp/wiki/Controlling-ExaBGP-:-possible-options-for-process

Each command received from the queue is send to stdout and captured by ExaBGP.
"""
import pika
import sys
import os
import json
from time import sleep


def api(user, passwd, queue, host, port, vhost, logger):

    def callback(ch, method, properties, body):
        body = body.decode("utf-8")
        route = json.loads(body)
        logger.info(body)
        sys.stdout.write("%s\n" % route["command"])
        sys.stdout.flush()

    while True:
        credentials = pika.PlainCredentials(user, passwd)

        parameters = pika.ConnectionParameters(
            host,
            port,
            vhost,
            credentials,
        )

        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue=queue)

        channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
            connection.close()
            print("\n[*] Interrupted - exiting")
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        except pika.exceptions.ConnectionClosedByBroker:
            sleep(15)
            continue
