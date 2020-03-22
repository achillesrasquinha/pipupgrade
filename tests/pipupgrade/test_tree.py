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