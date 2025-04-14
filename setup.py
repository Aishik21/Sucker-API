from setuptools import setup, find_packages

setup(
    name="web-crawler-api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "pydantic-settings>=2.0.0",
        "python-dotenv>=0.19.0",
        "requests>=2.26.0",
        "playwright>=1.30.0",
        "google-generativeai>=0.3.0",
        "slowapi>=0.1.5",
        "python-multipart>=0.0.5",
        "aiofiles>=0.7.0",
        "crawl4ai>=0.1.0",
    ],
    entry_points={
        "console_scripts": [
            "web-crawler=api.main:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A general-purpose web crawler API with LLM-powered content extraction",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/web-crawler-api",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    package_data={
        "": ["*.json", "*.env"],
    },
) 