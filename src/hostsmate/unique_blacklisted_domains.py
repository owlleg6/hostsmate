class UniqueBlacklistedDomains:
    """A class that manages a set of unique blacklisted domain names
    with `0.0.0.0` prefix.

    Attributes:
        __unique_domains (set): A set containing the unique blacklisted domain
        names.

    Methods:
        add_domain(domain: str) -> None

    Properties:
        items (set[str]): A set containing the unique blacklisted domain names.
        amount (int): The length of the __unique_domains set.

    """
    __unique_domains: set[str] = set()
    __non_routable_ip: str = '0.0.0.0'

    def add_domain(self, domain: str) -> None:
        """Add a domain name with 0.0.0.0 prefix to the set of unique domains.

        Args:
            domain (str): The domain name to add.
        """
        if domain.startswith(self.__non_routable_ip):
            self.__unique_domains.add(domain)
        else:
            self.__unique_domains.add(
                f'{self.__non_routable_ip} {domain}'
            )

    @property
    def items(self) -> set[str]:
        """Return the set of unique domain names."""
        return self.__unique_domains

    @property
    def amount(self) -> int:
        """Return the number of unique domains."""
        return len(self.__unique_domains)
