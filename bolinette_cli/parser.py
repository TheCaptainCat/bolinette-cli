import importlib
import sys

import yaml
from bolinette_common import paths, files

from bolinette_cli import Loader
from bolinette_cli.nodes import Node, Command


class Parser:
    def __init__(self):
        self.cwd = paths.cwd()
        self.origin = paths.dirname(__file__)
        self.blnt = Parser.pickup_blnt(paths.cwd())
        self.nodes = self.parse_nodes()

    def instance_path(self, *path):
        return self.root_path('instance', *path)

    def root_path(self, *path):
        return paths.join(self.cwd, *path)

    def internal_path(self, *path):
        return paths.join(self.origin, *path)

    def parse_nodes(self):
        with open(self.internal_path('nodes.yml')) as f:
            return Loader.load_nodes(yaml.safe_load(f))

    def execute(self, argv, cur_node=None, index=1):
        if index >= len(argv):
            return self.print_node_doc(argv[1:index], cur_node)
        nodes = self.nodes if cur_node is None else cur_node.children
        current = None
        for node in nodes:
            if node.name == argv[index]:
                current = node
        if current is not None:
            if isinstance(current, Node):
                return self.execute(argv, current, index + 1)
            elif isinstance(current, Command):
                self.parse_command(argv, current, index + 1)
                if self.check_command(current):
                    self.ask_params(current)
                    self.run_command(current)
        else:
            print('Invalid command: ' + ' '.join(argv[1:index + 1]))
            return self.print_node_doc(argv[1:index], cur_node)

    def print_node_doc(self, argv, node):
        if node is not None:
            nodes = node.children
        else:
            nodes = self.nodes
        if len(argv) > 0:
            print('Command: ' + ' '.join(argv))
            print('  Sub commands:')
        else:
            print('Commands:')
        for node in nodes:
            if hasattr(node, 'hidden') and node.hidden:
                continue
            if node.desc is not None:
                print(f'    - {node.name}: {node.desc}')
            else:
                print(f'    - {node.name}')

    def check_command(self, command):
        valid = True
        for inline in command.inline:
            if inline.value is None:
                text = f'Missing parameter: {inline.name}'
                if inline.desc is not None:
                    text += f' ({inline.desc})'
                print(text)
                valid = False
        return valid

    def ask_params(self, command):
        for ask in [a for a in command.ask if a.value is None]:
            text = ask.name
            if ask.desc is not None:
                text += f' ({ask.desc})'
            prompt = '$ '
            if ask.required:
                prompt = '<required> ' + prompt
            if ask.default is not None:
                prompt = f'<default: {ask.default}> ' + prompt
            while True:
                print(text)
                value = input(prompt)
                if not value and not ask.required:
                    break
                if not value and ask.default is not None:
                    value = ask.default
                if not not value:
                    break
            if not not value:
                ask.value = value

    def parse_command(self, argv, command, index):
        skip = False
        inline_index = 0
        while index < len(argv):
            current = argv[index]
            if current.startswith('--'):
                for arg in command.args + command.ask:
                    if current == '--' + arg.name:
                        if index + 1 < len(argv):
                            arg.value = argv[index + 1]
                            skip = True
                        else:
                            arg.missing = True
                for flag in command.flags:
                    if current == '--' + flag.name:
                        flag.value = True
            elif current.startswith('-'):
                for arg in command.args:
                    if current == '-' + arg.flag:
                        if index + 1 < len(argv):
                            arg.value = argv[index + 1]
                            skip = True
                        else:
                            arg.missing = True
                for flag in command.flags:
                    if current == '-' + flag.flag:
                        flag.value = True
            else:
                if inline_index < len(command.inline):
                    command.inline[inline_index].value = current
                    inline_index += 1
            index += 1
            if skip:
                index += 1
                skip = False

    def run_command(self, command):
        module = importlib.import_module('bolinette_cli.commands.' + command.command)
        func = getattr(module, command.command)
        params = {'parser': self}
        for param in command.inline + command.ask + command.flags + command.args:
            params[param.name] = param.value
        for param in command.params:
            params[param] = command.params[param]
        func(**params)

    @staticmethod
    def pickup_blnt(cwd):
        manifest = files.read_manifest(cwd)
        if manifest is not None:
            if cwd not in sys.path:
                sys.path = [cwd] + sys.path
            module = importlib.import_module(manifest.get('module'))
            blnt = getattr(module, 'bolinette', None)
            return blnt
        return None
