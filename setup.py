import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pygiftparserrgmf',
    version='0.0.2',
    author='Román Ginés Martínez Ferrández',
    author_email='rgmf@riseup.net',
    description='Moodle GIFT files parser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/rgmf/pygiftparser',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX :: Linux'
    ],
    python_requires='>=3.8',
)