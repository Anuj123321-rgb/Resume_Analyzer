#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Scoring Module

This module provides functions for scoring resumes based on various criteria.
"""

from typing import Dict, List, Any, Optional
import re
from datetime import datetime

from resume_analyzer.models.resume import Resume
from resume_analyzer.utils.text_utils import calculate_text_stats


def score_resume(resume: Resume) -> float:
    """
    Calculate an overall score for the resume.
    
    Args:
        resume (Resume): The resume to score.
        
    Returns:
        float: The overall score (0-10).
    """
    # Calculate individual component scores
    skill_score = score_skills(resume)
    experience_score = score_experience(resume)
    education_score = score_education(resume)
    format_score = score_format(resume)
    
    # Store component scores in the resume object
    resume.skill_score = skill_score
    resume.experience_score = experience_score
    resume.education_score = education_score
    resume.format_score = format_score
    
    # Calculate weighted average for overall score
    weights = {
        'skills': 0.3,
        'experience': 0.4,
        'education': 0.2,
        'format': 0.1
    }
    
    overall_score = (
        skill_score * weights['skills'] +
        experience_score * weights['experience'] +
        education_score * weights['education'] +
        format_score * weights['format']
    )
    
    # Round to one decimal place
    overall_score = round(overall_score, 1)
    
    # Store overall score in the resume object
    resume.overall_score = overall_score
    
    return overall_score


def score_skills(resume: Resume) -> float:
    """
    Score the skills section of the resume.
    
    Args:
        resume (Resume): The resume to score.
        
    Returns:
        float: The skills score (0-10).
    """
    score = 0.0
    
    # Check if skills exist
    if not resume.skills:
        return score
    
    # Base score on number of skills (up to 5 points)
    num_skills = len(resume.skills)
    if num_skills >= 15:
        score += 5.0
    elif num_skills >= 10:
        score += 4.0
    elif num_skills >= 7:
        score += 3.0
    elif num_skills >= 5:
        score += 2.0
    elif num_skills >= 3:
        score += 1.0
    
    # Add points for skill relevance if skill_scores are available (up to 5 points)
    if resume.skill_scores:
        relevance_score = sum(resume.skill_scores.values()) / max(1, len(resume.skill_scores))
        score += min(5.0, relevance_score)
    else:
        # If no skill_scores, assume average relevance
        score += 2.5
    
    return min(10.0, score)


def score_experience(resume: Resume) -> float:
    """
    Score the experience section of the resume.
    
    Args:
        resume (Resume): The resume to score.
        
    Returns:
        float: The experience score (0-10).
    """
    score = 0.0
    
    # Check if experience exists
    if not resume.experience:
        return score
    
    # Base score on number of experiences (up to 3 points)
    num_experiences = len(resume.experience)
    if num_experiences >= 4:
        score += 3.0
    elif num_experiences >= 3:
        score += 2.5
    elif num_experiences >= 2:
        score += 2.0
    elif num_experiences >= 1:
        score += 1.0
    
    # Add points for experience duration (up to 3 points)
    total_months = 0
    for exp in resume.experience:
        # Calculate duration if start_date and end_date are available
        if exp['start_date'] and exp['end_date'] and exp['end_date'].lower() != 'present':
            try:
                # Try to parse dates in various formats
                for fmt in ['%b %Y', '%B %Y', '%m/%Y', '%m-%Y', '%Y']:
                    try:
                        start_date = datetime.strptime(exp['start_date'], fmt)
                        break
                    except ValueError:
                        continue
                else:
                    # If no format worked, skip this experience
                    continue
                
                for fmt in ['%b %Y', '%B %Y', '%m/%Y', '%m-%Y', '%Y']:
                    try:
                        end_date = datetime.strptime(exp['end_date'], fmt)
                        break
                    except ValueError:
                        continue
                else:
                    # If no format worked, skip this experience
                    continue
                
                # Calculate months between dates
                months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
                total_months += max(0, months)
            except (ValueError, AttributeError):
                # If date parsing fails, assume 12 months
                total_months += 12
        elif exp['start_date'] and exp['end_date'] and exp['end_date'].lower() == 'present':
            try:
                # Try to parse start date
                for fmt in ['%b %Y', '%B %Y', '%m/%Y', '%m-%Y', '%Y']:
                    try:
                        start_date = datetime.strptime(exp['start_date'], fmt)
                        break
                    except ValueError:
                        continue
                else:
                    # If no format worked, skip this experience
                    continue
                
                # Calculate months until now
                now = datetime.now()
                months = (now.year - start_date.year) * 12 + (now.month - start_date.month)
                total_months += max(0, months)
            except (ValueError, AttributeError):
                # If date parsing fails, assume 12 months
                total_months += 12
        else:
            # If dates are not available, assume 12 months
            total_months += 12
    
    # Score based on total months of experience
    if total_months >= 60:  # 5+ years
        score += 3.0
    elif total_months >= 36:  # 3+ years
        score += 2.5
    elif total_months >= 24:  # 2+ years
        score += 2.0
    elif total_months >= 12:  # 1+ year
        score += 1.5
    elif total_months > 0:  # Some experience
        score += 1.0
    
    # Add points for responsibilities and descriptions (up to 2 points)
    has_responsibilities = any(exp.get('responsibilities') for exp in resume.experience)
    has_descriptions = any(exp.get('description') for exp in resume.experience)
    
    if has_responsibilities and has_descriptions:
        score += 2.0
    elif has_responsibilities or has_descriptions:
        score += 1.0
    
    # Add points for job titles and companies (up to 2 points)
    has_titles = all(exp.get('title') for exp in resume.experience)
    has_companies = all(exp.get('company') for exp in resume.experience)
    
    if has_titles and has_companies:
        score += 2.0
    elif has_titles or has_companies:
        score += 1.0
    
    return min(10.0, score)


def score_education(resume: Resume) -> float:
    """
    Score the education section of the resume.
    
    Args:
        resume (Resume): The resume to score.
        
    Returns:
        float: The education score (0-10).
    """
    score = 0.0
    
    # Check if education exists
    if not resume.education:
        return score
    
    # Base score on number of education entries (up to 3 points)
    num_education = len(resume.education)
    if num_education >= 3:
        score += 3.0
    elif num_education >= 2:
        score += 2.0
    elif num_education >= 1:
        score += 1.0
    
    # Add points for degree level (up to 4 points)
    highest_degree_score = 0
    for edu in resume.education:
        degree = edu.get('degree', '').lower()
        
        # Check for PhD or Doctorate
        if re.search(r'ph\.?d|doct?or|doctorate', degree):
            degree_score = 4.0
        # Check for Master's
        elif re.search(r'master|ms|ma|mba|m\.s|m\.a', degree):
            degree_score = 3.0
        # Check for Bachelor's
        elif re.search(r'bachelor|bs|ba|b\.s|b\.a', degree):
            degree_score = 2.0
        # Check for Associate's or certificate
        elif re.search(r'associate|certificate|diploma', degree):
            degree_score = 1.0
        else:
            degree_score = 0.5
        
        highest_degree_score = max(highest_degree_score, degree_score)
    
    score += highest_degree_score
    
    # Add points for completeness of education entries (up to 3 points)
    completeness_score = 0
    for edu in resume.education:
        entry_score = 0
        
        # Check for institution
        if edu.get('institution'):
            entry_score += 0.5
        
        # Check for field of study
        if edu.get('field'):
            entry_score += 0.5
        
        # Check for dates
        if edu.get('start_date') or edu.get('end_date'):
            entry_score += 0.5
        
        # Check for GPA
        if edu.get('gpa'):
            entry_score += 0.5
        
        # Check for location
        if edu.get('location'):
            entry_score += 0.5
        
        # Check for description
        if edu.get('description'):
            entry_score += 0.5
        
        # Add the entry score (max 3 points per entry)
        completeness_score += min(3.0, entry_score)
    
    # Average the completeness score and add it (max 3 points)
    if num_education > 0:
        avg_completeness = completeness_score / num_education
        score += min(3.0, avg_completeness)
    
    return min(10.0, score)


def score_format(resume: Resume) -> float:
    """
    Score the format and structure of the resume.
    
    Args:
        resume (Resume): The resume to score.
        
    Returns:
        float: The format score (0-10).
    """
    score = 5.0  # Start with a middle score
    
    # Check if the resume has basic contact information (up to 2 points)
    contact_score = 0
    if resume.name:
        contact_score += 0.5
    if resume.email:
        contact_score += 0.5
    if resume.phone:
        contact_score += 0.5
    if resume.location:
        contact_score += 0.5
    
    score += min(2.0, contact_score)
    
    # Check if the resume has a summary (up to 1 point)
    if resume.summary:
        score += 1.0
    
    # Check text statistics (up to 2 points)
    if resume.raw_text:
        stats = calculate_text_stats(resume.raw_text)
        
        # Check word count (too short or too long is not good)
        word_count = stats['word_count']
        if 300 <= word_count <= 700:
            score += 1.0
        elif 200 <= word_count < 300 or 700 < word_count <= 1000:
            score += 0.5
        
        # Check lexical diversity (variety of words used)
        lexical_diversity = stats['lexical_diversity']
        if 0.4 <= lexical_diversity <= 0.7:
            score += 1.0
        elif 0.3 <= lexical_diversity < 0.4 or 0.7 < lexical_diversity <= 0.8:
            score += 0.5
    
    return min(10.0, score)


def generate_recommendations(resume: Resume) -> List[str]:
    """
    Generate recommendations for improving the resume.
    
    Args:
        resume (Resume): The resume to analyze.
        
    Returns:
        List[str]: A list of recommendations.
    """
    recommendations = []
    
    # Skill recommendations
    if not resume.skills or len(resume.skills) < 5:
        recommendations.append("Add more skills to your resume, aim for at least 5-10 relevant skills.")
    
    # Experience recommendations
    if not resume.experience:
        recommendations.append("Add work experience to your resume, even if it's internships or volunteer work.")
    else:
        for exp in resume.experience:
            if not exp.get('responsibilities') and not exp.get('description'):
                recommendations.append("Add detailed responsibilities or descriptions to your work experience.")
                break
    
    # Education recommendations
    if not resume.education:
        recommendations.append("Add your educational background to your resume.")
    
    # Contact information recommendations
    missing_contact = []
    if not resume.name:
        missing_contact.append("name")
    if not resume.email:
        missing_contact.append("email")
    if not resume.phone:
        missing_contact.append("phone number")
    
    if missing_contact:
        recommendations.append(f"Add your {', '.join(missing_contact)} to your contact information.")
    
    # Summary recommendations
    if not resume.summary:
        recommendations.append("Add a professional summary to highlight your key qualifications and career objectives.")
    
    # Format recommendations
    if resume.raw_text:
        stats = calculate_text_stats(resume.raw_text)
        
        if stats['word_count'] > 1000:
            recommendations.append("Your resume is quite long. Consider condensing it to 1-2 pages (300-700 words).")
        elif stats['word_count'] < 200:
            recommendations.append("Your resume is quite short. Consider adding more details about your experience and skills.")
    
    # Add general recommendations if there are few specific ones
    if len(recommendations) < 3:
        general_recommendations = [
            "Quantify your achievements with specific numbers and metrics where possible.",
            "Tailor your resume for each job application to highlight relevant skills and experience.",
            "Use action verbs to describe your responsibilities and achievements.",
            "Proofread your resume for spelling and grammar errors.",
            "Consider adding a LinkedIn profile or personal website to your contact information.",
            "Organize your resume in reverse chronological order (most recent experience first)."
        ]
        
        # Add general recommendations until we have at least 3
        for rec in general_recommendations:
            if rec not in recommendations:
                recommendations.append(rec)
                if len(recommendations) >= 3:
                    break
    
    # Store recommendations in the resume object
    resume.recommendations = recommendations
    
    return recommendations