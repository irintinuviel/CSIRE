import concurrent.futures
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
import stomp
import json
import os
import logging
from lxml import etree

nsmap = {
    "u1": "urn:pl:oire:unk_6_1_1_1:v1",
    "u5": "urn:pl:oire:unk_6_1_1_5:v1",
    "u7": "urn:pl:oire:unk_7_1_1_4:v1",
    "u2": "urn:pl:oire:unk_6_2_1_1:v1",
    "t": "urn:pl:oire:technical:v1"
}

def load_config(file):
    with open(file, 'r') as f:
        return json.load(f)

def init_logging(log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def send_file_to_queue(config, file):
    hostname, port = parse_broker_url(config['brokerurl'])
    conn = stomp.Connection([(hostname, port)])
    conn.connect(config['username'], config['password'], wait=True)

    if os.path.isfile(file):
        with open(file, 'r') as f:
            message = f.read()
            try:
                xml_root = etree.fromstring(message)
                jms = xml_root.xpath('//t:MessageId/text()', namespaces=nsmap)[0]

                headers = {
                    'JMSCorrelationID': jms,
                }

                conn.send(body=message, destination=config['queue'], headers=headers)
                logging.info(f'Sent file {f} to queue')
            except Exception as e:
                logging.error(f'Error sending file {f}: {e}')
    conn.disconnect()


def parse_broker_url(brokerurl):
    parts = brokerurl.replace('tcp://', '').split(':')
    return parts[0], int(parts[1])


class MyListener(stomp.ConnectionListener):
    def __init__(self, output_folder):
        self.conn = None
        self.output_folder = output_folder

    def on_message(self, frame):
        message_content = frame.body
        file_name= frame.headers.get('correlation-id')
        print(file_name)
        file_path = os.path.join(self.output_folder, f"{file_name}.xml")

        with open(file_path, 'w') as f:
            f.write(message_content)


def get_messages_from_queue(queue_name, config, output_folder):
    hostname, port = parse_broker_url(config['brokerurl'])
    conn = stomp.Connection([(hostname, port)])
    listener = MyListener(output_folder)
    listener.conn = conn
    conn.set_listener('', listener)

    conn.connect(config["username"], config["password"], wait=True)

    conn.subscribe(destination=queue_name, id=1, ack='auto')
    while True:
        time.sleep(1)
