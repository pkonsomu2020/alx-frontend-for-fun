#!/usr/bin/python3.8

import markdown
import sys
import re
import hashlib

def convert_to_html(markdown_file):
    with open(markdown_file, 'r') as file:
        markdown_content = file.read()

        # Regular expression to match bold and emphasis syntax
        bold_pattern = re.compile(r'\*\*(.*?)\*\*')
        emphasis_pattern = re.compile(r'__(.*?)__')
        md5_pattern = re.compile(r'\[\[(.*?)\]\]')
        remove_c_pattern = re.compile(r'\(\((.*?)\)\)')
        markdown_lines = markdown_content.split('\n')
        html_lines = []

        in_list = False

        for line in markdown_lines:
            # Check for list items
            list_match = re.match(r'^\s*-\s+(.*)$', line)
            if list_match:
                if not in_list:
                    html_lines.append('<ul>')
                    in_list = True
                list_item = list_match.group(1)
                # Check for bold and emphasis syntax in list item
                list_item = bold_pattern.sub(r'<b>\1</b>', list_item)
                list_item = emphasis_pattern.sub(r'<em>\1</em>', list_item)
                # Check for MD5 syntax in list item
                list_item = md5_pattern.sub(lambda x: hashlib.md5(x.group(1).encode()).hexdigest(), list_item.lower())
                # Check for remove 'c' syntax in list item
                list_item = remove_c_pattern.sub(lambda x: x.group(1).replace('c', ''), list_item)
                html_line = f"<li>{list_item}</li>"
                html_lines.append(html_line)
            else:
                # Check for paragraph lines
                para_match = re.match(r'^\s*(.*?)$', line)
                if para_match:
                    if in_list:
                        html_lines.append('</ul>')
                        in_list = False
                    para_text = para_match.group(1)
                    # Check for bold and emphasis syntax in paragraph
                    para_text = bold_pattern.sub(r'<b>\1</b>', para_text)
                    para_text = emphasis_pattern.sub(r'<em>\1</em>', para_text)
                    # Check for MD5 syntax in paragraph
                    para_text = md5_pattern.sub(lambda x: hashlib.md5(x.group(1).encode()).hexdigest(), para_text.lower())
                    # Check for remove 'c' syntax in paragraph
                    para_text = remove_c_pattern.sub(lambda x: x.group(1).replace('c', ''), para_text)
                    html_line = f"<p>{para_text}</p>"
                    html_lines.append(html_line)

        if in_list:
            html_lines.append('</ul>')

        html_content = '\n'.join(html_lines)
        return html_content

def save_html_file(html_content, output_file):
    with open(output_file, 'w') as file:
        file.write(html_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python markdown_to_html.py input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    html_content = convert_to_html(input_file)
    save_html_file(html_content, output_file)

