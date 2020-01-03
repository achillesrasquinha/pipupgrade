def _render_tree(node, depth = 0, indent = 2, formatter = None):
    spacing     = (indent * " ") * depth
    formatted   = formatter(node.obj) if formatter else node.obj

    string      = "%s%s\n" % (spacing, formatted)

    for child in node.children:
        string += _render_tree(child, depth + 1,
            indent = indent, formatter = formatter)
    
    return string

def _check_node(node, query):
    result = False

    if callable(query):
        result = bool(query(node))
    else:
        result = node == query

    return result

class Node:
    def __init__(self, obj, children = [ ], parent = None):
        self.obj        = obj
        self._children  = [ ]

        for child in children:
            self.add_child(child)

        self._parent    = parent

    @property
    def parent(self):
        return getattr(self, "_parent", None)

    @parent.setter
    def parent(self, value):
        if self.parent == value:
            pass
        else:
            self._parent = value

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

    def empty(self):
        nchildren = len(self.children)
        return bool(nchildren)

    def add_child(self, child):
        if not isinstance(child, Node):
            child = Node(child, parent = self)

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

    def to_dict(self, repr_ = None):
        key   = repr_(self.obj) if repr_ else str(self.obj)
        dict_ = dict({
            key: [d.to_dict(repr_ = repr_) \
                for d in self.children]
        })

        return dict_

    def find(self, query):
        """
        Performs a Depth-First Search to find a Node based on a query provieded.
        """
        found = None

        if _check_node(self, query):
            found = self

        for child in self.children:
            if _check_node(child):
                found = child

        return found

    def flatten(self):
        pass