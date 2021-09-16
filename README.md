# Gazette Machine Scrapers

These are [Scrapy](https://scrapy.org/) for Gazette Machine. They are run from [Scrapinghub](https://app.scrapinghub.com/p/375525/jobs) and the scraped
URLs are posted into S3, from where Gazette Machine pulls them in.

## Namibia

Scrapes Namibia Government Gazettes from https://laws.parliament.na/gazettes/namibia-government-gazettes.php?id=1

## Kenya

Scrapes the Kenya Gazette archive from http://www.kenyalaw.org/kenya_gazette/

# Development

To develop locally:

1. clone this repo
2. setup a virtualenv: ``virtualenv --no-site-packages env --python=python3``
3. activate: `source env/bin/activate`
3. install dependencies: `pip install -r requirements.txt`

# Deploying

To deploy:

1. Install the Scraping Hub commandline client with `pip install shub`
2. Run `shub deploy`

# License

Licensed under an [MIT License](LICENSE).

Copyright (2019) Laws.Africa.
