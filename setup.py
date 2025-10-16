"""
Package setup configuration for AI Financial Portfolio Manager
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ai-financial-portfolio-manager",
    version="1.0.0",
    author="AI Financial Portfolio Manager Team",
    description="AI-powered financial portfolio management and trading recommendation system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Saksham932007/financial_portfolio",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "portfolio-agent=main:main",
        ],
    },
    keywords="finance trading ai machine-learning stocks forex portfolio-management gemini",
    project_urls={
        "Bug Reports": "https://github.com/Saksham932007/financial_portfolio/issues",
        "Source": "https://github.com/Saksham932007/financial_portfolio",
        "Documentation": "https://github.com/Saksham932007/financial_portfolio#readme",
    },
)
