from setuptools import setup

setup(
    name='raindrop',
    version='0.2.3',
    description='a python library for Hydro Client Raindrop',
    license='MIT',
    packages=['raindrop'],
    author='Andy Chorlian',
    author_email='andy@hydrogenplatform.com',
    keywords=['blockchain', 'ethereum', '2FA', 'raindrop', 'web3', 'two-factor'],
    url='https://github.com/hydrogen-dev/raindrop-sdk-python',
	install_requires = [
		'httplib2'
	]
)
