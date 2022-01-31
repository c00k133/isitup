import os
import pytest
import yaml

from src.config import Config


@pytest.fixture
def default_config():
    return {
        'domains': ['domains0.com'],
        'produce_period_seconds': 10,
        'topic': 'PING',
        'brokers': [
           'kafka:9092',
        ],
        'database_uri': 'postgres://postgres:changeme@postgres:5432',
        'table_name': 'pings',
        'polling_period_milliseconds': 10000,
    }


@pytest.fixture
def default_domains():
    return [
        'domain1.com',
        'domain2.com',
    ]


def test_domains_from_file(default_domains, default_config, tmpdir):
    domains_file = tmpdir.join('domains.csv')
    domains_file.write('\n'.join(default_domains))

    config_data = {
        **default_config,
        'domains': domains_file.strpath,
    }
    config_file = tmpdir.join('config.yml')
    config_file.write(yaml.dump(config_data))

    config = Config(config_file.strpath)
    assert all(
        domain == default_domain
        for domain, default_domain
        in zip(config.domains, default_domains)
    )


def test_domains_from_array(default_domains, default_config, tmpdir):
    config_data = {
        **default_config,
        'domains': default_domains,
    }
    config_file = tmpdir.join('config.yml')
    config_file.write(yaml.dump(config_data))

    config = Config(config_file.strpath)
    assert all(
        domain == default_domain
        for domain, default_domain
        in zip(config.domains, default_domains)
    )


@pytest.fixture()
def setup_env_config_file(default_config, default_domains, tmpdir):
    config_data = {
        **default_config,
        'domains': default_domains,
    }
    config_file = tmpdir.join('config.yml')
    config_file.write(yaml.dump(config_data))

    old_environ = dict(os.environ)
    os.environ.update({
        Config.ENV_CONFIG: config_file.strpath,
    })

    yield
    os.environ.clear()
    os.environ.update(old_environ)


def test_config_from_env(setup_env_config_file, default_domains):
    config = Config()
    assert all(
        domain == default_domain
        for domain, default_domain
        in zip(config.domains, default_domains)
    )
