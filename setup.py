from setuptools import find_packages, setup

entry_points = {
    'console_scripts': [
        'conditional_tasks = conditional_tasks:main',
        'producer_consumer_queue = producer_consumer_queue:main'
        'mutual_exclusion_tasks = mutual_exclusion_tasks:main'
    ]
}

install_requires = [
    'Celery>=4.2.1',
    'flower==0.9.2',
    'redis==2.10.6',
    'ephem==3.7.6.0',
    'boto3==1.9.71',
]

extra_requires = {
    'development': ['pip-tools==2.0.2',]
}

setup(
    name='queue_task_runners',
    version='0.1.0',
    description='Console scripts that explain producer - queue / message brokers and consumers / '
                'worker threads.',
    author='Tonye Jack',
    author_email='jtonye@ymail.com',
    packages=find_packages(),
    entry_points=entry_points,
    install_requires=install_requires,
    extras_require=extra_requires,
)
