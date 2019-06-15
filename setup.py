from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='begoneads',
    version='0.0.7',
    description='BeGoneAds puts some popular hosts file lists into the hosts file as a adblocker measure.',
    python_requires='>=3.6',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='http://github.com/anned20/begoneads',
    entry_points={
        'console_scripts': ['begoneads=begoneads.begoneads:cli'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: System :: Networking',
    ],
    author='Anne Douwe Bouma',
    author_email='annedouwe@bouma.tech',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'click',
        'requests',
        'tqdm',
    ],
    zip_safe=False
)
