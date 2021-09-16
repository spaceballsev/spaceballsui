from setuptools import setup

setup(
    name='spaceballs_ws_server',
    version='0.0.1',
    description="""A web socket server which processes CAN messages,
     and relays the in JSON to be consumed by WS client""",
    long_description=__doc__,
    packages=['spaceballs_ws_server'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'spaceballs = spaceballs_ws_server.cli:start_cli'
            ]
    }

)
