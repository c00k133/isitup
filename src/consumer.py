import contextlib
import json
import logging

import psycopg2
import psycopg2.extras
from kafka import KafkaConsumer

from config import Config

_logger = logging.getLogger(__name__)
_config = Config()


def _create_db_table(conn):
    table_name = _config.table_name
    with conn.cursor() as cursor:
        _logger.info('Creating table', extra={'table_name': table_name})
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                url VARCHAR NOT NULL,
                status_code INT NOT NULL
            );
        ''')

        conn.commit()


def _store_pings(conn, pings):
    table_name = _config.table_name
    sql_statement = f'''
        INSERT INTO {table_name} (
            url,
            status_code
        )
        VALUES %s
    '''

    with conn.cursor() as cursor:
        _logger.info('Storing %d pings', len(pings))
        psycopg2.extras.execute_values(cursor, sql_statement, pings)
        conn.commit()


def _parse_records_to_storeable_pings(records):
    return [
        [message.value['url'], message.value['status_code']]
        for messages in records.values()
        for message in messages
    ]


def _value_deserializer(value):
    json_value = value.decode('utf-8')
    return json.loads(json_value)


def consume():
    _logger.info('Consumer started')

    database_uri = _config.database_uri
    _logger.info('Connecting to database: %s', database_uri)
    with contextlib.closing(psycopg2.connect(database_uri)) as conn:
        _create_db_table(conn)

        _logger.info('Connect to Kafka on topic %s', _config.topic)
        kafka_consumer = KafkaConsumer(
            _config.topic,
            bootstrap_servers=_config.brokers,
            value_deserializer=_value_deserializer,
        )
        with contextlib.closing(kafka_consumer):
            while True:
                records = kafka_consumer.poll(
                    timeout_ms=_config.polling_period_milliseconds,
                    max_records=100
                )

                if records:
                    pings = _parse_records_to_storeable_pings(records)
                    _store_pings(conn, pings)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    consume()
