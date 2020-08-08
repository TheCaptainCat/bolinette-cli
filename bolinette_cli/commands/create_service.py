from bolinette_common import console, files, paths
from bolinette_cli.commands.create_controller import create_controller


def create_service(parser, **options):
    manifest = files.read_manifest(parser.cwd)
    if manifest is None:
        console.error('No manifest found')
    else:
        module = manifest.get('module')
        path = parser.root_path(module)
        origin = parser.internal_path('files', 'templates')

        model_name = options.get('name').lower()
        class_name = model_name[0].upper() + model_name[1:]

        params = {
            'module': module,
            'name': model_name,
            'class': class_name
        }

        files.render_and_write(paths.join(origin, 'service.py.jinja2'),
                               paths.join(path, 'services', f'{model_name}.py'), params)
        files.append(paths.join(path, 'services', '__init__.py'),
                     f'from {module}.services.{model_name} import {model_name}_service\n')

        if options.get('controller', False):
            create_controller(parser, name=model_name)
