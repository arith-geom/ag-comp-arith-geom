#!/usr/bin/env python3
"""Manual extraction of member contact information from old HTML files"""
import os
import yaml
from bs4 import BeautifulSoup
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TYPO_MIRROR_DIR = os.path.join(BASE_DIR, 'typo_mirror', 'groups', 'arith-geom')
DATA_DIR = os.path.join(BASE_DIR, '_data')

def clean_text(text):
    if not text:
        return ""
    text = text.replace('\xa0', ' ')
    text = text.replace('<at>', '@')
    text = text.replace('\u003cat\u003e', '@')
    text = text.replace('\u003c', '<').replace('\u003e', '>')
    return re.sub(r'\s+', ' ', text).strip()

def extract_member_data(html_file):
    """Extract contact info from a member's HTML file"""
    if not os.path.exists(html_file):
        return {}
    
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    data = {}
    
    # Find photo
    img = soup.find('img', class_='image-embed-item')
    if img and img.get('src'):
        # Extract just the filename for simplified path
        src = img.get('src')
        if 'csm_Boeckle' in src:
            data['photo'] = '/assets/img/gebhard-boeckle.jpg'
        elif 'csm_Sudmann' in src or 'Cederbaum' in src or 'Sudmann' in src:
            data['photo'] = '/assets/img/astrid-cederbaum.jpg'
        elif 'Andrea_Conti' in src:
            data['photo'] = '/assets/img/andrea-conti.jpg'
        elif 'Kaiser' in src:
            data['photo'] = '/assets/img/theresa-kaiser.jpg'
        elif 'Shavali' in src:
            data['photo'] = '/assets/img/alireza-shavali.jpg'
    
    # Find bodytext
    bodytext = soup.find('div', class_='ce-bodytext')
    if not bodytext:
        textpic = soup.find('div', class_='ce-textpic')
        if textpic:
            bodytext = textpic.find('div', class_='ce-bodytext')
    
    if bodytext:
        text = bodytext.get_text('\n')
        
        # Extract email
        email_match = re.search(r'Email:\s*([^\n]+)', text)
        if email_match:
            email = clean_text(email_match.group(1))
            data['email'] = email
        
        # Extract phone
        tel_match = re.search(r'Tel\.?:\s*([^\n]+)', text)
        if tel_match:
            data['phone'] = clean_text(tel_match.group(1))
        
        # Extract fax
        fax_match = re.search(r'Fax:\s*([^\n]+)', text)
        if fax_match:
            data['fax'] = clean_text(fax_match.group(1))
        
        # Extract room
        room_match = re.search(r'Room:\s*([^\n]+)', text)
        if room_match:
            data['room'] = clean_text(room_match.group(1))
        
        # Extract office hours
        office_match = re.search(r'Office Hours?:\s*([^\n]+)', text, re.IGNORECASE)
        if office_match:
            data['office_hours'] = clean_text(office_match.group(1))
    
    # Extract CV link
    cv_link = soup.find('a', string=re.compile(r'(CV|cv|Short CV)', re.I))
    if not cv_link:
        cv_link = soup.find('a', href=re.compile(r'CV', re.I))
    if cv_link and cv_link.get('href'):
        href = cv_link.get('href')
        if 'fileadmin' in href:
            idx = href.find('fileadmin')
            data['cv'] = '/assets/' + href[idx:]
    
    return data

# Process each current member
members_to_process = [
    ('gebhard-boeckle.html', 'Prof. Dr. Gebhard Böckle', 'Group Leader', 'Head'),
    ('astrid-cederbaum.html', 'Astrid Cederbaum', 'Secretary', 'Secretary'),
    ('andrea-conti.html', 'Dr. Andrea Conti', 'Researcher', 'Members'),
    ('paola-chilla.html', 'Paola Chilla', 'PhD Student', 'Members'),
    ('sriramcv.html', 'Sriram Chinthalagiri Venkata', 'PhD Student', 'Members'),
    ('theresa-kaiser.html', 'Theresa Kaiser', 'PhD Student', 'Members'),
    ('giacomo-hermes-ferraro.html', 'Dr. Giacomo Hermes Ferraro', 'Researcher', 'Members'),
    ('alireza-shavali.html', 'Alireza Shavali', 'PhD Student', 'Members'),
]

print("Extracting member data...")
for html_file, name, role, section in members_to_process:
    filepath = os.path.join(TYPO_MIRROR_DIR, 'members', html_file)
    data = extract_member_data(filepath)
    print(f"\n{name}:")
    for key, value in data.items():
        print(f"  {key}: {value}")
