#!/usr/bin/env python
"""
Generate API documentation from source code and convert Jupyter notebooks.

This script:
1. Uses pydoc-markdown to generate markdown API docs from Python docstrings
2. Converts Jupyter notebooks to markdown and removes interactive widgets
3. Converts HTML tables to markdown tables

Usage:
    python generate_api_docs.py

Requirements:
    pip install pydoc-markdown jupyter nbconvert beautifulsoup4
"""

import os
import re
import subprocess
import sys

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


def html_table_to_markdown(html_table):
    """Convert an HTML table to markdown format."""
    if not HAS_BS4:
        return html_table

    soup = BeautifulSoup(html_table, 'html.parser')
    table = soup.find('table')

    if not table:
        return html_table

    rows = []

    # Get header row
    header_row = table.find('thead')
    if header_row:
        headers = [th.get_text(strip=True) for th in header_row.find_all('th')]
        if headers:
            rows.append('| ' + ' | '.join(headers) + ' |')
            rows.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')

    # Get body rows
    tbody = table.find('tbody')
    if tbody:
        for tr in tbody.find_all('tr'):
            cells = []
            # Handle both th (for index) and td cells
            for cell in tr.find_all(['th', 'td']):
                text = cell.get_text(strip=True)
                # Truncate long cell content
                if len(text) > 50:
                    text = text[:47] + '...'
                cells.append(text)
            if cells:
                rows.append('| ' + ' | '.join(cells) + ' |')

    if len(rows) > 1:
        return '\n'.join(rows)
    else:
        return html_table

# Define modules to generate API docs for
API_MODULES = [
    ("georouting.routers.google", "docs/api/google.md"),
    ("georouting.routers.osrm", "docs/api/osrm.md"),
    ("georouting.routers.bing", "docs/api/bing.md"),
    ("georouting.routers.esri", "docs/api/esri.md"),
    ("georouting.routers.osmnx", "docs/api/osmnx.md"),
    ("georouting.routers.base", "docs/api/base.md"),
    ("georouting.routers.mapbox", "docs/api/mapbox.md"),
    ("georouting.routers.tomtom", "docs/api/tomtom.md"),
    ("georouting.routers.here", "docs/api/here.md"),
    ("georouting.routers.baidu", "docs/api/baidu.md"),
    ("georouting.routers.openrouteservice", "docs/api/openrouteservice.md"),
    ("georouting.utils", "docs/api/utils.md"),
]

# Define notebooks to convert
NOTEBOOKS = [
    ("docs/usage.ipynb", "docs/usage_.md"),
]


def generate_api_docs():
    """Generate API documentation using pydoc-markdown."""
    print("Generating API documentation...")

    # Get the directory where this script is located
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Ensure docs/api directory exists
    api_dir = os.path.join(base_path, "docs/api")
    os.makedirs(api_dir, exist_ok=True)

    success_count = 0
    for module, output_file in API_MODULES:
        output_path = os.path.join(base_path, output_file)

        try:
            # Run pydoc-markdown
            result = subprocess.run(
                ["pydoc-markdown", "-I", ".", "-m", module, "--render-toc"],
                capture_output=True,
                text=True,
                cwd=base_path,
            )

            if result.returncode == 0:
                with open(output_path, "w") as f:
                    f.write(result.stdout)
                print(f"  ✓ Generated {output_file}")
                success_count += 1
            else:
                print(f"  ✗ Failed to generate {output_file}: {result.stderr}")
        except FileNotFoundError:
            print(
                f"  ✗ pydoc-markdown not found. Install with: pip install pydoc-markdown"
            )
            return False
        except Exception as e:
            print(f"  ✗ Error generating {output_file}: {e}")

    print(f"Generated {success_count}/{len(API_MODULES)} API documentation files")
    return success_count == len(API_MODULES)


def convert_notebooks():
    """Convert Jupyter notebooks to markdown and clean up widgets."""
    print("\nConverting Jupyter notebooks...")

    # Get the directory where this script is located
    base_path = os.path.dirname(os.path.abspath(__file__))

    success_count = 0
    for notebook, output_file in NOTEBOOKS:
        notebook_path = os.path.join(base_path, notebook)
        output_path = os.path.join(base_path, output_file)

        if not os.path.exists(notebook_path):
            print(f"  ✗ Notebook not found: {notebook}")
            continue

        try:
            # Convert notebook to markdown
            result = subprocess.run(
                [
                    "jupyter",
                    "nbconvert",
                    "--to",
                    "markdown",
                    notebook_path,
                    "--output",
                    os.path.basename(output_file),
                ],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(notebook_path),
            )

            if result.returncode != 0:
                print(f"  ✗ Failed to convert {notebook}: {result.stderr}")
                continue

            # Clean up interactive widgets and convert tables
            if os.path.exists(output_path):
                with open(output_path, "r") as f:
                    content = f.read()

                # Remove folium map widget divs (contain iframe with srcdoc)
                pattern = r'<div style="width:100%;">\s*<div style="position:relative[^>]*>.*?</iframe>\s*</div>\s*</div>'
                content = re.sub(
                    pattern,
                    "*[Interactive map - view in Jupyter notebook]*",
                    content,
                    flags=re.DOTALL,
                )

                # Convert HTML tables to markdown tables
                if HAS_BS4:
                    # Find all HTML table blocks (including surrounding div with style)
                    table_pattern = r'<div>\s*<style scoped>.*?</style>\s*<table.*?</table>\s*</div>'

                    def replace_table(match):
                        return html_table_to_markdown(match.group(0))

                    content = re.sub(table_pattern, replace_table, content, flags=re.DOTALL)
                else:
                    print("    Note: Install beautifulsoup4 to convert HTML tables to markdown")

                with open(output_path, "w") as f:
                    f.write(content)

                print(f"  ✓ Converted {notebook} → {output_file}")
                success_count += 1
            else:
                print(f"  ✗ Output file not created: {output_file}")

        except FileNotFoundError:
            print(f"  ✗ jupyter not found. Install with: pip install jupyter nbconvert")
            return False
        except Exception as e:
            print(f"  ✗ Error converting {notebook}: {e}")

    print(f"Converted {success_count}/{len(NOTEBOOKS)} notebooks")
    return success_count == len(NOTEBOOKS)


def main():
    """Main function to generate all documentation."""
    print("=" * 50)
    print("Georouting Documentation Generator")
    print("=" * 50)

    api_success = generate_api_docs()
    notebook_success = convert_notebooks()

    print("\n" + "=" * 50)
    if api_success and notebook_success:
        print("All documentation generated successfully!")
    else:
        print("Some documentation generation failed. Check errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
