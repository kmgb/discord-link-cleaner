from dataclasses import dataclass

# Ideally this should be as compatible as possible with existing blocking solutions
# This parser aims to bridge the gap between ABP filters (with removeparam) and this program
# Could make use of https://github.com/adblockplus/python-abp, but it felt too bloated for my needs.


@dataclass
class RemoveParamRule:
    domain_regex: str
    params: list[str]


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

        for o in options:
            k, v = o.split("=")
            if k == "removeparam":
                rule.params.append(v)
            if k == "domain":
                return None  # Ignore site-specific filters

        # Ignore site-specific filters for now
        if leftside:
            return None  # TODO: do something about ||, @@|| and domain names

        return rule


def main():
    parser = AbpFilterParser()
    parser.load(open("general_url.txt"))

    print(parser.get_filter_list())


if __name__ == "__main__":
    main()
