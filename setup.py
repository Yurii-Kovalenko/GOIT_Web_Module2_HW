from setuptools import setup, find_packages

setup(
    name='my_assistant',
    version='0.0.1',
    description='My assistant',
    url='https://github.com/Yurii-Kovalenko/GOIT_Web_Module1_HW',
    author='Yurii Kovalenko',
    author_email='yuriy.kovalenko.in@gmail.com',
    license='MIT',
    packages=find_packages(),
    entry_points={'console_scripts': ['my-assistant=my_assistant.main:main']}
)