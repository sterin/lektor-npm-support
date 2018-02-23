import os
import py
import pytest
import time

from lektor.builder import Builder
from lektor.db import Database
from lektor.project import Project
from lektor.environment import Environment
from lektor_npm_support import NPMSupportPlugin


@pytest.fixture(scope='function')
def project():
    return Project.from_path(os.path.join(os.path.dirname(__file__), 'demo-project'))


@pytest.fixture(scope='function')
def env(project):
    return Environment(project)


@pytest.fixture(scope='function')
def pad(env):
    return Database(env).new_pad()


@pytest.fixture(scope='function')
def builder(tmpdir, pad):
    output_dir = str(tmpdir.mkdir("output"))
    return Builder(pad, output_dir, extra_flags=('npm',))


@pytest.fixture
def plugin(env):
    return NPMSupportPlugin(env, "npm-support")


@pytest.fixture
def mock_popen(mocker):
    return mocker.patch("lektor_npm_support.portable_popen", return_value=mocker.Mock(returncode=0))

@pytest.fixture
def mock_popen_fail(mocker):
    return mocker.patch("lektor_npm_support.portable_popen", return_value=mocker.Mock(returncode=1))

@pytest.fixture
def mock_popen_wait_fail(mocker):
    return mocker.patch("lektor_npm_support.portable_popen", return_value=mocker.Mock(wait=mocker.Mock(side_effect=OSError(1))))


@pytest.fixture
def mock_popen_sleep(mocker):
    def side_effect(*args, **kwargs):
        time.sleep(1)
        return mocker.DEFAULT
    return mocker.patch("lektor_npm_support.portable_popen", return_value=mocker.Mock(wait=mocker.Mock(side_effect=side_effect), returncode=0))


@pytest.fixture
def mock_call(mocker, *args, **kwargs):
    return mocker.call(*args, **kwargs)


@pytest.fixture
def env_path(env):
    return py.path.local(env.root_path)
