import os
import yaml


class Config:
    ENV_CONFIG = 'ISITUP_CONFIG_FILE'

    def __init__(self, config_file=None):
        if not config_file:
            config_file = self._get_config_file_from_env()

        with open(config_file) as fp:
            config = yaml.safe_load(fp)

        self.domains = self._parse_domains(config['domains'])
        self.produce_period_seconds = config['produce_period_seconds']
        self.brokers = config['brokers']
        self.topic = config['topic']

        self.database_uri = config['database_uri']
        self.table_name = config['table_name']
        self.polling_period_milliseconds = config['polling_period_milliseconds']

        self.security_protocol = config.get('security_protocol', 'PLAINTEXT')
        self.cert_file = config.get('cert_file', None)
        self.key_file = config.get('key_file', None)
        self.ca_file = config.get('ca_file', None)

    def _get_config_file_from_env(self):
        config_file = os.environ[Config.ENV_CONFIG]
        return config_file

    def _parse_domains_file(self, domains_file):
        with open(domains_file) as fp:
            domains = fp.read()
        domains = domains.split('\n')
        domains = filter(lambda domain: domain.strip(), domains)
        return list(domains)

    def _parse_domains(self, domains):
        if type(domains) is str:
            return self._parse_domains_file(domains)
        elif type(domains) is list:
            return domains
        return []
