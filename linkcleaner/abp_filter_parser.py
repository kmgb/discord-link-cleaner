from dataclasses import dataclass
import re

# Ideally this should be as compatible as possible with existing blocking solutions
# This parser aims to bridge the gap between ABP filters (with removeparam) and this program
# Could make use of https://github.com/adblockplus/python-abp, but it felt too bloated for my needs.


@dataclass
class RemoveParamRule:
    domain_regex: re.Pattern
    params: list[str | re.Pattern]


# Ignores filters that don't include $removeparam
class AbpFilterParser:
    """
    Simple parser of AdBlockPlus-style filters.
    Ignores filter rules with no $removeparam
    """
    rules: dict[str, set[str]] = {}

    def load(self, file_obj):
        """
        Parse the filters from the file_obj and add it to the rules list
        """
        for line in file_obj.readlines():
            rule = self.parse_filter_line(line.strip())
            if rule:
                self.rules.setdefault(rule.domain_regex, set()).update(rule.params)

    def get_filter_list(self) -> list[RemoveParamRule]:
        ret = []

        for k, v in self.rules.items():
            ret.append(RemoveParamRule(k, v))

        return ret

    def parse_filter_line(self, content):
        """
        Parse a single filter line, returns a RemoveParamRule if success
        """
        if content.startswith("!"):
            return

        leftside, options = content.split("$")
        options = options.split(",")

        rule = RemoveParamRule(".*", [])

        # TODO: Support ||daraz.*$removeparam=/spm=|scm=|from=|keyori=|sugg=|search=|mp=|c=|^abtest|^abbucket|pos=|themeID=|algArgs=|clickTrackInfo=|acm=|item_id=|version=|up_id=|pvid=/
        # TODO: Support ||ups.xplosion.de/ctx?event_id=$removeparam  <-- Not sure what blank removeparam means, does it remove all?
        for o in options:
            kv = o.split("=", 1)
            if len(kv) != 2:
                continue

            k, v = kv

            if k == "removeparam":
                rule.params.append(interpret_string_or_regex(v))

        # Ignore site-specific filters for now
        if len(leftside) > 2 and leftside.startswith("||"):
            ls = leftside[2:]
            # TODO: Figure out if re.escape can help, it caused issues before
            ls = ls.replace("/", r"\/")     # Escape path separators
            ls = ls.replace("?", r"\?")     # Escape path separators
            ls = ls.replace("^", r"(?:\?|\/)")
            ls = ls.replace(".", r"\.")     # Escape the periods in the URL already
            ls = ls.replace("*", ".*")      # Change wildcard syntax to regex

            regex = r"(?:\.|^)" + ls
            rule.domain_regex = re.compile(regex)

        return rule


def interpret_string_or_regex(text) -> str | re.Pattern:
    if len(text) > 2 and text[0] == "/" and text[-1] == "/":
        return re.compile(text[1:-1])
    else:
        return text


def main():
    parser = AbpFilterParser()
    parser.load(open("general_url.txt"))
    parser.load(open("specific.txt"))

    print(parser.get_filter_list())


if __name__ == "__main__":
    main()
