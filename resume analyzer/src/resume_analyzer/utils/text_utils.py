#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Text Utilities Module

This module provides utility functions for text processing and analysis.
"""

import re
from typing import List, Dict, Any, Tuple, Set


def clean_text(text: str) -> str:
    """
    Clean and normalize text for analysis.
    
    Args:
        text (str): The text to clean.
        
    Returns:
        str: The cleaned text.
    """
    # Replace multiple whitespace with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters that aren't useful for analysis
    text = re.sub(r'[^\w\s@.\-:,;()/\\]', ' ', text)
    
    # Normalize line breaks
    text = re.sub(r'\n+', '\n', text)
    
    return text.strip()


def extract_sections(text: str) -> Dict[str, str]:
    """
    Extract sections from resume text based on common section headers.
    
    Args:
        text (str): The resume text.
        
    Returns:
        Dict[str, str]: A dictionary mapping section names to their content.
    """
    # Common section headers in resumes
    section_patterns = {
        'summary': r'(?i)(\n|^)(summary|professional\s+summary|profile|about\s+me|objective)\s*:?\s*\n',
        'experience': r'(?i)(\n|^)(experience|work\s+experience|employment|work\s+history|professional\s+experience)\s*:?\s*\n',
        'education': r'(?i)(\n|^)(education|educational\s+background|academic\s+background|academic\s+history|qualifications)\s*:?\s*\n',
        'skills': r'(?i)(\n|^)(skills|technical\s+skills|core\s+competencies|competencies|expertise|proficiencies)\s*:?\s*\n',
        'certifications': r'(?i)(\n|^)(certifications|certificates|professional\s+certifications|credentials)\s*:?\s*\n',
        'projects': r'(?i)(\n|^)(projects|personal\s+projects|professional\s+projects|key\s+projects)\s*:?\s*\n',
        'languages': r'(?i)(\n|^)(languages|language\s+proficiencies)\s*:?\s*\n',
        'interests': r'(?i)(\n|^)(interests|hobbies|activities)\s*:?\s*\n',
        'references': r'(?i)(\n|^)(references|professional\s+references)\s*:?\s*\n',
        'publications': r'(?i)(\n|^)(publications|papers|articles)\s*:?\s*\n',
        'awards': r'(?i)(\n|^)(awards|honors|achievements|recognitions)\s*:?\s*\n',
        'volunteer': r'(?i)(\n|^)(volunteer|volunteering|community\s+service|community\s+involvement)\s*:?\s*\n'
    }
    
    # Find all section headers and their positions
    sections = {}
    section_positions = []
    
    for section_name, pattern in section_patterns.items():
        matches = list(re.finditer(pattern, text))
        for match in matches:
            section_positions.append((match.start(), section_name, match.group()))
    
    # Sort by position
    section_positions.sort()
    
    # Extract section content
    for i, (pos, section_name, header) in enumerate(section_positions):
        # Determine the end of this section (start of next section or end of text)
        if i < len(section_positions) - 1:
            end_pos = section_positions[i + 1][0]
        else:
            end_pos = len(text)
        
        # Extract the section content (excluding the header)
        header_end = pos + len(header)
        section_content = text[header_end:end_pos].strip()
        
        # Store the section
        sections[section_name] = section_content
    
    # If no sections were found, create a default 'content' section with all text
    if not sections:
        sections['content'] = text
    
    return sections


def split_into_sentences(text: str) -> List[str]:
    """
    Split text into sentences.
    
    Args:
        text (str): The text to split.
        
    Returns:
        List[str]: A list of sentences.
    """
    # Simple sentence splitting based on common sentence terminators
    # This is a basic implementation and may not handle all cases correctly
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def extract_bullet_points(text: str) -> List[str]:
    """
    Extract bullet points from text.
    
    Args:
        text (str): The text to extract bullet points from.
        
    Returns:
        List[str]: A list of bullet points.
    """
    # Common bullet point markers
    bullet_pattern = r'(?m)^\s*[•●\-\*\+◦○⦿⦾⦿⚫⚪⚬⚭⚮]\s+(.+?)(?=\n\s*[•●\-\*\+◦○⦿⦾⦿⚫⚪⚬⚭⚮]\s+|$)'
    
    # Find all bullet points
    bullet_points = re.findall(bullet_pattern, text)
    
    # If no bullet points were found with the pattern, try splitting by newlines
    if not bullet_points and '\n' in text:
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Check if lines might be bullet points without markers
        if len(lines) >= 3:  # At least 3 lines to consider them as potential bullet points
            bullet_points = lines
    
    return bullet_points


def calculate_keyword_density(text: str, keywords: List[str]) -> Dict[str, float]:
    """
    Calculate the density of keywords in the text.
    
    Args:
        text (str): The text to analyze.
        keywords (List[str]): The keywords to search for.
        
    Returns:
        Dict[str, float]: A dictionary mapping keywords to their density.
    """
    # Normalize text for comparison
    text_lower = text.lower()
    word_count = len(re.findall(r'\b\w+\b', text_lower))
    
    if word_count == 0:
        return {keyword: 0.0 for keyword in keywords}
    
    # Calculate density for each keyword
    density = {}
    for keyword in keywords:
        keyword_lower = keyword.lower()
        # Count occurrences of the keyword
        count = len(re.findall(r'\b' + re.escape(keyword_lower) + r'\b', text_lower))
        # Calculate density as percentage of total words
        density[keyword] = (count / word_count) * 100
    
    return density


def find_date_ranges(text: str) -> List[Tuple[str, str]]:
    """
    Find date ranges in text (e.g., "Jan 2020 - Present").
    
    Args:
        text (str): The text to search for date ranges.
        
    Returns:
        List[Tuple[str, str]]: A list of (start_date, end_date) tuples.
    """
    # Pattern for date ranges
    # This pattern matches common date formats like "Jan 2020 - Present" or "01/2020 - 12/2021"
    date_range_pattern = r'(?i)((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|january|february|march|april|june|july|august|september|october|november|december|\d{1,2})[\s./\-]\d{2,4})\s*(?:-|to|–|until|through)\s*((?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|january|february|march|april|june|july|august|september|october|november|december|\d{1,2})[\s./\-]\d{2,4}|present|current|now)'
    
    # Find all date ranges
    date_ranges = re.findall(date_range_pattern, text)
    
    # Clean up the matches
    cleaned_ranges = []
    for start_date, end_date in date_ranges:
        start_date = start_date.strip()
        end_date = end_date.strip()
        cleaned_ranges.append((start_date, end_date))
    
    return cleaned_ranges


def extract_urls(text: str) -> List[str]:
    """
    Extract URLs from text.
    
    Args:
        text (str): The text to extract URLs from.
        
    Returns:
        List[str]: A list of URLs.
    """
    # Pattern for URLs
    url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[\w/\-?=&.]*'
    
    # Find all URLs
    urls = re.findall(url_pattern, text)
    
    return urls


def extract_emails(text: str) -> List[str]:
    """
    Extract email addresses from text.
    
    Args:
        text (str): The text to extract email addresses from.
        
    Returns:
        List[str]: A list of email addresses.
    """
    # Pattern for email addresses
    email_pattern = r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}'
    
    # Find all email addresses
    emails = re.findall(email_pattern, text)
    
    return emails


def extract_phone_numbers(text: str) -> List[str]:
    """
    Extract phone numbers from text.
    
    Args:
        text (str): The text to extract phone numbers from.
        
    Returns:
        List[str]: A list of phone numbers.
    """
    # Pattern for phone numbers
    # This pattern matches common phone number formats
    phone_pattern = r'(?:\+\d{1,3}[\s-]?)?(?:\(\d{1,4}\)[\s-]?)?\d{1,4}[\s-]?\d{1,4}[\s-]?\d{1,4}'
    
    # Find all phone numbers
    phones = re.findall(phone_pattern, text)
    
    # Clean up the matches
    cleaned_phones = []
    for phone in phones:
        # Remove whitespace and common separators
        cleaned_phone = re.sub(r'[\s-]', '', phone)
        # Only keep if it's a reasonable length for a phone number
        if 7 <= len(cleaned_phone) <= 15:
            cleaned_phones.append(phone.strip())
    
    return cleaned_phones


def calculate_text_stats(text: str) -> Dict[str, Any]:
    """
    Calculate various statistics about the text.
    
    Args:
        text (str): The text to analyze.
        
    Returns:
        Dict[str, Any]: A dictionary of text statistics.
    """
    # Word count
    words = re.findall(r'\b\w+\b', text)
    word_count = len(words)
    
    # Sentence count
    sentences = split_into_sentences(text)
    sentence_count = len(sentences)
    
    # Average word length
    avg_word_length = sum(len(word) for word in words) / max(1, word_count)
    
    # Average sentence length
    avg_sentence_length = word_count / max(1, sentence_count)
    
    # Unique words
    unique_words = set(word.lower() for word in words)
    unique_word_count = len(unique_words)
    
    # Lexical diversity (unique words / total words)
    lexical_diversity = unique_word_count / max(1, word_count)
    
    return {
        'word_count': word_count,
        'sentence_count': sentence_count,
        'char_count': len(text),
        'avg_word_length': avg_word_length,
        'avg_sentence_length': avg_sentence_length,
        'unique_word_count': unique_word_count,
        'lexical_diversity': lexical_diversity
    }