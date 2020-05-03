import platform

from bolinette_cli import console, paths, templating, versions


def init_app(parser, **options):
    manifest = paths.read_manifest(parser.cwd)
    origin = parser.internal_path('files')
    if manifest is not None:
        return console.error('Manifest file found, '
                             'it seems Bolinette has already been initialized!')
    api_name = options.get('name')
    api_desc = options.get('desc')
    api_module = options.get('module')

    console.print('Fetching latest Bolinette version...')
    blnt_version = versions.get_last_blnt_version()
    if blnt_version is None:
        console.error('\nCould not get Bolinette version from PyPI.org')
        blnt_version = input('Please provide the package version (like 0.0.0) $ ')
    console.print(f'* Using Bolinette {blnt_version}')

    params = {
        'secret_key': paths.random_string(64),
        'jwt_secret_key': paths.random_string(64),
        'module': api_module,
        'name': api_name,
        'desc': api_desc,
        'blnt_version': blnt_version
    }

    console.print('Copying file...')
    templating.render_directory(paths.join(origin, 'api'), parser.cwd, params)
    paths.rename(paths.join(parser.cwd, 'server'), paths.join(parser.cwd, api_module))
    console.print('* Done')

    if paths.exists(paths.join(parser.cwd, 'venv')):
        console.print('Installing packages...')
        platform_name = platform.system()
        command = None
        if platform_name == 'Linux':
            command = paths.join(parser.cwd, "venv", "bin", "python")
        elif platform_name == 'Windows':
            command = paths.join(parser.cwd, "venv", "Scripts", "python.exe")
        if command is not None:
            paths.run_command(
                f'{command} -m pip install -r requirements.txt',
                lambda line: console.print(f'> {line}'))
            console.print('* Done')
        else:
            console.error('* Unable to install pip dependencies')
