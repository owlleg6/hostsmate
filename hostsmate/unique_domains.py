class UniqueDomains:
    """A class that manages a set of unique blacklisted domain names.

    Attributes:
        unique_domains (set): A set containing the unique blacklisted domain
        names.

    Methods:
        add_domain(domain: str) -> None
        get_unique_domains() -> set[str]
        count_domains() -> int
    """
    unique_domains: set[str] = set()

    def add_domain(self, domain: str) -> None:
        """Add a domain name to the set of unique domains.

        Args:
            domain (str): The domain name to add.
        """
        self.unique_domains.add(domain)

    def get_unique_domains(self) -> set[str]:
        """Return the set of unique domain names."""
        return self.unique_domains

    def count_domains(self) -> int:
        """Return the number of unique domains."""
        return len(self.unique_domains)
