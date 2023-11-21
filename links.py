import glob
import re
import requests
from bs4 import BeautifulSoup

# Regex pattern to match https urls
url_pattern = re.compile(r'https?://[^\s()\[\]]*')

# Domains to filter out
filter_domains = ['imgur.com', 'skcd.com']

# Initialize an empty dictionary to hold the unique urls and their titles
url_dict = {}

# Iterate through all .md files
for file in glob.glob('*.md'):
    with open(file, 'r') as f:
        # Read the file
        content = f.read()
        # Find all urls in the file
        urls = url_pattern.findall(content)
        # Trim extra characters that follow the URL
        trimmed_urls = [re.sub(r'[\)]*$', "", url) for url in urls]
        # Filter out urls containing certain domains
        filtered_urls = [url for url in trimmed_urls if not any(domain in url for domain in filter_domains)]

        # Fetch page title for each url
        for url in filtered_urls:
            try:
                response = requests.get(url, timeout=5)
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.title.string if soup.title else 'No title found'
                url_dict[url] = title
            except requests.exceptions.RequestException as e:
                print(f"Couldn't fetch URL: {url}. Error: {e}")

# Print urls as a Markdown list with their title
for url, title in url_dict.items():
    print(f'- [{title}]({url})')