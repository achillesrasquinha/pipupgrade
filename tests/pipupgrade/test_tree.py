# imports - test imports
import pytest

# imports - module imports
from pipupgrade.tree    import Node

def test_node():
    tree1 = Node("foo")
    assert tree1.empty == True
    assert tree1 == Node("foo")

    assert str(tree1) == "<Node 'foo'>"

    assert tree1.render() == \
"""\
foo
"""

    tree2 = Node("foo", children = ["bar", "baz"])
    assert tree2.parent == None
    assert tree2 != Node("foo", children = ["bar", "baz", "boo"])
    assert Node("foo", children = ["bar", "baz"]) \
        == Node("foo", children = ["bar", "baz"])
    assert not Node("foo", children = ["bar", "baz"]) \
            == Node("foo", children = ["baz", "boo"])

    assert tree2.render() == \
"""\
foo
  bar
  baz
"""

    assert tree2.render(indent = 4) == \
"""\
foo
    bar
    baz
"""

    assert tree2.render(indent = 4, formatter = lambda x: "* %s" % x) == \
"""\
* foo
    * bar
    * baz
"""
    assert      tree2.find(lambda x: x.obj == "foo")
    assert      tree2.find(lambda x: x.obj == "bar")
    assert not  tree2.find(lambda x: x.obj == "foobaz")

    tree3 = Node("foo")
    tree3.add_children(["bar", "baz"])

    tree4           = Node("foo")
    tree4.children  = ["bar", "baz"]

    with pytest.raises(TypeError):
        tree4.children = "bar"

    """
    foo
        -> bar
            -> baz
            -> boo
        -> boo
            -> bar
            -> foo
    """
    tree5 = Node("foo")
    node1 = Node("bar", ["baz", "boo"])
    node2 = Node("boo", ["bar", "foo"])
    tree5.add_children(node1, node2)
    assert tree5.find(node2) == node2
    tree5.to_json() == dict(
        foo = dict(
            bar = dict(baz = None, boo = None),
            boo = dict(bar = None, foo = None),
        )
    )

    assert hash(tree5) == id(tree5)

    tree6    = Node("foo")
    children = [Node("bar"), Node("baz")] 
    tree6.add_children(*children)
    tree6.children = children
    assert tree6.children == children

    tree7    = Node("foo")
    tree8    = Node("bar")
    tree8.parent = tree7
    assert tree8.parent == tree7
    tree8.parent = tree7
    assert tree8.parent == tree7