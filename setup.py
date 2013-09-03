from distutils.core import setup
f=open("README.rst")
setup(name='pylittlesis', version='0.01',
            py_modules=['littlesis'],
            url="https://github.com/mihi-tr/pylittlesis",
            author="Michael Bauer",
            author_email="mihi@lo-res.org",
            description="""A Python wrapper around the Little Sis API""",
            long_description=f.read()
                  )
