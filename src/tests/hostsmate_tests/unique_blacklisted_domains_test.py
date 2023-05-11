import pytest

from hostsmate_src.unique_blacklisted_domains import UniqueBlacklistedDomains


domains_with_0000_prefix_to_add: set[str] = {
    '0.0.0.0 example.com',
    '0.0.0.0 foo.bar',
    '0.0.0.0 foo.bar.zar'
}

pure_domains_to_add: set[str] = {
    'example-foo-bar.com',
    'foo.bar',
    'foo.bar.zar'
}


@pytest.mark.parametrize('domain_to_add', domains_with_0000_prefix_to_add)
def test_add_domain_with_0000_prefix(domain_to_add: str):
    blacklisted_domains = UniqueBlacklistedDomains()
    blacklisted_domains.add_domain(domain_to_add)
    assert domain_to_add in blacklisted_domains.items


@pytest.mark.parametrize('domain_to_add', pure_domains_to_add)
def test_add_domain_without_0000_prefix(domain_to_add: str):
    blacklisted_domains = UniqueBlacklistedDomains()
    blacklisted_domains.add_domain(domain_to_add)
    assert f'0.0.0.0 {domain_to_add}' in blacklisted_domains.items
