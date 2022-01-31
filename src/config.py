import yaml


class Config:
    def __init__(self, config_file='config.local.yml'):
        with open(config_file) as fp:
            config = yaml.safe_load(fp)

        self.domains = self._parse_domains(config['domains'])
        self.produce_period_seconds = config['produce_period_seconds']
        self.brokers = config['brokers']
        self.topic = config['topic']

        self.database_uri = config['database_uri']
        self.table_name = config['table_name']
        self.polling_period_milliseconds = config['polling_period_milliseconds']

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
        # TODO: fail gracefully or report to user
        return []
