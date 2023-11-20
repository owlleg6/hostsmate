[![codecov](https://codecov.io/gh/kravchenkoda/hostsmate/branch/master/graph/badge.svg)](https://codecov.io/gh/kravchenkoda/hostsmate)
[![PyTest](https://github.com/kravchenkoda/hostsmate/actions/workflows/pytest.yml/badge.svg)](https://github.com/kravchenkoda/hostsmate/actions/workflows/pytest.yml)
# HostsMate


Welcome to HostsMate! A CLI tool for Unix-like operating systems that works with /etc/hosts file.

Protect yourself from malware, tracking, ads, and spam. HostsMate blocks over 1.2M domains from regularly updated sources to keep your system safe. Customize blacklist and whitelist sources, manually block or whitelist domains, suspend HostsMate if necessary.


## Installation


To install `hostsmate`, you can use `pip`. Make sure to run the installation command with `sudo` to be able to further run `hostsmate` with `sudo`, which is required.

```bash
sudo pip install hostsmate
```

To run tests as well, install `hostsmate` with dev dependencies:

```bash
sudo pip install hostsmate[dev]
```

## How to use


Always use `sudo` when running `hostsmate` to ensure that it has the necessary permissions to modify your system's hosts file.


Start `hostsmate` with `sudo hostsmate --run`.

`sudo hostsmate` or `sudo hostsmate -h` will show the help message:

```
usage: hostsmate [-h] [-R | -a | -s | -r | -b [backup-path] | -x [domain] |
 -w [domain] | -W [url] | -B [url] | -i [url] | -o [url]]

options:
  -h, --help            show this help message and exit
  -R, --run             parse domains from blacklist sources and start the HostsMate
  -a, --autorun         setup automatic update of your Hosts file (Linux and FreeBSD only)
  -s, --suspend         suspend HostsMate
  -r, --resume          resume HostsMate.
  -b [backup-dir], --backup [backup-dir]
                        create a backup of the existing Hosts file in the specific directory
  -x [domain], --blacklist-domain [domain]
                        blacklist specified domain
  -w [domain], --whitelist-domain [domain]
                        whitelist specified domain
  -W [url], --add-whitelist-source [url]
                        add URL with whitelisted domains to whitelist sources
  -B [url], --add-blacklist-source [url]
                        add URL with blacklisted domains to blakclist sources
  -i [url], --remove-whitelist-source [url]
                        remove URL with whitelisted domains from whitelist sources
  -o [url], --remove-blacklist-source [url]
                        remove URL with blacklisted domains from blacklist sources
```
## Usage details



* `--blacklist-domain`  option saves the specified domain to `user's custom domains` section of the Hosts file.
These domain names will be preserved when the Hosts file is updated.
            

* Using `--add-blacklist-source` and `--add-whitelist-source` options you can add URL containing a list of domains, 
it will be parsed, formatted, deduplicated and used in your Hosts file.
             

* While running `--suspend` option you need to manually enable it back with `--resume`.


* `--autorun` is implemented through `anacrontab` dependency which is available on Linux and FreeBSD, hence this feature is limited to these OS.                                  
Autorun frequency may be set to *daily*, *weekly* or *monthly*. Daily is recommended ;)
     

* All sources are being parsed concurrently, so it's faster than a lot of similar tools.              
                 
## Logs


A log file is created for every date `hostsmate` ran in `/var/logs/hostsmate` directory.

## License


This project is licensed under the terms of the [MIT License](https://github.com/kravchenkoda/hostsmate/blob/master/LICENSE).
