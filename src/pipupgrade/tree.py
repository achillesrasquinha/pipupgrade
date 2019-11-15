class Node:
    def __init__(self, obj, children = [ ]):
        self.obj        = obj
        self._children  = [ ]

        for child in children:
            self.add_child(child)

    @property
    def children(self):
        return getattr(self, "_children", [ ])

    @children.setter
    def children(self, value):
        if self.children == value:
            pass
        elif not isinstance(value, (list, tuple)):
            raise TypeError("Children must be of type (list, tuple), found %s"
                % type(value)
            )
        else:
            self._children = value

    def add_child(self, child):
        if not isinstance(child, Node):
            raise TypeError("Child must be of type Node, found %s" % type(child))

        self.children.append(child)

    def __repr__(self):
        repr_ = "<Node '%s'>" % str(self.obj)
        return repr_