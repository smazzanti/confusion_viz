from setuptools import setup

setup(
    name='confusion_viz',
    version='0.1',
    description='Interactive visualization of confusion matrices',
    url='https://github.com/smazzanti/confusion_viz',
    author='Samuele Mazzanti',
    author_email='mazzanti.sam@gmail.com',
    license='MIT',
    packages=['confusion_viz'],
    install_requires=[
        'numpy>=1.18.1',
        'sklearn>=0.22.2.post1',
        'plotly>=4.5.2'
    ],
    zip_safe=False
)
