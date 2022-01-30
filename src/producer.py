def get_domains(domain_list_file='domains.csv'):
    with open(domain_list_file) as fp:
        domains = fp.read()
    domains = domains.split('\n')
    domains = filter(lambda domain: domain.strip(), domains)
    return list(domains)


def producer():
    domains = get_domains()


if __name__ == '__main__':
    producer()
