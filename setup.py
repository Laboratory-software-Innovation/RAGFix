from setuptools import setup, find_packages

setup(
    name='my_stackoverflow_module',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'stackapi',
        'grok',
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A utility module for interacting with Stack Overflow API',
    url='https://github.com/yourusername/my_stackoverflow_module',  # Optional
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
