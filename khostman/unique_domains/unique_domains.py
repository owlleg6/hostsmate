class UniqueDomains:
    unique_domains = set()

    def add_domain(self, domain: str) -> None:
        """Add a domain name to the set of unique domains.

        Args:
            domain (str): The domain name to add.

        Returns:
            None
        """
        self.unique_domains.add(domain)

    def get_unique_domains(self) -> set:
        """Return the set of unique domain names.

        Returns:
            set: The set of unique domain names.
        """
        return self.unique_domains
