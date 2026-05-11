"""Setup do RPA Framework Coop."""

from setuptools import setup, find_packages

with open("requirements.txt", encoding="utf-8") as f:
    requirements = [
        line.strip()
        for line in f
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="rpa-3003",
    version="1.0.0",
    description="Framework Python modular e extensível para automação RPA.",
    author="Coop Team",
    python_requires=">=3.9",
    packages=find_packages(exclude=["tests", "tests.*", "projects", "projects.*"]),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "rpa3003 = rpa_3003.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
)
