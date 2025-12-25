#!/usr/bin/env python3
"""
Parse HTML recipe files from Wayback Machine archive into structured Markdown.
"""

import os
import re
import html
from pathlib import Path
from bs4 import BeautifulSoup
import json
import unicodedata

# Category mapping from cat_*.html filenames to slugs
CATEGORY_MAP = {
    'cat_cakes_pies_frostings.html': 'cakes-pies-frostings',
    'cat_candies_cookies_confections.html': 'candies-cookies-confections',
    'cat_main_dishes_meats_vegetables.html': 'main-dishes-meats-vegetables',
    'cat_quickbreads_muffins_pancakes.html': 'quickbreads-muffins-pancakes',
    'cat_salads.html': 'salads',
    'cat_yeast_breads_rolls_sweet_dough.html': 'yeast-breads-rolls-sweet-dough',
}

CATEGORY_NAMES = {
    'cakes-pies-frostings': 'Cakes, Pies, Frostings',
    'candies-cookies-confections': 'Candies, Cookies, Confections',
    'main-dishes-meats-vegetables': 'Main Dishes, Meats, Vegetables',
    'quickbreads-muffins-pancakes': 'Quickbreads, Muffins, Pancakes',
    'salads': 'Salads',
    'yeast-breads-rolls-sweet-dough': 'Yeast Breads, Rolls, Sweet Dough',
}


def build_category_index(archives_dir: Path) -> dict:
    """Build a mapping of recipe filename -> category slug."""
    recipe_to_category = {}

    for cat_file, cat_slug in CATEGORY_MAP.items():
        cat_path = archives_dir / cat_file
        if not cat_path.exists():
            print(f"Warning: Category file not found: {cat_path}")
            continue

        with open(cat_path, 'r', encoding='utf-8', errors='replace') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Find all recipe links in the category page
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.endswith('.html') and not href.startswith('cat_') and not href.startswith('..'):
                recipe_to_category[href] = cat_slug

    return recipe_to_category


def clean_text(text: str) -> str:
    """Clean up text, converting HTML entities and normalizing whitespace."""
    if not text:
        return ''

    # Decode HTML entities
    text = html.unescape(text)

    # Convert fancy fractions
    text = text.replace('½', '1/2')
    text = text.replace('¼', '1/4')
    text = text.replace('¾', '3/4')
    text = text.replace('⅓', '1/3')
    text = text.replace('⅔', '2/3')
    text = text.replace('°', ' degrees')

    # Normalize whitespace
    text = ' '.join(text.split())

    return text.strip()


def convert_fractions(soup_element) -> str:
    """Convert <sup>N</sup>/<sub>M</sub> patterns to N/M."""
    if soup_element is None:
        return ''

    # Get the HTML and process it
    html_content = str(soup_element)

    # Replace <sup>X</sup>/<sub>Y</sub> with X/Y
    html_content = re.sub(
        r'<sup>(\d+)</sup>\s*/\s*<sub>(\d+)</sub>',
        r'\1/\2',
        html_content
    )

    # Parse back and get text
    temp_soup = BeautifulSoup(html_content, 'html.parser')
    return clean_text(temp_soup.get_text())


def parse_ingredient_list(ul_element) -> list:
    """Parse a <ul> with potentially unclosed <li> tags."""
    # Get the raw HTML and split by <li> tags
    html_content = str(ul_element)

    # Remove <ul> wrapper
    html_content = re.sub(r'^<ul[^>]*>', '', html_content)
    html_content = re.sub(r'</ul>$', '', html_content)

    # Split by <li> tags (handles unclosed tags)
    parts = re.split(r'<li[^>]*>', html_content)

    items = []
    for part in parts:
        # Remove any closing </li> tag and clean up
        part = re.sub(r'</li>', '', part)
        # Convert fractions in the text
        part = re.sub(r'<sup>(\d+)</sup>\s*/\s*<sub>(\d+)</sub>', r'\1/\2', part)
        # Parse remaining HTML and get text
        temp_soup = BeautifulSoup(part, 'html.parser')
        text = clean_text(temp_soup.get_text())
        if text:
            items.append(text)

    return items


