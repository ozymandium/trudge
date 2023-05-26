from setuptools import setup, find_packages

setup(
    name = "trudge",
    version = "0.0.0",
    description = "Lifts",
    packages = find_packages(),
    python_requires = ">=3.9.1",
    entry_points = {
        "console_scripts": [
            "trudge = trudge.cli:main",
        ],
    },
    test_suite = "test.py",
)
