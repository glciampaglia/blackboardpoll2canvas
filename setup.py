""" Setuptools script """

from setuptools import setup, find_packages

kwargs = dict(
    name="blackboardpoll2canvas",
    description=(
        'Import poll reports from BlackBoard Collaborate '
        'Ultra into Canvas gradebook format'),
    author='Giovanni Luca Ciampaglia',
    author_email='glc3@mail.usf.edu',
    license='MIT',
    url='https://github.com/glciampaglia/blackboardpoll2canvas.git',
    packages=find_packages(),
    install_requires=[
        'nameparser',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            "blackboardpoll2canvas = blackboardpoll2canvas.main:main"
        ]
    }
)

if __name__ == '__main__':
    setup(**kwargs)
