import contextlib
import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from kafka import KafkaProducer

from config import Config

_logger = logging.getLogger(__name__)
_config = Config()


def _value_serializer(dict_value):
    json_value = json.dumps(dict_value)
    return json_value.encode('utf-8')


def _format_domain_to_url(domain):
    if 'http' in domain or 'https' in domain:
        return domain
    else:
        return f'http://{domain}'


def _ping_domain(domain, timeout=10):
    url = _format_domain_to_url(domain)
    response = requests.get(url, timeout=10)
    return {
        'url': url,
        'status_code': response.status_code,
    }


def _on_future_done(future):
    if future.done():
        _logger.info(f'Future job done successfully')
    else:
        _logger.info(f'Future job cancelled')


def _produce(thread_pool_executor, kafka_producer):
    futures = {
        thread_pool_executor.submit(_ping_domain, domain): domain
        for domain in _config.domains
    }

    for future in as_completed(futures):
        domain = futures[future]

        try:
            data = future.result()
        except requests.Timeout:
            _logger.warning('Reaching domain timed out', extra={'domain': domain})
        except Exception as exc:
            _logger.exception(f'Reaching domain failed', {'domain': domain}, exc_info=exc)
        else:
            kafka_producer.send(_config.topic, value=data)
            future.add_done_callback(_on_future_done)


def producer():
    _logger.info('Producer started')

    kafka_producer = KafkaProducer(
        bootstrap_servers=_config.brokers,
        value_serializer=_value_serializer,
        security_protocol=_config.security_protocol,
        ssl_certfile=_config.cert_file,
        ssl_keyfile=_config.key_file,
        ssl_cafile=_config.ca_file,
    )

    with contextlib.closing(kafka_producer):
        with ThreadPoolExecutor() as executor:
            while True:
                _logger.info('Ping round started')
                _produce(executor, kafka_producer)

                time.sleep(_config.produce_period_seconds)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    producer()
