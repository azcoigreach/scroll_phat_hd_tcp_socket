from setuptools import setup

setup(
    author="azcoigreach",
    author_email="azcoigreach@gmail.com",
    name = 'Scroll-Phat HD TCP Socket',
    version = '0.0.1',
    packages=['scroll_phat_tcp'],
    include_package_data=True,
    install_requires = [
        'click',
        'coloredlogs',
        'scrollphathd',
    ],
    entry_points = '''
        [console_scripts]
        scroll_phat_tcp=scroll_phat_tcp.cli:cli
    ''',
)