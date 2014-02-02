import fabric.api as fab


def html():
    with fab.lcd('docs'):
        fab.local('../env/bin/sphinx-build -b html . ./_build')
