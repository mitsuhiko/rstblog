from setuptools import setup

setup(
    name='rstblog',
    version='1.0',
    author='Armin Ronacher <armin.ronacher@active-4.com>',
    packages=['rstblog', 'rstblog.modules'],
    description='',
    long_description='',
    license='BSD License',
    include_package_data=True,
    entry_points = {
        'console_scripts': ['run-rstblog = rstblog.cli:main'],
    },
    install_requires=['PyYAML', 'Babel', 'blinker', 'docutils', 'Jinja2>=2.4', 'Werkzeug']
)
