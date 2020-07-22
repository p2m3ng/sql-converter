from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [elem.strip() for elem in open('requirements.txt', 'r').readlines()]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author='p2m3ng',
    author_email='contact@p2m3ng.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6.9',
    ],
    description='Dump SQL query result in various format and supports',
    entry_points={
        'console_scripts': [
            'pysqldump=pysqldump.cli:cli',
        ],
    },
    install_requires=requirements,
    include_package_data=True,
    keywords='',
    license=open('LICENSE').read(),
    long_description=readme + '\n\n',
    platforms='any',
    name='sql-domain',
    packages=find_packages('src'),
    package_dir={"": "src"},
    setup_requires=['pytest_runner'],
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitlab.com/p2m3ng/sql-converter',
    version='1.0.1',
    zip_safe=False,
)
