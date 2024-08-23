from setuptools import setup, find_packages

setup(
    name="time_series_labeler",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "plotly",
        "ipywidgets",
        "scikit-learn",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A library for interactive labeling of time series data with advanced features",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/time_series_labeler",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)