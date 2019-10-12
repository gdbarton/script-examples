#!/usr/bin/env bash

# Grant Barton August 2019
# This script polls the local elasticsearch port and returns critical if it doesn't receive
# a 200 http response

response=`curl -s -o /dev/null -w "%{http_code}" localhost:9200`

if [ $response = "200" ] ; then
        exit 0
else
        echo "Elasticsearch is not running on $HOSTNAME"
        exit 2
fi
