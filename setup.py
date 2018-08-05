from setuptools import setup

setup(name='cloud2vec',
	version='0.1',
	description='Make dynamic word clouds with word2vec.',
	url="https://github.com/ruanchaves/cloud2vec",
	author='Ruan Chaves',
	author_email='ruanchaves93@gmail.com',
	license='MIT',
	packages=[
			'datetime'
			'difflib',
			'functools',
			'gensim',
			'heapq',
			'itertools',
			'json',
			'logging',
			'multiprocessing',
			'numpy',
			'python-telegram-bot',
			'random',
			're',
			'sympy',
			'sys',
			'yapi',
		],	
	zip_safe=False)
