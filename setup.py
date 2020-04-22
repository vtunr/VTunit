import setuptools
import subprocess
with open("README.md", "r") as fh:
    long_description = fh.read()

packages = [dep.rstrip('\n') for dep in open("requirements.txt", "r")]

def get_git_version():
    return subprocess.check_output(['git', 'describe','--dirty', '--tags']).strip()

setuptools.setup(
    name="VTunit", # Replace with your own username
    version=get_git_version(),
    author="Tony Martinet",
    author_email="tonymartinet@gmail.com",
    description="Unit test helper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vtunr/VTunit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['vtunit=vtunit:main',
                            'vtunit_cmake_generator=generator.mock_generator:main', 
                            'vtunit_test_runner_generator=generator.test_runner_generator:main',
                            'vtunit_output_generator=generator.output_generator:main']
    },
    python_requires='>=2.7',
    install_requires=packages
)