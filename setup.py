from setuptools import setup, find_packages

setup(
    name='django-setstatus',
    version='0.1.0',
    description='a generic way to set time limited statuses to objects in Django',
    long_description=open('README').read(),
    author='Jervis Whitley',
    author_email='jervisw@whit.com.au',
    url='http://github.com/jtrain/django-setstatus/tree/master',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    package_data = {
    },
    zip_safe=False,
)
