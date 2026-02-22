import re
from bs4 import BeautifulSoup
import requests
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd

# Load the CSV file
df = pd.read_csv('./static/updated_content.csv')

def extract_content_in_sequence(soup):
    content_sequence = []
    for element in soup.find_all(['p', 'pre', 'div']):
        if element.name == 'p':
            content_sequence.append({'type': 'text', 'content': element.text.strip().replace('\n', '')})
        elif element.name == 'pre':
            content_sequence.append({'type': 'code', 'content': element.text.strip()})
        elif element.name == 'div' and 'code-block' in element.get('class', []):
            content_sequence.append({'type': 'code-block', 'content': element.text.strip()})
        elif element.name == 'div' and 'w3-example' in element.get('class', []):
            code_content = element.find('div', class_ = 'w3-code notranslate pythonHigh')
            if code_content:
                content_sequence.append({'type': 'code-block', 'content': code_content.text.strip()})
    return content_sequence

def gfg(subtopic):
    print('Scraping GFG')
    url = df.loc[df['Sub-topics'] == subtopic, 'gfg'].values[0]
    gfg_data = {}
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    main_content = soup.find('div', {'class': 'text'}) or soup.find('div', {'class': 'page_content'})

    if main_content:
        gfg_data[url] = extract_content_in_sequence(main_content)
    gfg_data[url] = generate_html('gfg', gfg_data, url, subtopic)
    return gfg_data

def w3schools(subtopic):
    print('Scraping W3Schools')
    url = df.loc[df['Sub-topics'] == subtopic, 'w3school'].values[0]
    w3schools_data = {}
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    main_content = soup.find('div', {'id': 'main'}) or soup.find('div', {'class': 'onlycontentinner'})

    if main_content:
        w3schools_data[url] = extract_content_in_sequence(main_content)
    w3schools_data[url] = generate_html('w3schools', w3schools_data, url, subtopic)
    return w3schools_data

def youtube(subtopic):
    print('Fetching YouTube Transcript')
    url = df.loc[df['Sub-topics'] == subtopic, 'youtube'].values[0]
    youtube_data = {}
    video_id = url.split('v=')[-1]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ' '.join([segment['text'] for segment in transcript])
        youtube_data[url] = [{'type': 'text', 'content': transcript_text}]
    except Exception as e:
        youtube_data[url] = [{'type': 'text', 'content': f"Error occurred: {e}"}]

    youtube_data[url] = generate_html('youtube', youtube_data, url, subtopic)
    return youtube_data

def generate_html(preference, data, url, subtopic):
    source_map = {
        'gfg': 'GeeksforGeeks',
        'w3schools': 'W3Schools',
        'youtube': 'YouTube'
    }
    source = source_map.get(preference, 'Source')
    credits = url

    html_content = f"""
<div class="content-container">
  <h1>Let's Learn {subtopic}</h1>
  <h2 id="source">Source: <a href="{credits}">{source}</a></h2>
"""

    for content_list in data.values():
        html_content += f"""
  <p><span class="content-url">Content from {source} - <a href="{credits}" target="_blank">{credits}</a>:</span></p>
"""
        for item in content_list:
            if item['type'] == 'text':
                html_content += f"<p>{item['content']}</p>"
            elif item['type'] == 'code':
                html_content += f"<pre>{item['content']}</pre>"
            elif item['type'] == 'code-block':
                html_content += f"<div class='code-block'>{item['content']}</div>"

    html_content += """
</div>
"""
    return html_content
