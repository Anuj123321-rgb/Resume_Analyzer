#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Experience Analyzer Module

This module provides functionality for analyzing and extracting work experience
and education information from resumes.
"""

import re
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

from resume_analyzer.models.resume import Resume


def analyze(resume: Resume) -> None:
    """
    Analyze the resume and extract experience and education information.
    
    Args:
        resume (Resume): The resume object to analyze.
    """
    # Extract work experience
    extract_experience(resume)
    
    # Extract education
    extract_education(resume)
    
    # Score the experience and education
    score_experience_education(resume)


def extract_experience(resume: Resume) -> None:
    """
    Extract work experience from the resume.
    
    Args:
        resume (Resume): The resume object to update with experience information.
    """
    text = resume.raw_text
    
    # Extract the experience section
    experience_section = _extract_section(text, [
        'experience', 'work experience', 'employment history', 'professional experience',
        'career history', 'work history'
    ])
    
    if not experience_section:
        return
    
    # Split the experience section into entries
    experience_entries = _split_section_into_entries(experience_section)
    
    for entry in experience_entries:
        # Extract company and title
        company, title = _extract_company_title(entry)
        
        if not company:
            continue
        
        # Extract dates
        start_date, end_date = _extract_dates(entry)
        
        # Extract location
        location = _extract_location(entry)
        
        # Extract description and responsibilities
        description, responsibilities = _extract_description_responsibilities(entry)
        
        # Add the experience to the resume
        resume.add_experience(
            company=company,
            title=title,
            start_date=start_date,
            end_date=end_date,
            location=location,
            description=description,
            responsibilities=responsibilities
        )


def extract_education(resume: Resume) -> None:
    """
    Extract education information from the resume.
    
    Args:
        resume (Resume): The resume object to update with education information.
    """
    text = resume.raw_text
    
    # Extract the education section
    education_section = _extract_section(text, [
        'education', 'academic background', 'educational background', 'academic history',
        'educational history', 'academic qualifications', 'educational qualifications'
    ])
    
    if not education_section:
        return
    
    # Split the education section into entries
    education_entries = _split_section_into_entries(education_section)
    
    for entry in education_entries:
        # Extract institution and degree
        institution, degree = _extract_institution_degree(entry)
        
        if not institution:
            continue
        
        # Extract field of study
        field = _extract_field_of_study(entry, degree)
        
        # Extract dates
        start_date, end_date = _extract_dates(entry)
        
        # Extract location
        location = _extract_location(entry)
        
        # Extract GPA
        gpa = _extract_gpa(entry)
        
        # Extract description
        description = _extract_education_description(entry)
        
        # Add the education to the resume
        resume.add_education(
            institution=institution,
            degree=degree,
            field=field,
            start_date=start_date,
            end_date=end_date,
            gpa=gpa,
            location=location,
            description=description
        )


def _extract_section(text: str, section_headers: List[str]) -> Optional[str]:
    """
    Extract a section from the resume text based on common section headers.
    
    Args:
        text (str): The resume text.
        section_headers (List[str]): List of possible section headers.
        
    Returns:
        Optional[str]: The extracted section text if found, None otherwise.
    """
    # Split the text into lines
    lines = text.split('\n')
    
    # Find the section
    section_start = -1
    section_end = -1
    
    for i, line in enumerate(lines):
        line_lower = line.lower().strip()
        
        # Check if this line is a section header
        if any(header == line_lower or header in line_lower for header in section_headers):
            section_start = i + 1
            continue
        
        # If we found the start of the section, look for the end
        if section_start != -1 and section_end == -1:
            # Check if this line is the start of another section
            if line and line[0].isupper() and (line[-1] == ':' or line.isupper()) or \
               line.lower().strip() in ['skills', 'education', 'experience', 'projects',
                                       'certifications', 'summary', 'objective', 'profile']:
                section_end = i
                break
    
    # If we found a section, extract it
    if section_start != -1:
        if section_end == -1:  # If we didn't find the end, use the rest of the text
            section_end = len(lines)
        
        section_lines = lines[section_start:section_end]
        section_text = '\n'.join([line for line in section_lines if line.strip()])
        
        return section_text
    
    return None


def _split_section_into_entries(section_text: str) -> List[str]:
    """
    Split a section into individual entries.
    
    Args:
        section_text (str): The section text.
        
    Returns:
        List[str]: List of entry texts.
    """
    # Try to split by common patterns
    entries = []
    
    # Pattern 1: Entries separated by blank lines
    if '\n\n' in section_text:
        entries = [entry.strip() for entry in section_text.split('\n\n') if entry.strip()]
    
    # Pattern 2: Entries starting with dates or company names
    if not entries:
        lines = section_text.split('\n')
        current_entry = []
        
        for line in lines:
            # Check if this line looks like the start of a new entry
            if re.match(r'\d{4}|\d{2}/\d{2}|\d{2}-\d{2}|[A-Z][a-z]+\s[A-Z][a-z]+', line.strip()) and current_entry:
                entries.append('\n'.join(current_entry))
                current_entry = [line]
            else:
                current_entry.append(line)
        
        if current_entry:
            entries.append('\n'.join(current_entry))
    
    # If we still couldn't split, treat the whole section as one entry
    if not entries:
        entries = [section_text]
    
    return entries


def _extract_company_title(entry: str) -> Tuple[str, str]:
    """
    Extract company name and job title from an experience entry.
    
    Args:
        entry (str): The experience entry text.
        
    Returns:
        Tuple[str, str]: The company name and job title.
    """
    lines = entry.split('\n')
    company = ""
    title = ""
    
    # Look for patterns like "Company Name - Job Title" or "Job Title at Company Name"
    for line in lines[:3]:  # Check the first few lines
        line = line.strip()
        
        # Pattern: Company Name - Job Title
        if ' - ' in line:
            parts = line.split(' - ', 1)
            company = parts[0].strip()
            title = parts[1].strip()
            break
        
        # Pattern: Job Title at Company Name
        if ' at ' in line.lower():
            parts = re.split(r'\s+at\s+', line, flags=re.IGNORECASE, maxsplit=1)
            title = parts[0].strip()
            company = parts[1].strip()
            break
        
        # Pattern: Job Title, Company Name
        if ',' in line:
            parts = line.split(',', 1)
            title = parts[0].strip()
            company = parts[1].strip()
            break
    
    # If we couldn't find a pattern, use heuristics
    if not company or not title:
        # Assume the first line might contain both or one of them
        first_line = lines[0].strip()
        
        if not company and not title:
            # Just use the first line as the company name
            company = first_line
        elif not company:
            # Try to extract company from the second line
            if len(lines) > 1:
                company = lines[1].strip()
        elif not title:
            # Try to extract title from the second line
            if len(lines) > 1:
                title = lines[1].strip()
    
    return company, title


def _extract_dates(entry: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract start and end dates from an entry.
    
    Args:
        entry (str): The entry text.
        
    Returns:
        Tuple[Optional[str], Optional[str]]: The start and end dates.
    """
    # Look for common date patterns
    date_patterns = [
        # MM/YYYY - MM/YYYY
        r'(\d{1,2}/\d{4})\s*-\s*(\d{1,2}/\d{4}|Present|Current|Now)',
        # MM-YYYY - MM-YYYY
        r'(\d{1,2}-\d{4})\s*-\s*(\d{1,2}-\d{4}|Present|Current|Now)',
        # YYYY - YYYY
        r'(\d{4})\s*-\s*(\d{4}|Present|Current|Now)',
        # Month YYYY - Month YYYY
        r'([A-Z][a-z]+\s+\d{4})\s*-\s*([A-Z][a-z]+\s+\d{4}|Present|Current|Now)',
        # Month Year - Month Year (e.g., January 2020 - March 2022)
        r'([A-Z][a-z]+\s+\d{4})\s*-\s*([A-Z][a-z]+\s+\d{4}|Present|Current|Now)'
    ]
    
    for pattern in date_patterns:
        matches = re.search(pattern, entry)
        if matches:
            start_date = matches.group(1)
            end_date = matches.group(2)
            
            # Normalize "Present" variations
            if end_date in ['Present', 'Current', 'Now']:
                end_date = 'Present'
            
            return start_date, end_date
    
    return None, None


