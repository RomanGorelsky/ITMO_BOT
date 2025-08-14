import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup
import os

# Example config mapping program names to URLs
PROGRAM_URLS = {
    'Искусственный Интеллект': 'https://abit.itmo.ru/program/master/ai',
    'Управление ИИ-продуктами/AI Product': 'https://abit.itmo.ru/program/master/ai_product'
}

def get_curriculum_file(program_name):

    url = PROGRAM_URLS.get(program_name)
    if not url:
        raise ValueError(f"No URL found for program: {program_name}")

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to load program page: {url}")

    soup = BeautifulSoup(response.text, 'html.parser')
    # Try to find the curriculum link/button (adjust selector as needed)
    curriculum_link = None
    
    for a in soup.find_all('a'):
        text = a.get_text(strip=True).lower()
        href = a.get('href', '')
        if 'учебный план' in text and href.endswith('.pdf'):
            curriculum_link = a
            break

    if not curriculum_link or not curriculum_link.has_attr('href'):
        raise Exception(f"Curriculum link not found on page: {url}")

    curriculum_url = curriculum_link['href']
    # Make absolute if relative
    if curriculum_url.startswith('/'):
        from urllib.parse import urljoin
        curriculum_url = urljoin(url, curriculum_url)

    # Download the curriculum file
    file_response = requests.get(curriculum_url)
    if file_response.status_code != 200:
        raise Exception(f"Failed to download curriculum file: {curriculum_url}")

    # Determine file extension (default to pdf)
    ext = os.path.splitext(curriculum_url)[1] or '.pdf'
    filename = f"{program_name.replace(' ', '_').replace('/', '_')}_curriculum{ext}"
    filepath = os.path.join('curriculums', filename)

    # Ensure directory exists
    os.makedirs('curriculums', exist_ok=True)

    # Save the file
    with open(filepath, 'wb') as f:
        f.write(file_response.content)

    return filepath

