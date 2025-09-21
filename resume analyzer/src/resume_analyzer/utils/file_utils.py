#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
File Utilities Module

This module provides utility functions for file operations such as saving
analysis results in different formats.
"""

import os
import json
from typing import Dict, Any

from resume_analyzer.models.resume import Resume


def save_json(data: Dict[str, Any], output_path: str) -> None:
    """
    Save data as a JSON file.
    
    Args:
        data (Dict[str, Any]): The data to save.
        output_path (str): The path to save the JSON file.
    """
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the data as JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_text(text: str, output_path: str) -> None:
    """
    Save text to a file.
    
    Args:
        text (str): The text to save.
        output_path (str): The path to save the text file.
    """
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the text
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)


def save_html(resume: Resume, output_path: str) -> None:
    """
    Save resume analysis as an HTML file.
    
    Args:
        resume (Resume): The resume object to save.
        output_path (str): The path to save the HTML file.
    """
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Generate HTML content
    html_content = _generate_html(resume)
    
    # Save the HTML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


def _generate_html(resume: Resume) -> str:
    """
    Generate HTML content for the resume analysis.
    
    Args:
        resume (Resume): The resume object.
        
    Returns:
        str: The HTML content.
    """
    # HTML template
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Resume Analysis: {filename}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1, h2, h3 {{
                color: #2c3e50;
            }}
            .section {{
                margin-bottom: 30px;
                border-bottom: 1px solid #eee;
                padding-bottom: 20px;
            }}
            .score {{
                font-size: 24px;
                font-weight: bold;
                color: {score_color};
            }}
            .recommendations {{
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 5px;
                border-left: 5px solid #007bff;
            }}
            .skill-tag {{
                display: inline-block;
                background-color: #e9ecef;
                padding: 5px 10px;
                margin: 5px;
                border-radius: 15px;
                font-size: 14px;
            }}
            .experience-item, .education-item {{
                margin-bottom: 15px;
                padding-left: 10px;
                border-left: 3px solid #007bff;
            }}
            .responsibility-item {{
                margin-left: 20px;
                position: relative;
            }}
            .responsibility-item:before {{
                content: "•";
                position: absolute;
                left: -15px;
            }}
        </style>
    </head>
    <body>
        <h1>Resume Analysis: {filename}</h1>
        <p>Analyzed on: {analyzed_date}</p>
        
        <div class="section">
            <h2>Overall Score</h2>
            <p class="score">{overall_score}/10</p>
            <p>This score is based on an evaluation of your skills, experience, and education.</p>
        </div>
        
        <div class="section">
            <h2>Personal Information</h2>
            {personal_info}
        </div>
        
        {summary_section}
        
        <div class="section">
            <h2>Skills</h2>
            <div>
                {skills}
            </div>
            <p>Skill Score: <strong>{skill_score}/10</strong></p>
        </div>
        
        <div class="section">
            <h2>Experience</h2>
            {experience}
            <p>Experience Score: <strong>{experience_score}/10</strong></p>
        </div>
        
        <div class="section">
            <h2>Education</h2>
            {education}
            <p>Education Score: <strong>{education_score}/10</strong></p>
        </div>
        
        <div class="section recommendations">
            <h2>Recommendations</h2>
            <ul>
                {recommendations}
            </ul>
        </div>
        
        <footer>
            <p>Generated by Resume Analyzer</p>
        </footer>
    </body>
    </html>
    """
    
    # Determine score color
    score_color = "#dc3545"  # Red for low scores
    if resume.overall_score >= 7.0:
        score_color = "#28a745"  # Green for high scores
    elif resume.overall_score >= 5.0:
        score_color = "#ffc107"  # Yellow for medium scores
    
    # Format personal information
    personal_info = "<p>No personal information found.</p>"
    personal_info_items = []
    
    if resume.name:
        personal_info_items.append(f"<strong>Name:</strong> {resume.name}")
    if resume.email:
        personal_info_items.append(f"<strong>Email:</strong> {resume.email}")
    if resume.phone:
        personal_info_items.append(f"<strong>Phone:</strong> {resume.phone}")
    if resume.location:
        personal_info_items.append(f"<strong>Location:</strong> {resume.location}")
    if resume.linkedin:
        personal_info_items.append(f"<strong>LinkedIn:</strong> <a href='https://{resume.linkedin}'>{resume.linkedin}</a>")
    if resume.website:
        personal_info_items.append(f"<strong>Website:</strong> <a href='{resume.website}'>{resume.website}</a>")
    
    if personal_info_items:
        personal_info = "<p>" + "<br>".join(personal_info_items) + "</p>"
    
    # Format summary section
    summary_section = ""
    if resume.summary:
        summary_section = f"""
        <div class="section">
            <h2>Summary</h2>
            <p>{resume.summary}</p>
        </div>
        """
    
    # Format skills
    skills = "<p>No skills found.</p>"
    if resume.skills:
        skills_html = [f"<span class='skill-tag'>{skill}</span>" for skill in resume.skills]
        skills = "\n".join(skills_html)
    
    # Calculate skill score for display
    skill_score = sum(resume.skill_scores.values()) if resume.skill_scores else 0
    
    # Format experience
    experience = "<p>No work experience found.</p>"
    if resume.experience:
        experience_items = []
        for exp in resume.experience:
            exp_html = f"<div class='experience-item'>"
            exp_html += f"<h3>{exp['title']} at {exp['company']}</h3>"
            
            dates = []
            if exp['start_date']:
                dates.append(exp['start_date'])
            if exp['end_date']:
                dates.append(exp['end_date'])
            
            if dates:
                exp_html += f"<p>{' - '.join(dates)}</p>"
            
            if exp['location']:
                exp_html += f"<p>{exp['location']}</p>"
            
            if exp['description']:
                exp_html += f"<p>{exp['description']}</p>"
            
            if exp['responsibilities']:
                exp_html += "<ul>"
                for resp in exp['responsibilities']:
                    exp_html += f"<li class='responsibility-item'>{resp}</li>"
                exp_html += "</ul>"
            
            exp_html += "</div>"
            experience_items.append(exp_html)
        
        experience = "\n".join(experience_items)
    
    # Format education
    education = "<p>No education information found.</p>"
    if resume.education:
        education_items = []
        for edu in resume.education:
            edu_html = f"<div class='education-item'>"
            
            degree_field = edu['degree']
            if edu['field']:
                degree_field += f", {edu['field']}"
            
            edu_html += f"<h3>{edu['institution']}</h3>"
            edu_html += f"<p>{degree_field}</p>"
            
            dates = []
            if edu['start_date']:
                dates.append(edu['start_date'])
            if edu['end_date']:
                dates.append(edu['end_date'])
            
            if dates:
                edu_html += f"<p>{' - '.join(dates)}</p>"
            
            if edu['location']:
                edu_html += f"<p>{edu['location']}</p>"
            
            if edu['gpa']:
                edu_html += f"<p>GPA: {edu['gpa']}</p>"
            
            if edu['description']:
                edu_html += f"<p>{edu['description']}</p>"
            
            edu_html += "</div>"
            education_items.append(edu_html)
        
        education = "\n".join(education_items)
    
    # Format recommendations
    recommendations = "<li>No specific recommendations.</li>"
    if resume.recommendations:
        recommendations_items = [f"<li>{rec}</li>" for rec in resume.recommendations]
        recommendations = "\n".join(recommendations_items)
    
    # Fill the template
    html_content = html_template.format(
        filename=resume.filename,
        analyzed_date=resume.parsed_date.strftime('%Y-%m-%d %H:%M:%S'),
        overall_score=f"{resume.overall_score:.1f}",
        personal_info=personal_info,
        summary_section=summary_section,
        skills=skills,
        skill_score=f"{skill_score:.1f}",
        experience=experience,
        experience_score=f"{resume.experience_score:.1f}",
        education=education,
        education_score=f"{resume.education_score:.1f}",
        recommendations=recommendations,
        score_color=score_color
    )
    
    return html_content