def _render_tree(node, depth = 0, indent = 2, formatter = None):
    spacing     = (indent * " ") * depth
    formatted   = formatter(node.obj) if formatter else node.obj

    string      = "%s%s\n" % (spacing, formatted)

    for child in node.children:
        string += _render_tree(child, depth + 1,
            indent = indent, formatter = formatter)
    
    return string

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
            child = Node(child)

        self.children.append(child)

    def add_children(self, *children):
        for child in children:
            self.add_child(child)

    def __repr__(self):
        repr_ = "<Node '%s'>" % str(self.obj)
        return repr_

    def render(self, indent = 2, formatter = None):
        string = _render_tree(self, indent = indent, formatter = formatter)
        return string

    def to_dict(self, repr_ = None, object_key = "object"):
        dict_ = dict({
            object_key: repr_(self.obj) if repr_ else str(self.obj),
            "children": [
                d.to_dict(repr_ = repr_) for d in self.children
            ]
        })

        return dict_

    @staticmethod
    def from_dict(dict_, objectify = None, object_key = "object"):
        obj             = objectify(dict_[object_key] ) \
            if objectify else dict_[object_key]
        children        = dict_["children"]

        node            = Node(obj)
        node.children   = [Node.from_dict(child) for child in children]

        return node