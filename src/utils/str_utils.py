from urllib.parse import urlparse


class StringUtils:
    """
    A utility class that provides static methods for manipulating strings.

    Methods:
        strip_domain_prefix(url: str) -> str
        sep_num_with_commas(number: int) -> str:
    """

    @staticmethod
    def strip_domain_prefix(url: str) -> str:
        """
        Given a URL string, return the domain name with any leading protocol
        or "www." prefix removed.

        Args:
            url (str): The URL string to strip.

        Returns:
            str: The stripped domain name.
        """
        if urlparse(url).scheme:
            domain: str = urlparse(url).netloc.split(':')[0]
            if domain.startswith('www.'):
                return domain[4:]
            return domain
        else:
            domain: str = urlparse(url).path
            if domain.startswith('www.'):
                return domain[4:]
            return url

    @staticmethod
    def sep_num_with_commas(number: int) -> str:
        """
        Given an integer, return a string representation of the integer with
        commas separating each group of three digits.

        Args:
            number (int): The number to format.

        Returns:
            str: The formatted string representation of the number.
        """
        return "{:,}".format(number)
