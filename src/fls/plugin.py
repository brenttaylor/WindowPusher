import importlib
import os
import sys

_loaded_plugins = []


def load_plugin(file_path):
    lp_position = len(_loaded_plugins)
    file_path = file_path.split('/')
    sys.path.append(os.path.abspath('/'.join(file_path[:-1])))
    ext = -3 if file_path[-1].lower().endswith(".py") else -4 if file_path[-1].lower().endswith(".pyc") else 0
    importlib.import_module(file_path[-1][:ext] if ext < 0 else file_path[-1])
    return tuple(_loaded_plugins[lp_position:])


def load_plugin_directory(directory_path):
    lp_position = len(_loaded_plugins)
    for plugin in os.listdir(directory_path):
        load_plugin(plugin)
    return tuple(_loaded_plugins[lp_position:])


def get_plugins(base_type=None):
    if base_type is None:
        return tuple(_loaded_plugins)
    plugins = []
    for plugin in _loaded_plugins:
        if base_type in type(plugin).__bases__:
            plugins.append(plugin)
    return tuple(plugins)


class PluginType(type):
    def __init__(cls, name, bases, attrs):
        super(PluginType, cls).__init__(name, bases, attrs)
        if name is not "BasePlugin":
            _loaded_plugins.append(cls())


class BasePlugin(object):
    __metaclass__ = PluginType



