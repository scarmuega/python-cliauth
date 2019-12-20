from setuptools import setup

setup(name='cliauth',
      version='0.2.0',
      python_requires='>=3',
      description='Easy auth for your python CLI',
      packages=['cliauth'],
      install_requires=[
          'requests', 'pyjwt'
      ],
      zip_safe=False,
    )
