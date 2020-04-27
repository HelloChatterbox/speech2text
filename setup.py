from setuptools import setup

setup(
    name='speech2text',
    version='0.1.0',
    packages=['speech2text', 'speech2text.engines'],
    url='https://github.com/JarbasAl/speech2text',
    install_requires=["requests", "SpeechRecognition==3.8.1"],
    license='Apache2.0',
    author='jarbasAI',
    author_email='jarbasai@mailfence.com',
    description='Mycroft STT engine wrappers'
)
