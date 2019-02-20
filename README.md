# BeGoneAds

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/anned20/begoneads.svg)
![GitHub issues](https://img.shields.io/github/issues/anned20/begoneads.svg)
![GitHub pull requests](https://img.shields.io/github/issues-pr/anned20/begoneads.svg)
![GitHub](https://img.shields.io/github/license/anned20/begoneads.svg)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
![Awesome Badges](https://img.shields.io/badge/badges-awesome-green.svg)

BeGoneAds is a script that puts some popular hosts file lists into the systems hosts file as a adblocker measure.

## Getting started

Clone this repository:

```shell
git clone https://github.com/anned20/begoneads.git
```

Install the dependencies:

```shell
pip install -r requirements.txt
```

You are now ready to use BeGoneAds:

```shell
python begoneads.py
```

You should see something like:

```
Usage: begoneads.py [OPTIONS] COMMAND [ARGS]...

  Install or uninstall BeGoneAds, the host blocker for the system hosts
  file

Options:
  --help  Show this message and exit.

Commands:
  install    Install or update BeGoneAds
  uninstall  Uninstall BeGoneAds
```
## Sources of hosts data unified in this variant

Updated `hosts` files from the following locations are always unified and
included:

Host file source | Home page |
-----------------|:---------:|
Steven Black's ad-hoc list | [link](https://github.com/StevenBlack/hosts/blob/master/data/StevenBlack/hosts) |
Malware Domain List | [link](https://www.malwaredomainlist.com/) |
add.Dead | [link](https://github.com/FadeMind/hosts.extras) |
add.Spam | [link](https://github.com/FadeMind/hosts.extras) |
Dan Pollock | [link](https://someonewhocares.org/hosts/) |
MVPS hosts file | [link](http://winhelp2002.mvps.org/) |
yoyo.org | [link](https://pgl.yoyo.org/adservers/) |
Mitchell Krog's - Badd Boyz Hosts | [link](https://github.com/mitchellkrogza/Badd-Boyz-Hosts) |
CoinBlocker | [link](https://gitlab.com/ZeroDot1/CoinBlockerLists) |
UncheckyAds | [link](https://github.com/FadeMind/hosts.extras) |
add.2o7Net | [link](https://github.com/FadeMind/hosts.extras) |
KADhosts | [link](https://github.com/azet12/KADhosts) |
AdAway | [link](https://adaway.org/) |
add.Risk | [link](https://github.com/FadeMind/hosts.extras) |

## Testing

To run the tests you use [pytest](https://pytest.org)

Execute them with `pytest` in the project directory

## Built with

- [requests](http://docs.python-requests.org/en/master/) - Getting the webpage
- [click](https://github.com/mitsuhiko/click) - Parsing command line options
- [tqdm](https://github.com/tqdm/tqdm) - Showing a fancy progress bar

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
