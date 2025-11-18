#!/usr/bin/env python
"""
Generate llms-full.txt by combining all documentation markdown files.

This script creates a single comprehensive file containing all documentation
for LLMs to understand the georouting package.

Usage:
    python generate_llms_full.py
"""

import os

# Define the order of files to include
files_order = [
    'docs/index.md',
    'docs/installation.md',
    'docs/usage.md',
    'docs/api/index.md',
    'docs/api/google.md',
    'docs/api/osrm.md',
    'docs/api/bing.md',
    'docs/api/esri.md',
    'docs/api/osmnx.md',
    'docs/api/base.md',
    'docs/api/utils.md',
    'docs/contributing.md',
    'docs/changelog.md',
    'docs/faq.md',
]

def main():
    # Get the directory where this script is located
    base_path = os.path.dirname(os.path.abspath(__file__))

    content_parts = []
    content_parts.append("# Georouting - Complete Documentation\n")
    content_parts.append("> A Python routing library providing a unified API across multiple routing services.\n\n")
    content_parts.append("This file contains the complete documentation for georouting, compiled from all documentation sources.\n\n")
    content_parts.append("---\n\n")

    files_included = 0
    for file_path in files_order:
        full_path = os.path.join(base_path, file_path)
        if os.path.exists(full_path):
            with open(full_path, 'r') as f:
                file_content = f.read()

            # Add section header
            content_parts.append(f"## Source: {file_path}\n\n")
            content_parts.append(file_content)
            content_parts.append("\n\n---\n\n")
            files_included += 1
        else:
            print(f"Warning: {file_path} not found, skipping...")

    # Write the combined file
    output_path = os.path.join(base_path, 'docs/llms-full.txt')
    with open(output_path, 'w') as f:
        f.write(''.join(content_parts))

    print(f"Created docs/llms-full.txt with {files_included} documentation files")

if __name__ == '__main__':
    main()
