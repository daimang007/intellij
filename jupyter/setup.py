from setuptools import setup, find_packages

setup(
    name="corusclient",
    version="0.0.1",
    # description="Corus AI Client for Python",
    # author="Your Name",
    # author_email="your.email@example.com",
    # url="https://github.com/yourusername/corusclient",
    # packages=find_packages(include=['corusclient', 'corusclient.*']),
    packages=['corusclient'],
    install_requires=[
        "requests",
        "nbformat",
        "ipython==8.14.0",
        "ipynbname",
        "ipylab",
    ]
    # entry_points={
    #     "console_scripts": [
    #         "corusclient = corusclient.cli:main",  # Replace with your package's main script
    #     ],
    # },
)
