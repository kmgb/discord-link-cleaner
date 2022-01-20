import re
from furl import furl
from filter_parser import RemoveParamParser, RemoveParamRule
from orderedmultidict import omdict

URL_REGEX = re.compile(r"https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)")  # noqa: E501

PARAM_RULE_LIST: list[RemoveParamRule] = []
# Setup script
with open("general_url.txt") as f1, open("specific.txt") as f2:
    parser = RemoveParamParser()
    parser.parse_filterlist(f1)
    parser.parse_filterlist(f2)
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

    # Some filter rules depend on the path, some even depend on the arguments
    url_without_scheme = parsed_url.netloc + str(parsed_url.path)
    if parsed_url.query:
        url_without_scheme += "?" + str(parsed_url.query)

    # Remove params from matching urls
    for rule in PARAM_RULE_LIST:
        if re.search(rule.domain_regex, url_without_scheme):
            for p in rule.params:
                if isinstance(p, re.Pattern):
                    # Filter the parameters by regex and recreate the omdict
                    # allitems() returns a key-value pair for each iteration
                    parsed_url.args = omdict(filter(
                        lambda kv:
                            # TODO: Clean this up
                            # Tests the regex against the 'key=value' string if there's a value
                            # Just 'value' if there is no value.
                            not re.search(p, kv[0] + "="+kv[1]) if kv[1]
                            else not re.search(p, kv[0]),
                            parsed_url.args.allitems()
                    ))
                else:  # Simple string entry
                    # Remove non-regex entry
                    parsed_url.args.pop(p, default=0)

    return parsed_url.url


def remove_params(parsed_url, param_list):
    for p in param_list:
        parsed_url.args.pop(p, default=0)

    return parsed_url
