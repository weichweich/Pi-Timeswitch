from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='Timeswitch',
      version='0.1',
      description='Time based GPIO switching',
      author='Albrecht Weiche',
      author_email='weich@posteo.de',

      url='https://github.com/weichweich/Pi-Timeswitch',
      packages=['timeswitch'],

      install_requires=required,
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],

      entry_points={
          'console_scripts': [
              'timeswitch = timeswitch.server:main',
              'timer = timeswitch.timer:main',
          ]
      }
      )