def _extract_location(entry: str) -> Optional[str]:
    """
    Extract location from an entry.
    
    Args:
        entry (str): The entry text.
        
    Returns:
        Optional[str]: The location if found, None otherwise.
    """
    # Look for common location patterns
    location_patterns = [
        # City, State
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s+([A-Z]{2})',
        # City, Country
        r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
        # Location: City, State
        r'Location:\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s+([A-Z]{2}|[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
    ]
    
    for pattern in location_patterns:
        matches = re.search(pattern, entry)
        if matches:
            city = matches.group(1)
            state_country = matches.group(2)
            return f"{city}, {state_country}"
    
    return None


def _extract_description_responsibilities(entry: str) -> Tuple[Optional[str], List[str]]:
    """
    Extract job description and responsibilities from an experience entry.
    
    Args:
        entry (str): The experience entry text.
        
    Returns:
        Tuple[Optional[str], List[str]]: The job description and list of responsibilities.
    """
    lines = entry.split('\n')
    description_lines = []
    responsibilities = []
    
    # Skip the first few lines (likely company, title, dates)
    start_idx = min(3, len(lines))
    
    # Check if there are bullet points for responsibilities
    for i in range(start_idx, len(lines)):
        line = lines[i].strip()
        
        # Check for bullet points or numbered lists
        if line.startswith('•') or line.startswith('-') or line.startswith('*') or re.match(r'^\d+\.', line):
            # Remove the bullet point or number
            responsibility = re.sub(r'^[•\-*]\s*|^\d+\.\s*', '', line).strip()
            if responsibility:
                responsibilities.append(responsibility)
        elif line:
            description_lines.append(line)
    
    description = ' '.join(description_lines) if description_lines else None
    
    return description, responsibilities


