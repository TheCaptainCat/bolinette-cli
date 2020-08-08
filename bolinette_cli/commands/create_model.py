from bolinette_common import console, paths, files
from bolinette_cli.commands.create_controller import create_controller
from bolinette_cli.commands.create_service import create_service


def create_model(parser, **options):
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
            'name': model_name,
            'class': class_name
        }

        files.render_and_write(paths.join(origin, 'model.py.jinja2'),
                               paths.join(path, 'models', f'{model_name}.py'), params)
        files.append(paths.join(path, 'models', '__init__.py'),
                     f'from {module}.models.{model_name} import {class_name}\n')

        if options.get('service', False):
            create_service(parser, name=model_name)

        if options.get('controller', False):
            create_controller(parser, name=model_name)
