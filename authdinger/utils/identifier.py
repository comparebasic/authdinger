class Ident(object):
    "Ident is a way to quickly describe an action <tag>@<base>.<ext>\n"
    "\n"
    "notes:\n"
    "  - source = <base>.<ext>\n"
    "  - a tag with no @ symbol is assigned to <tag>\n"
    "  - ident represents the original string\n"
    "  - if base is numerical it is assigned as an integer\n"


    def __init__(self, ident):

        self.ident = ident
        self.tag = None
        self.name = None
        self.location = None

        parts = ident.split("=")
        if len(parts) == 1:
            self.tag = ident
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
            raise TypeError(ident)
       

    def __str__(self):
        return "Ident<{}={}@{}>".format(
            self.tag, self.name, self.location) 
