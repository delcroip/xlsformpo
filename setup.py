from setuptools import setup

setup(
    name='xlsformpo',
    version='0.0.1',
    author='DHU SwissTPH httu.admin@swisstph.ch',
    description='Python library translateXLSForms.',
    long_description='Python library translateXLSForms usign po files (gettext)',
    url='https://github.com/SwissTPH/xlsformpo',
    keywords='xlsform, gettext, ODK, XForm',
    python_requires='>=3.8, <4',
    install_requires=[
        "pandas",
        "polib",
        "html2text",
        "xlsxwriter"
        ],
    #extras_require={
    #    'test': ['pytest', 'coverage'],
    #},
    #package_data={
    #    'sample': ['example_data.csv'],
    #},
    #entry_points={
    #    'runners': [
    #        'sample=sample:main',
    #    ]
    #}
)
