from utils.str_utils import StringUtils
import pytest


@pytest.fixture
def string_utils():
    return StringUtils()


@pytest.mark.parametrize(
    'domain, expected', [
        ('www.example.com', 'example.com'),
        ('https://website.com', 'website.com'),
        ('www.example.com.au', 'example.com.au'),
        ('ftp://example.com.au', 'example.com.au')
    ]
)
def test_strip_domain_prefix(string_utils, domain, expected):
    assert string_utils.strip_domain_prefix(domain) == expected


@pytest.mark.parametrize(
    'number, expected', [
        (120, '120'),
        (15242, '15,242'),
        (150500, '150,500'),
        (2560300, '2,560,300')
    ]
)
def test_sep_num_with_commas(string_utils, number, expected):
    assert string_utils.sep_num_with_commas(number) == expected
