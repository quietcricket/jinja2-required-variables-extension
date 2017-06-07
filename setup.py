from setuptools import setup

setup (
    name='jinja2-required-variables-extension',
    version='0.1.1',
    description='A custom Jinja tag `required`: ignore enclosed block of content if any of the variables is empty',
    author='Shang Liang',
    author_email='shang@wewearglasses.com',
    url='https://github.com/wewearglasses/jinja2-required-variables-extension',
    license='MIT',
    packages=['jinja2_ext_required'],
    install_requires=['Jinja2>=2.4'],
    classifiers=[],
)