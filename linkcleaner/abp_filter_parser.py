from dataclasses import dataclass
import re

SPLIT_UNESCAPED_COMMA_REGEX = re.compile(r"(?<!\\),")


@dataclass
class RemoveParamRule:
    domain_regex: re.Pattern
    params: list[str | re.Pattern]


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

        # TODO: Fix parsing with escaped '$' and ',' characters in
        # removeparam regular expressions
        leftside, options = content.split("$", 1)
        options = re.split(SPLIT_UNESCAPED_COMMA_REGEX, options)

        rule = RemoveParamRule(re.compile(".*"), [])

        for o in options:
            # De-escape the expression so we can interpret it
            o = re.sub(r"\\($|,|\/)", r"\1", o)
            kv = o.split("=", 1)

            # Special case of removeparam:
            # If there is no specified value, remove all parameters
            if len(kv) == 1 and kv[0] == "removeparam":
                rule.params.append(re.compile(".*"))
                continue

            if len(kv) != 2:
                continue

            k, v = kv
            if k == "removeparam":
                if res := parse_removeparam(v):
                    rule.params.extend(res)

        if len(leftside) > 2 and leftside.startswith("||"):
            ls = leftside[2:]
            # TODO: Figure out if re.escape can help, it caused issues before
            ls = ls.replace("/", r"\/")         # Escape path separators
            ls = ls.replace("?", r"\?")         # Escape path separators
            ls = ls.replace(".", r"\.")         # Escape the periods in the URL already
            ls = ls.replace("^", r"(?:\?|\/)")  # Change ABP separator to regex
            ls = ls.replace("*", r".*")         # Change wildcard syntax to regex

            regex = r"(?:\.|^)" + ls
            rule.domain_regex = re.compile(regex)

        # TODO: Handle exception filters (@@||filter)

        return rule


# TODO: Negated expressions with '~'
def parse_removeparam(v) -> list[str | re.Pattern]:
    # Check and extract if in regex form
    if m := re.fullmatch("/(.*)/(i)?", v):
        if len(m.groups()) == 3 and m.group(2) == "i":
            return [re.compile(m[1], flags=re.IGNORECASE)]
        else:
            return [re.compile(m[1])]
    else:
        return v.split("|")


def main():
    parser = AbpFilterParser()
    parser.load(open("general_url.txt"))
    parser.load(open("specific.txt"))

    print(parser.get_filter_list())


if __name__ == "__main__":
    main()
