import pytest

import os.path as osp
import collections

from pipupgrade.model.project import Project, get_included_requirements
# imports - test imports
from testutils import PATH

def unordered_list_equal(a, b):
    return collections.Counter(a) == collections.Counter(b)

def test_project():
    with pytest.raises(ValueError):
        Project("foobar")

    path_project = PATH["PROJECT"]
    requirements = [
        osp.join(path_project, "requirements", "foobar.txt"),
        osp.join(path_project, "requirements-dev.txt"),
        osp.join(path_project, "requirements.txt")
    ]

    project = Project(path_project)
    assert project.path == path_project
    assert unordered_list_equal(project.requirements, requirements)

    project = Project(path_project, depth_search = True)
    assert unordered_list_equal(project.requirements,
        requirements + [osp.join(path_project, "folder", "requirements-recursive.txt")])

    assert project.pipfile == osp.join(path_project, "Pipfile")

    assert str(project) == "<Project %s>" % path_project

    project = Project.from_path(path_project)
    assert project.path == path_project

def test_get_included_requirements():
    path = osp.join(PATH["DATA"], "requirements-recursive.txt")
    assert get_included_requirements(path) == [
        osp.join(PATH["DATA"], "requirements-included.txt")
    ]