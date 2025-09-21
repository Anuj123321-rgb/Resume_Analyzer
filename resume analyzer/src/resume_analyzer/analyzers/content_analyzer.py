#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Content Analyzer Module

This module provides functionality for analyzing the content of resumes
and extracting basic information such as contact details and summary.
"""

import re
from typing import Optional, List, Dict, Any

from resume_analyzer.models.resume import Resume


def analyze(resume: Resume) -> None:
    """
    Analyze the resume content and extract basic information.
    
    Args:
        resume (Resume): The resume object to analyze.
    """
    # Extract basic information
    extract_contact_info(resume)
    extract_summary(resume)


def extract_contact_info(resume: Resume) -> None:
    """
    Extract contact information from the resume.
    
    Args:
        resume (Resume): The resume object to update with contact information.
    """
    text = resume.raw_text
    
    # Extract name (this is a simple heuristic and may not work for all resumes)
    # Look for name at the beginning of the resume
    lines = text.split('\n')
    for i in range(min(5, len(lines))):
        line = lines[i].strip()
        if line and len(line) < 50 and not any(keyword in line.lower() for keyword in ['resume', 'cv', 'curriculum']):
            resume.name = line
            break
    
    # Extract email
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    email_matches = re.findall(email_pattern, text)
    if email_matches:
        resume.email = email_matches[0]
    
    # Extract phone number
    phone_patterns = [
        r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # 123-456-7890 or 123.456.7890 or 1234567890
        r'\b\(\d{3}\)[-. ]?\d{3}[-.]?\d{4}\b',  # (123) 456-7890 or (123)456-7890
        r'\b\+\d{1,3}[-. ]?\d{3}[-. ]?\d{3}[-. ]?\d{4}\b',  # +1 123-456-7890 or +1-123-456-7890
    ]
    
    for pattern in phone_patterns:
        phone_matches = re.findall(pattern, text)
        if phone_matches:
            resume.phone = phone_matches[0]
            break
    
    # Extract LinkedIn profile
    linkedin_patterns = [
        r'linkedin\.com/in/[\w-]+',
        r'linkedin\.com/profile/[\w-]+',
    ]
    
    for pattern in linkedin_patterns:
        linkedin_matches = re.findall(pattern, text, re.IGNORECASE)
        if linkedin_matches:
            resume.linkedin = linkedin_matches[0]
            break
    
    # Extract website/portfolio
    website_patterns = [
        r'https?://(?:www\.)?[\w-]+\.[\w.-]+(?:/[\w.-]*)*/?',
        r'www\.[\w-]+\.[\w.-]+(?:/[\w.-]*)*/?',
    ]
    
    for pattern in website_patterns:
        website_matches = re.findall(pattern, text)
        if website_matches:
            # Filter out LinkedIn and common job sites
            filtered_websites = [w for w in website_matches if not any(site in w.lower() for site in 
                                ['linkedin', 'indeed', 'monster', 'careerbuilder', 'glassdoor'])]
            if filtered_websites:
                resume.website = filtered_websites[0]
                break
    
    # Extract location
    # This is a simple approach and may not work for all resumes
    location_patterns = [
        r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*,\s[A-Z]{2}\b',  # City, State (e.g., New York, NY)
        r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\s\d{5}\b',  # City Zip (e.g., New York 10001)
    ]
    
    for pattern in location_patterns:
        location_matches = re.findall(pattern, text)
        if location_matches:
            resume.location = location_matches[0]
            break


def extract_summary(resume: Resume) -> None:
    """
    Extract the summary or objective section from the resume.
    
    Args:
        resume (Resume): The resume object to update with summary information.
    """
    text = resume.raw_text
    
    # Look for common summary section headers
    summary_headers = [
        'summary', 'professional summary', 'profile', 'professional profile',
        'objective', 'career objective', 'about me', 'career summary'
    ]
    
    # Split the text into lines
    lines = text.split('\n')
    
    # Find the summary section
    summary_start = -1
    summary_end = -1
    
    for i, line in enumerate(lines):
        line_lower = line.lower().strip()
        
        # Check if this line is a summary header
        if any(header == line_lower or header in line_lower for header in summary_headers):
            summary_start = i + 1
            continue
        
        # If we found the start of the summary, look for the end
        if summary_start != -1 and summary_end == -1:
            # Check if this line is the start of another section
            if line and line[0].isupper() and line[-1] == ':' or \
               line.lower().strip() in ['skills', 'experience', 'education', 'work experience',
                                       'employment', 'projects', 'certifications']:
                summary_end = i
                break
    
    # If we found a summary section, extract it
    if summary_start != -1:
        if summary_end == -1:  # If we didn't find the end, use a reasonable number of lines
            summary_end = min(summary_start + 5, len(lines))
        
        summary_lines = lines[summary_start:summary_end]
        summary_text = ' '.join([line.strip() for line in summary_lines if line.strip()])
        
        # Clean up the summary text
        summary_text = re.sub(r'\s+', ' ', summary_text).strip()
        
        if summary_text:
            resume.summary = summary_text