def _extract_institution_degree(entry: str) -> Tuple[str, str]:
    """
    Extract institution name and degree from an education entry.
    
    Args:
        entry (str): The education entry text.
        
    Returns:
        Tuple[str, str]: The institution name and degree.
    """
    lines = entry.split('\n')
    institution = ""
    degree = ""
    
    # Look for patterns like "Institution Name - Degree" or "Degree at Institution Name"
    for line in lines[:3]:  # Check the first few lines
        line = line.strip()
        
        # Pattern: Institution Name - Degree
        if ' - ' in line:
            parts = line.split(' - ', 1)
            institution = parts[0].strip()
            degree = parts[1].strip()
            break
        
        # Pattern: Degree at Institution Name
        if ' at ' in line.lower():
            parts = re.split(r'\s+at\s+', line, flags=re.IGNORECASE, maxsplit=1)
            degree = parts[0].strip()
            institution = parts[1].strip()
            break
        
        # Pattern: Degree, Institution Name
        if ',' in line:
            parts = line.split(',', 1)
            degree = parts[0].strip()
            institution = parts[1].strip()
            break
    
    # If we couldn't find a pattern, use heuristics
    if not institution or not degree:
        # Assume the first line might contain both or one of them
        first_line = lines[0].strip()
        
        if not institution and not degree:
            # Just use the first line as the institution name
            institution = first_line
        elif not institution:
            # Try to extract institution from the second line
            if len(lines) > 1:
                institution = lines[1].strip()
        elif not degree:
            # Try to extract degree from the second line
            if len(lines) > 1:
                degree = lines[1].strip()
    
    # Look for common degree keywords if degree is still empty
    if not degree:
        degree_keywords = [
            'Bachelor', 'Master', 'PhD', 'Doctorate', 'Associate', 'BS', 'BA', 'MS', 'MA',
            'BSc', 'MSc', 'BBA', 'MBA', 'B.S.', 'M.S.', 'B.A.', 'M.A.', 'Ph.D.', 'B.Tech',
            'M.Tech', 'B.E.', 'M.E.', 'Certificate', 'Diploma'
        ]
        
        for line in lines:
            for keyword in degree_keywords:
                if keyword in line:
                    degree = line.strip()
                    break
            if degree:
                break
    
    return institution, degree


