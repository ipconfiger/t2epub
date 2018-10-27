from setuptools import setup


setup(name='t2epub',
            version='0.0.1',
            description='Commnadline tool to transfer txt file to epub format',
            author='Alexander Li',
            author_email='superpowerlee@gmail.com',
            url='https://github.com/ipconfiger/t2epub',
            download_url='',
            packages=['t2epub'],
            zip_safe=True,
            include_package_data=True,
            license='GNU General Public License v3.0',
            keywords='txt epub novel',
            long_description="Commnadline tool to transfer txt file to epub format",
            install_requires=[
                      'jinja2',
                      'click',
                      'six',
            ],
            entry_points = {
                'console_scripts': ['t2pub=t2epub.main:main'],
            }
      )
