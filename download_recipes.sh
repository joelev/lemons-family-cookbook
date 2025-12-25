#!/bin/bash
cd /Users/joel/Documents/Side\ Projects/Code/lcookscraper

count=0
total=$(wc -l < recipe_urls.txt)

while read -r url; do
    filename=$(basename "$url")
    if [ ! -f "archives/$filename" ]; then
        curl -sL "https://web.archive.org/web/20051213034931/http://www.lemonscookbook.com/$url" | python3 clean_html.py --archives > "archives/$filename"
        ((count++))
        echo "[$count/$total] Downloaded $filename"
    else
        ((count++))
        echo "[$count/$total] Skipped $filename (exists)"
    fi
done < recipe_urls.txt

echo "Done! Downloaded $count recipes."
