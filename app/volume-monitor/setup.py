from setuptools import setup, find_packages

setup(
    name="volume-monitor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "prometheus-client",
        "psutil",
    ],
    entry_points={
        "console_scripts": [
            "volume-monitor=run:main"
        ]
    },
)

