========================
Pdf Scraper
========================

A django project that crawls websites for pdf documents. A typical use case is a site that publishes reports or announcements in pdf
format on a frequent basis. This application can crawl the site for new pdf's and record when they were found. The crawl
engine is based on the excellent Scrapy project which uses the Twisted reactor.

To use this project follow these steps:

#1. Create your working environment
#2. Install Requirements
#3. Create your "Spiders" corresponding to the sites you want to crawl
#4. Crawl!

*note: these instructions show creation of a project called "icecream".  You
should replace this name with the actual name of your project.*

1 Working Environment
===================

You have several options in setting up your working environment.  We recommend
using virtualenv to separate the dependencies of your project from your system's
python environment.  If on Linux or Mac OS X, you can also use virtualenvwrapper to help manage multiple virtualenvs across different projects.

Virtualenv with virtualenvwrapper
------------------------------------

In Linux and Mac OSX, you can install virtualenvwrapper (http://virtualenvwrapper.readthedocs.org/en/latest/),
which will take care of managing your virtual environments and adding the
project path to the `site-directory` for you::

    $ mkdir pdfscraper
    $ mkvirtualenv pdfscraper



Installing Requirements
=================

To install your requirements for local use, run the following::

    $ pip install -r requirements/local.txt

if `cryptography` fails to compile, you probably need some package dependencies. Run the following::

    $ sudo apt-get install build-essential libssl-dev libffi-dev python-dev


Create your "Spiders"
=====================

Fire up your django admin to create your Spiders::

    $ ./manage.py runserver --settings=pdfscraper.settings.<settingsfile>

Navigate to `http://localhost:8000/admin/spiders/spider/` in your favourite browser.

Here is the advanced part. You must specify two important fields to create your Spider.

#1. Allow (or Deny) Rule - specify the regular expression(s) corresponding to your. 
#2. Spider URLs - Allowed Domain - you must specify the url domain(s) you want to crawl
#3. Spider URLs - Start Url - you must specify the initial url(s) to visit to begin your crawl

As an example, imagine we wanted to crawl example.com for pdf's. The following would be our fields
Allow Rule: .+example.com/.+
Deny Rule: .+\\.flv  # We don't want to crawl flv pages
Start Url: http://www.example.com/
Allowed Domain: http://www.example.com/


Crawl!
=============================

Crawling is easy. Just run the following::

    $ ./manage.py scrape --settings=pdfscraper.settings.<settingsfile>

where <settingsfile> can be `local`, `production`, etc.

Once the scrape is complete, you can fire up your django admin to view the results::

    $ ./manage.py runserver --settings=pdfscraper.settings.<settingsfile>

Navigate to `http://localhost:8000/admin/spiders/spider/` in your favourite browser. Check our the SpiderSession objects. 
These pertain to objects stored to track your scrape activity. Also check out the DataItem objects. These objects contains 
your pdf links and other very useful metadata.


Acknowledgements
================

- All of the contributors_ to this project.

.. _contributors: https://github.com/Valuehorizon/Pdf-Scraper/blob/master/CONTRIBUTORS.txt
