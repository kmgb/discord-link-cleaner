import re
from furl import furl
from abp_filter_parser import AbpFilterParser, RemoveParamRule

URL_REGEX = re.compile(r"https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)")  # noqa: E501

PARAM_RULE_LIST: list[RemoveParamRule] = []
# Setup script
with open("general_url.txt") as f:
    parser = AbpFilterParser()
    parser.load(f)
    PARAM_RULE_LIST = parser.get_filter_list()


def find_urls(text) -> list[str]:
    return re.findall(URL_REGEX, text)


def clean_url(url):
    try:
        f = furl(url)
    except ValueError:
        return None

    # If it looks like a login URL, don't mess with it
    if f.username or f.password:
        return None

    # Remove params from matching urls
    for rule in PARAM_RULE_LIST:
        if re.match(rule.domain_regex, f.netloc):
            for p in rule.params:
                f.args.pop(p, default=0)

    return f.url


def remove_params(parsed_url, param_list):
    for p in param_list:
        parsed_url.args.pop(p, default=0)

    return parsed_url
