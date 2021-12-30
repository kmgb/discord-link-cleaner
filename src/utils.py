import re
from typing import List
from furl import furl

# Regex by @diegoperini
URL_REGEX = re.compile(r"https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)")  # noqa: E501
AMAZON_PRODUCT_REGEX = re.compile(r"")


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

    match f.netloc:
        case "www.amazon.ca" | "www.amazon.com":
            return clean_amazon_url(f)

        case "twitter.com":
            return remove_params(f, ["ref_src", "ref_url"])

        case _:
            return None


def remove_params(parsed_url, param_list):
    for p in param_list:
        if p in parsed_url.args:
            del parsed_url.args[p]

    return parsed_url.url


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

    return parsedurl.url
