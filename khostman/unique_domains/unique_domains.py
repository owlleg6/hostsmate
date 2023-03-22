class UniqueDomains:
    unique_domains = set()

    def add_domain(self, domain):
        self.unique_domains.add(domain)

    def get_unique_domains(self):
        return self.unique_domains
