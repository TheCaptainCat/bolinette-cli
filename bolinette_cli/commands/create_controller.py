from bolinette_common import console, files, paths


def create_controller(parser, **options):
    manifest = files.read_manifest(parser.cwd)
    if manifest is None:
        console.error('No manifest found')
    else:
        module = manifest.get('module')
        path = parser.root_path(module)
        origin = parser.internal_path('files', 'templates')

        model_name = options.get('name')

        params = {
            'module': module,
            'name': model_name
        }

        files.render_and_write(paths.join(origin, 'controller.py.jinja2'),
                               paths.join(path, 'controllers', f'{model_name}.py'), params)
        files.append(paths.join(path, 'controllers', '__init__.py'),
                     f'from {module}.controllers.{model_name} import ns as {model_name}_namespace\n')
