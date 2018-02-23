import py


def test_disabled_by_default(plugin):
    extra_flags = {}
    assert not plugin.is_enabled(extra_flags)


def test_enabled_with_npm_flag(plugin):
    extra_flags = {"npm": True}
    assert plugin.is_enabled(extra_flags)


def npm_call(mock_call, folder, npm, *args):
    return mock_call([npm] + list(args), cwd=folder)


def assert_exact_calls(mock, expected_calls, **kwargs):
    mock.assert_has_calls(expected_calls, any_order=True)
    assert mock.call_count == len(expected_calls), "wrong number of subprocesses"


def test_build(plugin, builder, env_path, mock_popen_sleep, mock_call):
    plugin.on_before_build_all(builder)
    assert_exact_calls(mock_popen_sleep, [
        npm_call(mock_call, env_path / 'webpack', 'npm', 'install'),
        npm_call(mock_call, env_path / 'webpack', 'npm', 'run', 'build'),
        npm_call(mock_call, env_path / 'parcel', 'yarn', 'install'),
        npm_call(mock_call, env_path / 'parcel', 'yarn', 'run', 'dummy_build')
        ])
    assert not plugin.proc_manager


def test_build_fail(plugin, builder, env_path, mock_popen_fail, mock_call):
    plugin.on_before_build_all(builder)
    assert_exact_calls(mock_popen_fail, [
        npm_call(mock_call, env_path / 'webpack', 'npm', 'install'),
        npm_call(mock_call, env_path / 'parcel', 'yarn', 'install'),
        ])
    assert mock_popen_fail.call_count == 2
    assert not plugin.proc_manager


def test_build_wait_fail(plugin, builder, env_path, mock_popen_wait_fail, mock_call):
    plugin.on_before_build_all(builder)
    assert_exact_calls(mock_popen_wait_fail, [
        npm_call(mock_call, env_path / 'webpack', 'npm', 'install'),
        npm_call(mock_call, env_path / 'parcel', 'yarn', 'install'),
        ])
    assert mock_popen_wait_fail.call_count == 2
    assert not plugin.proc_manager


def test_watch(plugin, env_path, mock_popen_sleep, mock_call):
    plugin.on_server_spawn(extra_flags={"npm": True})
    plugin.proc_manager.wait()
    assert_exact_calls(mock_popen_sleep, [
        npm_call(mock_call, env_path / 'webpack', 'npm', 'install'),
        npm_call(mock_call, env_path / 'webpack', 'npm', 'run', 'dummy_watch'),
        npm_call(mock_call, env_path / 'parcel', 'yarn', 'install'),
        npm_call(mock_call, env_path / 'parcel', 'yarn', 'run', 'watch')
        ])

def test_watch_sleep(plugin, env_path, mock_popen_sleep, mock_call):
    plugin.on_server_spawn(extra_flags={"npm": True})
    assert plugin.proc_manager
    plugin.on_server_stop()
    assert mock_popen_sleep.call_count == 2
    assert not plugin.proc_manager


def test_build_plugin_disabled(plugin, builder, mock_popen):
    builder.extra_flags={}
    plugin.on_before_build_all(builder)
    mock_popen.assert_not_called()


def test_watch_plugin_disabled(plugin, mock_popen):
    plugin.on_server_spawn(extra_flags={})
    mock_popen.assert_not_called()
