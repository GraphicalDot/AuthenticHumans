amoeba
======

Project Amoeba.


Urlworkers
These worker populate the redis tree with specified social network

Class: UrlWorkersLinkedin
Class: UrlWorkersFacebook
Class: UrlWorkersGithub

These are periodic tasks

To run: celery -A tasks worker --loglevel=info --beat