def _extract_field_of_study(entry: str, degree: str) -> Optional[str]:
    """
    Extract field of study from an education entry.
    
    Args:
        entry (str): The education entry text.
        degree (str): The degree text.
        
    Returns:
        Optional[str]: The field of study if found, None otherwise.
    """
    # Check if the field is already in the degree
    field_patterns = [
        r'in\s+([A-Za-z\s]+)',  # "in Computer Science"
        r'of\s+([A-Za-z\s]+)',  # "of Business Administration"
    ]
    
    for pattern in field_patterns:
        matches = re.search(pattern, degree)
        if matches:
            return matches.group(1).strip()
    
    # Look for field in the entry
    lines = entry.split('\n')
    
    # Skip the first few lines (likely institution, degree, dates)
    start_idx = min(3, len(lines))
    
    for i in range(start_idx, len(lines)):
        line = lines[i].strip()
        
        # Look for common field indicators
        field_indicators = [
            'Major:', 'Field:', 'Concentration:', 'Specialization:'
        ]
        
        for indicator in field_indicators:
            if indicator in line:
                return line.split(indicator, 1)[1].strip()
    
    return None


def _extract_gpa(entry: str) -> Optional[float]:
    """
    Extract GPA from an education entry.
    
    Args:
        entry (str): The education entry text.
        
    Returns:
        Optional[float]: The GPA if found, None otherwise.
    """
    # Look for common GPA patterns
    gpa_patterns = [
        r'GPA:\s*(\d+\.\d+)',  # GPA: 3.8
        r'GPA\s+of\s+(\d+\.\d+)',  # GPA of 3.8
        r'(\d+\.\d+)\s+GPA',  # 3.8 GPA
    ]
    
    for pattern in gpa_patterns:
        matches = re.search(pattern, entry)
        if matches:
            try:
                return float(matches.group(1))
            except ValueError:
                pass
    
    return None


def _extract_education_description(entry: str) -> Optional[str]:
    """
    Extract education description from an education entry.
    
    Args:
        entry (str): The education entry text.
        
    Returns:
        Optional[str]: The education description if found, None otherwise.
    """
    lines = entry.split('\n')
    description_lines = []
    
    # Skip the first few lines (likely institution, degree, dates)
    start_idx = min(3, len(lines))
    
    for i in range(start_idx, len(lines)):
        line = lines[i].strip()
        
        # Skip lines that look like GPA or field indicators
        if any(indicator in line for indicator in ['GPA:', 'Major:', 'Field:', 'Concentration:', 'Specialization:']):
            continue
        
        # Skip bullet points
        if line.startswith('•') or line.startswith('-') or line.startswith('*') or re.match(r'^\d+\.', line):
            continue
        
        if line:
            description_lines.append(line)
    
    description = ' '.join(description_lines) if description_lines else None
    
    return description


def score_experience_education(resume: Resume) -> None:
    """
    Score the experience and education sections of the resume.
    
    Args:
        resume (Resume): The resume object to update with scores.
    """
    # Score experience
    experience_score = _score_experience(resume)
    resume.experience_score = experience_score
    
    # Score education
    education_score = _score_education(resume)
    resume.education_score = education_score
    
    # Calculate overall score (weighted average)
    resume.overall_score = 0.5 * experience_score + 0.3 * education_score + 0.2 * sum(resume.skill_scores.values())
    
    # Add recommendations based on experience and education analysis
    _add_experience_education_recommendations(resume)


