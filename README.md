# Gazette Machine Scrapers

These are [Scrapy](https://scrapy.org/) for Gazette Machine. They are run from [Zyte](https://app.zyte.com/p/375525/spiders) and the scraped
URLs are posted into S3, from where Gazette Machine pulls them in.

# Development

To develop locally:

1. clone this repo
2. setup a virtualenv: ``python3 -m venv env``
3. activate: `source env/bin/activate`
3. install dependencies: `pip install -r requirements.txt`

# Deploying

To deploy:

1. Install the Scraping Hub commandline client with `pip install shub`
2. Run `shub deploy`
3. In [Zyte](https://app.zyte.com/p/375525/spiders) configure the spider's AWS and output settings, similar to the other spiders.
4. In gazettemachine, update `settings.GM['SCRAPINGHUB_SPIDERS']` to include the new spider, if it should be run daily.

* AWS_ACCESS_KEY_ID: from AWS
* AWS_SECRET_ACCESS_KEY: from AWS
* FEED_FORMAT: csv
* FEED_URI: `s3://lawsafrica-gazettes-incoming/dropbox/<code>.csv`
