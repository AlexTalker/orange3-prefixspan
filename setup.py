#!/usr/bin/env python

from setuptools import setup, find_packages
from distutils.extension import Extension
from os import path

VERSION = '0.0.1'

ENTRY_POINTS = {
    'orange3.addon': (
        'sequence = orangecontrib.sequence',
    ),
    # Entry point used to specify packages containing tutorials accessible
    # from welcome screen. Tutorials are saved Orange Workflows (.ows files).
    'orange.widgets.tutorials': (
        # Syntax: any_text = path.to.package.containing.tutorials
    ),

    # Entry point used to specify packages containing widgets.
    'orange.widgets': (
        # Syntax: category name = path.to.package.containing.widgets
        # Widget category specification can be seen in
        #    orangecontrib/datafusion/widgets/__init__.py
        'Sequence = orangecontrib.sequence.widgets',
    ),

    # Register widget help
    "orange.canvas.help": (
        #'html-index = orangecontrib.associate.widgets:WIDGET_HELP_PATH',
    ),
}

def do_setup():
    setup(
        name="Orange3-Sequence",
        description="Orange add-on for mining sequence patterns.",
        #long_description=open(path.join(path.dirname(__file__), 'README.rst')).read(),
        version=VERSION,
        author='Rostock University',
        author_email='alextalker@yandex.ru',
        #url='https://github.com/biolab/orange3-associate',
        keywords=(
            'frequent itemset mining',
            'sequence pattern mining',
            'prefixspan',
            'frequent patterns',
            'FIM', 'FPM',
            'orange3 add-on',
        ),
        packages=find_packages(),
        package_data={
        #    "orangecontrib.associate.widgets": ["icons/*.svg"],
        },
        entry_points=ENTRY_POINTS,
        install_requires=[
            'prefixspan',
        ],
        namespace_packages=['orangecontrib'],
        classifiers=[
            'Programming Language :: Python',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Operating System :: OS Independent',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Intended Audience :: Education',
            'Intended Audience :: Science/Research',
            'Intended Audience :: Developers',
        ],
        zip_safe=False,
    )


if __name__ == '__main__':
    do_setup()