def _score_experience(resume: Resume) -> float:
    """
    Score the experience section of the resume.
    
    Args:
        resume (Resume): The resume object.
        
    Returns:
        float: The experience score (0-10).
    """
    if not resume.experience:
        return 0.0
    
    # Base score depends on number of experiences
    base_score = min(5.0, len(resume.experience))
    
    # Additional points for quality of experience
    quality_score = 0.0
    
    for exp in resume.experience:
        # Points for having responsibilities
        if exp['responsibilities']:
            quality_score += 0.5 * min(1.0, len(exp['responsibilities']) / 3.0)
        
        # Points for detailed description
        if exp['description'] and len(exp['description']) > 50:
            quality_score += 0.5
        
        # Points for having dates
        if exp['start_date'] and exp['end_date']:
            quality_score += 0.5
        
        # Points for having location
        if exp['location']:
            quality_score += 0.25
    
    # Normalize quality score
    quality_score = min(5.0, quality_score)
    
    # Combine scores
    total_score = base_score + quality_score
    
    return total_score


def _score_education(resume: Resume) -> float:
    """
    Score the education section of the resume.
    
    Args:
        resume (Resume): The resume object.
        
    Returns:
        float: The education score (0-10).
    """
    if not resume.education:
        return 0.0
    
    # Base score depends on number of education entries
    base_score = min(5.0, len(resume.education) * 2.5)
    
    # Additional points for quality of education
    quality_score = 0.0
    
    for edu in resume.education:
        # Points for having degree and field
        if edu['degree']:
            quality_score += 1.0
        
        if edu['field']:
            quality_score += 1.0
        
        # Points for having dates
        if edu['start_date'] and edu['end_date']:
            quality_score += 0.5
        
        # Points for having GPA
        if edu['gpa']:
            quality_score += 1.0
        
        # Points for having description
        if edu['description']:
            quality_score += 0.5
    
    # Normalize quality score
    quality_score = min(5.0, quality_score)
    
    # Combine scores
    total_score = base_score + quality_score
    
    return total_score


def _add_experience_education_recommendations(resume: Resume) -> None:
    """
    Add recommendations based on experience and education analysis.
    
    Args:
        resume (Resume): The resume object to update with recommendations.
    """
    # Experience recommendations
    if not resume.experience:
        resume.add_recommendation("Add work experience to your resume, even if it's internships or volunteer work.")
    elif len(resume.experience) < 2:
        resume.add_recommendation("Consider adding more work experiences to demonstrate your career progression.")
    
    for exp in resume.experience:
        if not exp['responsibilities']:
            resume.add_recommendation(f"Add bullet points describing your responsibilities and achievements at {exp['company']}.")
        elif len(exp['responsibilities']) < 3:
            resume.add_recommendation(f"Add more bullet points for your role at {exp['company']} to highlight your achievements.")
        
        if not exp['start_date'] or not exp['end_date']:
            resume.add_recommendation(f"Add specific dates for your position at {exp['company']}.")
    
    # Education recommendations
    if not resume.education:
        resume.add_recommendation("Add your educational background to your resume.")
    
    for edu in resume.education:
        if not edu['field']:
            resume.add_recommendation(f"Specify your field of study at {edu['institution']}.")
        
        if not edu['start_date'] or not edu['end_date']:
            resume.add_recommendation(f"Add specific dates for your education at {edu['institution']}.")
        
        if not edu['gpa'] and edu['degree'] and any(keyword in edu['degree'] for keyword in ['Bachelor', 'Master', 'PhD']):
            resume.add_recommendation(f"Consider adding your GPA for your {edu['degree']} if it's above 3.0.")
    
    # Overall recommendations
    if resume.overall_score < 5.0:
        resume.add_recommendation("Your resume needs significant improvement. Focus on adding more detailed work experiences and skills.")
    elif resume.overall_score < 7.0:
        resume.add_recommendation("Your resume is good but could be improved. Consider adding more specific achievements and quantifiable results.")
    else:
        resume.add_recommendation("Your resume is strong. Consider tailoring it further for specific job applications.")