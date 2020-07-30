# MSN News Crawler

This is a crawler to crawl news features from MSN news website such as body, title, vert and subvert, giving serveral news urls.

Build with scrapy 2.0 and python3.7:

`https://docs.scrapy.org/en/latest/intro/tutorial.html`


The conda enviroment is exported to `enviroments.yaml`. To create a conda enviroment, please run:

```bash
conda env create -f environment.yaml
conda activate scrapy
```

Set environment varialble `MIND_NEWS_PATH` to the path of your `news.tsv`

```bash
export MIND_NEWS_PATH=[your path]
```

Run the crawler:

```bash
scrapy crawl msn -o msn.json
```

The crawled urls are in the `start_url` list of `msn/spiders/msn_spider.py`. You can add more urls here.

To add more news features, please edit `items.py` and `msn_spider.py`.

