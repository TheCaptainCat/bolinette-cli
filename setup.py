from bolinette_common import paths, files
from setuptools import setup, find_packages


def project_packages(module):
    return [m for m in find_packages() if m.startswith(module)]


setup(
    name='Bolinette-CLI',
    packages=project_packages('bolinette_cli'),
    include_package_data=True,
    version=files.read_version(paths.dirname(__file__)),
    license='MIT',
    description='The Bolinette CLI, useful commands for your Bolinette API',
    author='Pierre Chat',
    author_email='pierrechat89@hotmail.fr',
    url='https://github.com/TheCaptainCat/bolinette-cli',
    keywords=['Flask', 'Bolinette', 'Web', 'Framework'],
    install_requires=files.read_requirements(paths.cwd()),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    setup_requires=[
        'wheel'
    ],
    entry_points={
        'console_scripts': [
            'blnt=bolinette_cli:main'
        ]
    },
)
