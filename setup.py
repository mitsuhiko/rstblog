from setuptools import setup

setup(
    name='rstblog',
    version='1.0',
    author='Armin Ronacher <armin.ronacher@active-4.com>',
    packages=['rstblog', 'rstblog.modules'],
    description='',
    long_description='',
    license='BSD License',
    entry_points = {
        'console_scripts': ['run-rstblog = rstblog.cli:main'],
    },
    package_data={
        'rstblog': ['templates/*.html', 'templates/blog/*.html']
    },
    install_requires=['PyYAML', 'Babel', 'blinker', 'Jinja2']
)