def parse_recipe(html_path: Path, category: str) -> dict:
    """Parse a single recipe HTML file."""
    with open(html_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Extract title
    title_elem = soup.find('h3', class_='title')
    if not title_elem:
        print(f"Warning: No title found in {html_path}")
        return None

    title = clean_text(title_elem.get_text())

    # Find the blogbody div containing the recipe content
    blogbody = soup.find('div', class_='blogbody')
    if not blogbody:
        print(f"Warning: No blogbody found in {html_path}")
        return None

    # Process content - collect ingredients and instructions
    content_parts = []

    # Skip the title, process remaining elements
    for elem in blogbody.children:
        if elem.name == 'h3':
            continue  # Skip title
        if elem.name == 'ul':
            # Ingredient list - use special parser for unclosed <li> tags
            items = parse_ingredient_list(elem)
            if items:
                content_parts.append({'type': 'ingredients', 'items': items})
        elif elem.name == 'p':
            text = convert_fractions(elem)
            if text and text not in ['', ' ']:
                content_parts.append({'type': 'instruction', 'text': text})
        elif elem.name == 'a' and elem.get('name') == 'more':
            # End marker
            break

    # Try to identify story content (usually the last paragraph(s) that are personal)
    story = None
    if content_parts:
        # Check last few paragraphs for story indicators
        story_indicators = [
            'I like', 'I love', 'I usually', 'This is', 'This was',
            'Grandma', 'My mother', 'My grandmother', 'recipe from',
            "Mama's", "Grandma's", "This makes", "Very good",
            'Kirk', 'Lorea', 'Joel', 'Vivian'
        ]

        # Look for story at the end
        for i in range(len(content_parts) - 1, max(0, len(content_parts) - 3), -1):
            part = content_parts[i]
            if part['type'] == 'instruction':
                if any(ind.lower() in part['text'].lower() for ind in story_indicators):
                    story = part['text']
                    content_parts = content_parts[:i]
                    break

    return {
        'title': title,
        'category': category,
        'content_parts': content_parts,
        'story': story,
        'slug': html_path.stem,
    }


def recipe_to_markdown(recipe: dict) -> str:
    """Convert a parsed recipe to Markdown with frontmatter."""
    lines = ['---']
    lines.append(f'title: "{recipe["title"]}"')
    lines.append(f'category: {recipe["category"]}')
    if recipe.get('story'):
        # Escape quotes in story for YAML
        escaped_story = recipe['story'].replace('"', '\\"')
        lines.append(f'story: "{escaped_story}"')
    lines.append('---')
    lines.append('')

    # Write content
    for part in recipe['content_parts']:
        if part['type'] == 'ingredients':
            for item in part['items']:
                lines.append(f'- {item}')
            lines.append('')
        elif part['type'] == 'instruction':
            lines.append(part['text'])
            lines.append('')

    return '\n'.join(lines)


def main():
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    archives_dir = project_dir / 'archives'
    output_dir = project_dir / 'src' / 'content' / 'recipes'

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build category index
    print("Building category index...")
    recipe_to_category = build_category_index(archives_dir)
    print(f"Found {len(recipe_to_category)} recipes in category indexes")

    # Parse all recipe files
    recipe_files = [f for f in archives_dir.glob('*.html')
                   if not f.name.startswith('cat_')]

    print(f"Found {len(recipe_files)} recipe files to parse")

    parsed_count = 0
    skipped_count = 0

    for html_path in recipe_files:
        # Get category for this recipe
        category = recipe_to_category.get(html_path.name)
        if not category:
            print(f"Warning: No category found for {html_path.name}, skipping")
            skipped_count += 1
            continue

        # Parse the recipe
        recipe = parse_recipe(html_path, category)
        if not recipe:
            skipped_count += 1
            continue

        # Convert to markdown
        markdown = recipe_to_markdown(recipe)

        # Write output file
        output_path = output_dir / f"{recipe['slug']}.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)

        parsed_count += 1

    print(f"\nParsed {parsed_count} recipes")
    print(f"Skipped {skipped_count} files")
    print(f"Output written to {output_dir}")


if __name__ == '__main__':
    main()
