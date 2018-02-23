from setuptools import setup

tests_require = [
    'lektor',
    'pytest',
    'pytest-cov',
    'pytest-mock'
]

setup(
    name='lektor-npm-support',
    author=u'Baruch Sterin',
    author_email='lektor-npm-support@bsterin.com',
    version='0.1',
    url='http://github.com/sterin/lektor-npm-support',
    license='BSD',
    description="Adds support for using npm/yarn to build assets in Lektor",
    py_modules=['lektor_npm_support'],
    install_requires=['future'],
    setup_requires=['pytest-runner'],
    tests_require=tests_require,
    extras_require={'test': tests_require},
    entry_points={
        'lektor.plugins': [
            'npm-support = lektor_npm_support:NPMSupportPlugin',
        ]
    }
)
