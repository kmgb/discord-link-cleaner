import re
from typing import List
from furl import furl

URL_REGEX = re.compile(r"https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)")  # noqa: E501

GENERAL_TRACKER_LIST = []
# Setup script
with open("general_param_list.txt") as f:
    for param in f.readlines():
        GENERAL_TRACKER_LIST.append(param.rstrip())

print(GENERAL_TRACKER_LIST)


def find_urls(text) -> List[str]:
    return re.findall(URL_REGEX, text)


def clean_url(url):
    try:
        f = furl(url)
    except ValueError:
        return None

    # If it looks like a login URL, don't mess with it
    if f.username or f.password:
        return None

    # General filters
    f = remove_params(f, GENERAL_TRACKER_LIST)

    match f.netloc:
        case "www.amazon.ca" | "www.amazon.com":
            f = clean_amazon_url(f)

        case "store.steampowered.com":
            f = remove_params(f, ["snr"])

        case "twitter.com":
            f = remove_params(f, ["ref_src", "ref_url"])

    return f.url


def remove_params(parsed_url, param_list):
    for p in param_list:
        if p in parsed_url.args:
            del parsed_url.args[p]

    return parsed_url


def clean_amazon_url(parsedurl):
    path = str(parsedurl.path)

    # Don't clean up non-product pages
    if ("/dp/" not in path
            and not path.startswith("/events/")
            and not (path.endswith("/b") or "/b/" not in path)):
        return None

    # Amazon.com has a faux-parameter /ref=XX at the end of its paths
    # Remove that from the path
    if parsedurl.path.segments:
        lastsegment = parsedurl.path.segments[-1]
        if lastsegment.startswith("ref="):
            parsedurl.path.remove(lastsegment)

    # Special case: node parameters are important for identifying categories
    node_value = parsedurl.args.get("node")

    parsedurl.args.load("")  # Parameters on these pages are all trackers

    if node_value:
        parsedurl.args["node"] = node_value

    return parsedurl
