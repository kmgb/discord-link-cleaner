import re
from furl import furl
from abp_filter_parser import AbpFilterParser, RemoveParamRule

URL_REGEX = re.compile(r"https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)")  # noqa: E501

PARAM_RULE_LIST: list[RemoveParamRule] = []
# Setup script
with open("general_url.txt") as f1, open("specific.txt") as f2:
    parser = AbpFilterParser()
    parser.load(f1)
    parser.load(f2)
    PARAM_RULE_LIST = parser.get_filter_list()


def find_urls(text) -> list[str]:
    return re.findall(URL_REGEX, text)


def clean_url(url):
    try:
        parsed_url = furl(url)
    except ValueError:
        return None

    # If it looks like a login URL, don't mess with it
    if parsed_url.username or parsed_url.password:
        return None

    # Remove params from matching urls
    for rule in PARAM_RULE_LIST:
        if re.search(rule.domain_regex, parsed_url.netloc + str(parsed_url.path)):
            for p in rule.params:
                parsed_url.args.pop(p, default=0)

    return parsed_url.url


def remove_params(parsed_url, param_list):
    for p in param_list:
        parsed_url.args.pop(p, default=0)

    return parsed_url
