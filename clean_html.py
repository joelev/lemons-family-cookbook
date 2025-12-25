#!/usr/bin/env python3
"""Clean Wayback Machine HTML files for local use."""

import re
import sys

def clean_html(html, is_archives_page=False):
    """Remove Wayback Machine artifacts and rewrite URLs for local use."""
    prefix = "../" if is_archives_page else ""

    # Remove Wayback Machine script tags
    html = re.sub(r'<script[^>]*src="https://web-static\.archive\.org[^"]*"[^>]*></script>\s*', '', html)
    html = re.sub(r'<script[^>]*>window\.RufflePlayer[^<]*</script>\s*', '', html)
    html = re.sub(r'<script type="text/javascript">\s*__wm\.init[^<]*</script>\s*', '', html)

    # Remove Wayback Machine CSS links
    html = re.sub(r'<link[^>]*href="https://web-static\.archive\.org[^"]*"[^>]*/>\s*', '', html)

    # Remove HTML comments with archive info
    html = re.sub(r'<!--\s*FILE ARCHIVED ON.*?-->', '', html, flags=re.DOTALL)
    html = re.sub(r'<!--\s*playback timings.*?-->', '', html, flags=re.DOTALL)

    # Rewrite CSS URL (handles both lemons.css and styles-site.css)
    html = re.sub(
        r'href="https://web\.archive\.org/web/\d+cs_/http://[^/]+/(lemons|styles-site)\.css"',
        f'href="{prefix}lemons.css"',
        html
    )

    # Rewrite image URLs
    html = re.sub(
        r'(?:src|SRC)="/web/\d+im_/http://[^/]+/l_images/([^"\']+)"',
        f'src="{prefix}l_images/\\1"',
        html
    )

    # Rewrite internal links to archives (handle both www and non-www)
    html = re.sub(
        r'href="https://web\.archive\.org/web/\d+/http://(?:www\.)?lemonscookbook\.com/archives/([^"]+)"',
        f'href="{prefix}archives/\\1"' if not is_archives_page else r'href="\1"',
        html
    )

    # Rewrite front page link
    html = re.sub(
        r'href="https://web\.archive\.org/web/\d+/http://(?:www\.)?lemonscookbook\.com/"',
        f'href="{prefix}index.html"',
        html
    )

    # Remove mailto rewrite
    html = re.sub(
        r'href="https://web\.archive\.org/web/\d+/mailto:',
        'href="mailto:',
        html
    )

    return html

if __name__ == '__main__':
    is_archives = len(sys.argv) > 1 and sys.argv[1] == '--archives'
    # Handle encoding issues from old web pages
    html = sys.stdin.buffer.read().decode('utf-8', errors='replace')
    print(clean_html(html, is_archives))
