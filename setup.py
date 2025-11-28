from setuptools import setup, find_packages
from pathlib import Path

# Read README.md for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    # Basic package information
    name="resume-tailor",
    version="0.1.0",
    author="Aravind Adari",
    author_email="aravind.adari@gmail.com",
    description="AI-powered resume tailoring tool with FastAPI REST API and file upload support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aravindswamy246/PMS_v1",
    license="MIT",

    # Package structure
    packages=find_packages(where="src"),
    package_dir={"": "src"},

    # Package dependencies
    install_requires=[
        "openai>=2.6.0",
        "python-dotenv>=1.0.0",
        "click>=8.0.0",
        "fastapi>=0.120.0",
        "uvicorn[standard]>=0.34.0",
        "pydantic>=2.0.0",
        "httpx>=0.27.0",
        "aiofiles>=23.2.0",
        "python-docx>=1.2.0",
        "PyPDF2>=3.0.0",
        "python-multipart>=0.0.9",  # Required for file uploads
    ],

    # Development dependencies
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-asyncio>=0.21.0',
            'pytest-cov>=4.1.0',
            'black>=22.0',
            'flake8>=4.0',
            'mypy>=1.0',
            'httpx>=0.28.1',  # For testing API
        ],
    },

    # Python version requirement
    python_requires='>=3.8',

    # Package metadata
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: FastAPI",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business",
        "Topic :: Text Processing",
    ],

    # Entry points for command-line scripts
    entry_points={
        'console_scripts': [
            'resume-tailor=main:main',
        ],
    },

    # Additional package data
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.md', '*.yml', '*.yaml'],
    },
    zip_safe=False,

    # Keywords for PyPI
    keywords=[
        'resume',
        'job-application',
        'openai',
        'gpt',
        'api',
        'fastapi',
        'ai',
        'nlp',
        'career',
    ],
)
