#!/bin/bash
# AUTHOR: Luis Alberto López Álvarez - TFM (ETSIT - UPM)
#
# harvest.sh - Lógica necesaria para recopilar URLS ".onion"


LIST=`mktemp`
http_proxy="" https_proxy="" wget --no-check-certificate --tries=1 -T 10  -O - http://www.thehackerstore.net/2015/07/huge-list-of-darknet-deep-web-hidden.html | grep -E -o '[0-9a-zA_Z]+\.onion' >> $LIST
http_proxy="" https_proxy="" wget --no-check-certificate --tries=1 -T 10  -O - https://thehiddenwiki.org/ | grep -E -o '[0-9a-zA_Z]+\.onion' >> $LIST
http_proxy="" https_proxy="" wget --no-check-certificate --tries=1 -T 10  -O - https://torhiddenwiki.com/ | grep -E -o '[0-9a-zA_Z]+\.onion' >> $LIST
http_proxy="" https_proxy="" wget --no-check-certificate --tries=1 -T 10  -O - https://darknetmarkets.org/markets/ | grep -E -o '[0-9a-zA_Z]+\.onion' >> $LIST
http_proxy="" https_proxy="" wget --no-check-certificate --tries=1 -T 10  -O - https://www.reddit.com/r/onions/comments/73jpvo/loads_of_good_onion_links_part_two/ | grep -E -o '[0-9a-zA_Z]+\.onion' >> $LIST
http_proxy="" https_proxy="" wget --no-check-certificate --tries=1 -T 10  -O - https://www.quora.com/What-are-some-cool-dark-web-websites?share=1 | grep -E -o '[0-9a-zA_Z]+\.onion' >> $LIST
http_proxy="" https_proxy="" wget --no-check-certificate --tries=1 -T 10  -O - https://www.reddit.com/r/onions/comments/56sz15/suggestions_links_post_it_here/ | grep -E -o '[0-9a-zA_Z]+\.onion' >> $LIST
http_proxy="" https_proxy="" wget --no-check-certificate --tries=1 -T 10  -O - http://www.linuxx.eu/p/deep-web-link-list-onion.html | grep -E -o '[0-9a-zA_Z]+\.onion' >> $LIST
http_proxy="" https_proxy="" wget --no-check-certificate --tries=1 -T 10  -O - http://seriezfree.blogspot.com/p/blog-page.html | grep -E -o '[0-9a-zA_Z]+\.onion' >> $LIST
http_proxy="" https_proxy="" wget --no-check-certificate --tries=1 -T 10  -O - https://pastebin.com/TB4ifihx | grep -E -o '[0-9a-zA_Z]+\.onion' >> $LIST
http_proxy="" https_proxy="" wget --no-check-certificate --tries=1 -T 10  -O - https://www.reddit.com/r/onions/search\?q\=url:.onion\&sort\=new\&restrict_sr\=on | grep -E -o '[0-9a-zA_Z]+\.onion' >> $LIST
http_proxy="" https_proxy="" wget --no-check-certificate --tries=1 -T 10  -O - https://raw.githubusercontent.com/alecmuffett/onion-sites-that-dont-suck/master/README.md | grep -E -o '[0-9a-zA_Z]+\.onion' >> $LIST
http_proxy="" https_proxy="" wget --no-check-certificate --tries=1 -T 10  -O - https://en.wikipedia.org/wiki/List_of_Tor_hidden_services | grep -E -o '[0-9a-zA_Z]+\.onion' >> $LIST
http_proxy="" https_proxy="" wget --no-check-certificate --tries=1 -T 10  -O - https://torlinks.io/trusted-tor-sites/ | grep -E -o '[0-9a-zA_Z]+\.onion' >> $LIST

# Peticiones para realizar el Harvesting
sudo chmod -R +x /home/vagrant/Desktop/tor-scraper-classifier/config/urls_harvest.txt
URLS="/home/vagrant/Desktop/tor-scraper-classifier/config/urls_harvest.txt"
for URL in $(cat "$URLS"); do
  echo "URL: $URL"
  if ! curl --socks5-hostname localhost:9051 "$URL"; then
    echo "No se pudo obtener la información para $URL"
  else
    curl --socks5-hostname localhost:9051 "$URL" | grep -E -o '[0-9a-zA_Z]+\.onion' >> "$LIST"
  fi
done

# Inserción de los resultados en un fichero .txt llamado harvest_results.txt
cat $LIST | grep -E -o '[0-9a-zA_Z]+\.onion' | sort | uniq | sort -R > /home/vagrant/Desktop/tor-scraper-classifier/results/harvest_results.txt
NUMBER=`wc -l /home/vagrant/Desktop/tor-scraper-classifier/results/harvest_results.txt | tr -s ' ' | cut -f 1 -d ' '`
echo "Se han recopilado $NUMBER URLs .onion ..."
rm $LIST