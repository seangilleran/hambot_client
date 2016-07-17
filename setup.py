from setuptools import setup


setup(
    name='hambot-client',
    version='0.1',
    license='MIT',
    author='Sean Gilleran',
    author_email='sgilleran@gmail.com',
    url='https://github.com/seangilleran/hambot_client',
    download_url='https://github.com/seangilleran/hambot_client/tarball/0.1',
    packages=['hambot'],
    install_requires=[
        'Pillow>=3.3.0',
        'py-enigma>=0.1',
        'py-enigma-operator>=0.6',
        'pytz>=2016.6',
        'tzlocal>=1.2.2',
        'requests>=2.10'],
    zip_safe=False
)
