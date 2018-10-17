#! /Users/trensink/anaconda3/bin/python
"""
elastic search example
"""
import subprocess

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

PORTNUMBER = 9200

# client = Elasticsearch()

# s = Search(using=client, index="my-index") \
#     .filter("term", category="search") \
#     .query("match", title="python")   \
#     .exclude("match", description="beta")

# s.aggs.bucket('per_tag', 'terms', field='tags') \
#     .metric('max_lines', 'max', field='lines')

# response = s.execute()

# for hit in response:
#     print(hit.meta.score, hit.title)

# for tag in response.aggregations.per_tag.buckets:
#     print(tag.key, tag.max_lines.value)

if __name__ == '__main__':

    subprocess.call('python -m http.server {}'.format(PORTNUMBER), shell=True)
