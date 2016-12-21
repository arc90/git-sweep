import sys
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()

version = '0.1.1'

install_requires = [
    'GitPython>=0.3.2RC1',
    'six==1.10.0']

# Add argparse if less than Python 2.7
if sys.version_info[0] <= 2 and sys.version_info[1] < 7:
    install_requires.append('argparse>=1.2.1')

setup(name='git-sweep',
    version=version,
    description="Clean up branches from your Git remotes",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Version Control',
        'Topic :: Text Processing'
    ],
    keywords='git maintenance branches',
    author='Arc90, Inc.',
    author_email='',
    url='http://arc90.com',
    license='MIT',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['git-sweep=gitsweep.entrypoints:main']
    }
)
