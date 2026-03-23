class Nav(object):
    def __init__(self, nav, lookup):
        self.lookup = lookup

    def __str__(self):
        return "Nav<{}>".format(self.lookup)


class NavItem(object):
    def __init__(self, name, path, idx, perms):
        self.name = name
        self.path = path
        self.idx = idx
        self.perms = perms

    def __str__(self):
        return "NavItem<{},{},{},{}>".format(self.name, self.path, self.idx, self.perms)

    def __repr__(self):
        return self.__str__()


def setup_nav(server):
    print("Setup Nav")
    nav = []
    lookup = {}
    perms = server.config["perms"]
    idx = 0
    for path, chain in server.routes.items():
        h = chain[0]
        first = h.ident

        if first.tag == "title" and first.location:
            lookup[path] = NavItem(first.location, path, idx, perms.get(path))
            idx += 1

    server.nav = Nav(nav, lookup)
    print(server.nav)
