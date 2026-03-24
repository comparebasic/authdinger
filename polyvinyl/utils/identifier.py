class Ident(object):
    "Ident is a way to quickly describe an action <tag>@<base>.<ext>\n"
    "\n"
    "notes:\n"
    "  - source = <base>.<ext>\n"
    "  - a tag with no @ symbol is assigned to <tag>\n"
    "  - ident_s represents the original string\n"
    "  - if base is numerical it is assigned as an integer\n"


    def __init__(self, ident_s):
        self.ident = ident_s
        self.tag = None
        self.name = None
        self.location = None

        parts = ident_s.split("=")
        if len(parts) == 1:
            self.tag = ident_s
        elif len(parts) == 2:
            self.tag = parts[0]
            self.name = parts[1]

            eparts = parts[1].split('@')
            if len(eparts) == 1:
                self.name = eparts[0]
            elif len(eparts) == 2:
                self.name = eparts[0]
                self.location = eparts[1]
            elif len(eparts) > 0:
                self.name = eparts[0]
                self.location = eparts[1:]

            try:
                self.name = int(self.name) 
            except ValueError:
                pass
        else:
            raise TypeError(ident_s)
       

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Ident<{}={}@{}>".format(
            self.tag, self.name, self.location) 


def fuzzy_match(a, b):
    return (not a.tag or a.tag == b.tag) and \
        (not a.name or a.name == b.name) and \
        (not a.location or a.location == b.location)
