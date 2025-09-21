#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Skills Analyzer Module

This module provides functionality for analyzing and extracting skills from resumes.
"""

import re
import os
import json
from typing import List, Dict, Set, Optional
from pathlib import Path

from resume_analyzer.models.resume import Resume


# Default skills data
DEFAULT_SKILLS = {
    "programming_languages": [
        "Python", "Java", "JavaScript", "C++", "C#", "Ruby", "PHP", "Swift", 
        "Kotlin", "Go", "Rust", "TypeScript", "Scala", "Perl", "R", "MATLAB",
        "Bash", "PowerShell", "SQL", "HTML", "CSS", "C", "Objective-C", "Dart",
        "Groovy", "VBA", "Lua", "Haskell", "Clojure", "F#", "COBOL", "Fortran"
    ],
    "frameworks_libraries": [
        "React", "Angular", "Vue.js", "Django", "Flask", "Spring", "ASP.NET",
        "Express.js", "Node.js", "jQuery", "Bootstrap", "TensorFlow", "PyTorch",
        "Keras", "Pandas", "NumPy", "Scikit-learn", "Laravel", "Ruby on Rails",
        "Symfony", "Flutter", "React Native", "Xamarin", "Unity", "Unreal Engine",
        "Next.js", "Gatsby", "Redux", "Vuex", "MobX", "RxJS", "D3.js", "Three.js"
    ],
    "databases": [
        "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Oracle", "SQL Server",
        "Redis", "Cassandra", "Elasticsearch", "DynamoDB", "Firebase", "Neo4j",
        "MariaDB", "CouchDB", "Firestore", "Realm", "InfluxDB", "Couchbase"
    ],
    "cloud_platforms": [
        "AWS", "Azure", "Google Cloud", "Heroku", "DigitalOcean", "Linode",
        "IBM Cloud", "Oracle Cloud", "Alibaba Cloud", "Salesforce", "Netlify",
        "Vercel", "Firebase", "AWS Lambda", "EC2", "S3", "RDS", "DynamoDB",
        "CloudFront", "Route 53", "IAM", "Azure Functions", "App Service",
        "Google App Engine", "Google Kubernetes Engine", "Cloud Functions"
    ],
    "devops_tools": [
        "Docker", "Kubernetes", "Jenkins", "GitLab CI", "GitHub Actions",
        "Travis CI", "CircleCI", "Ansible", "Terraform", "Puppet", "Chef",
        "Vagrant", "Prometheus", "Grafana", "ELK Stack", "Nagios", "Zabbix",
        "New Relic", "Datadog", "Splunk", "Sentry", "Airflow", "Argo CD"
    ],
    "version_control": [
        "Git", "SVN", "Mercurial", "GitHub", "GitLab", "Bitbucket", "Azure DevOps"
    ],
    "methodologies": [
        "Agile", "Scrum", "Kanban", "Waterfall", "Lean", "XP", "TDD", "BDD",
        "DevOps", "CI/CD", "Microservices", "Serverless", "Domain-Driven Design"
    ],
    "soft_skills": [
        "Communication", "Teamwork", "Problem Solving", "Critical Thinking",
        "Time Management", "Leadership", "Adaptability", "Creativity", "Collaboration",
        "Emotional Intelligence", "Conflict Resolution", "Decision Making",
        "Negotiation", "Presentation", "Public Speaking", "Mentoring", "Coaching"
    ],
    "data_science": [
        "Machine Learning", "Deep Learning", "Natural Language Processing",
        "Computer Vision", "Data Mining", "Data Analysis", "Data Visualization",
        "Statistical Analysis", "A/B Testing", "Regression", "Classification",
        "Clustering", "Dimensionality Reduction", "Feature Engineering",
        "Reinforcement Learning", "Time Series Analysis", "Bayesian Methods"
    ],
    "design": [
        "UI/UX", "Photoshop", "Illustrator", "Sketch", "Figma", "InDesign",
        "After Effects", "Premiere Pro", "Blender", "3D Modeling", "Animation",
        "Wireframing", "Prototyping", "User Research", "Usability Testing",
        "Responsive Design", "Graphic Design", "Typography", "Color Theory"
    ],
    "project_management": [
        "JIRA", "Trello", "Asana", "Monday.com", "ClickUp", "Basecamp",
        "Microsoft Project", "Smartsheet", "Notion", "Confluence", "Slack",
        "Microsoft Teams", "Zoom", "Google Meet", "Risk Management",
        "Budgeting", "Resource Allocation", "Stakeholder Management"
    ],
    "mobile_development": [
        "iOS", "Android", "Swift", "Kotlin", "Objective-C", "Java",
        "React Native", "Flutter", "Xamarin", "Ionic", "Cordova", "PhoneGap",
        "SwiftUI", "Jetpack Compose", "ARKit", "ARCore", "Core ML", "TensorFlow Lite"
    ],
    "testing": [
        "Unit Testing", "Integration Testing", "Functional Testing", "End-to-End Testing",
        "Regression Testing", "Performance Testing", "Load Testing", "Stress Testing",
        "Security Testing", "Penetration Testing", "JUnit", "pytest", "Mocha", "Jest",
        "Selenium", "Cypress", "Appium", "TestNG", "Jasmine", "Karma", "Postman"
    ],
    "security": [
        "Cybersecurity", "Network Security", "Application Security", "Cloud Security",
        "Encryption", "Authentication", "Authorization", "OAuth", "JWT", "SAML",
        "SSO", "Firewall", "VPN", "Intrusion Detection", "Penetration Testing",
        "Vulnerability Assessment", "Security Auditing", "Compliance", "GDPR", "HIPAA"
    ]
}


def analyze(resume: Resume) -> None:
    """
    Analyze the resume and extract skills.
    
    Args:
        resume (Resume): The resume object to analyze.
    """
    # Load skills data
    skills_data = _load_skills_data()
    
    # Extract skills from the resume text
    extract_skills(resume, skills_data)
    
    # Score the skills
    score_skills(resume)


def _load_skills_data() -> Dict[str, List[str]]:
    """
    Load skills data from a JSON file or use the default skills data.
    
    Returns:
        Dict[str, List[str]]: Dictionary of skill categories and their skills.
    """
    # Try to load skills data from a file
    skills_file = Path(__file__).parent / 'data' / 'skills.json'
    
    if os.path.exists(skills_file):
        try:
            with open(skills_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    
    # If file doesn't exist or couldn't be loaded, use the default skills data
    return DEFAULT_SKILLS


def extract_skills(resume: Resume, skills_data: Dict[str, List[str]]) -> None:
    """
    Extract skills from the resume text based on the skills data.
    
    Args:
        resume (Resume): The resume object to update with skills.
        skills_data (Dict[str, List[str]]): Dictionary of skill categories and their skills.
    """
    text = resume.raw_text.lower()
    
    # Create a set to store found skills
    found_skills: Set[str] = set()
    
    # Extract skills from each category
    for category, skills in skills_data.items():
        for skill in skills:
            # Create a regex pattern to match the skill
            # This pattern matches the skill as a whole word, ignoring case
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            
            # Search for the skill in the resume text
            if re.search(pattern, text):
                found_skills.add(skill)
    
    # Extract skills from the "Skills" section if it exists
    skills_section = _extract_skills_section(resume.raw_text)
    if skills_section:
        # Split the skills section by common delimiters
        for delimiter in [',', '•', '·', '\n', ';']:
            if delimiter in skills_section:
                skills_list = [s.strip() for s in skills_section.split(delimiter) if s.strip()]
                for skill in skills_list:
                    # Only add skills that are not too long (likely not a skill if too long)
                    if 2 <= len(skill) <= 50:
                        found_skills.add(skill)
                break
    
    # Update the resume with the found skills
    resume.skills = sorted(list(found_skills))


def _extract_skills_section(text: str) -> Optional[str]:
    """
    Extract the skills section from the resume text.
    
    Args:
        text (str): The resume text.
        
    Returns:
        Optional[str]: The skills section text if found, None otherwise.
    """
    # Look for common skills section headers
    skills_headers = [
        'skills', 'technical skills', 'core skills', 'key skills',
        'professional skills', 'competencies', 'areas of expertise'
    ]
    
    # Split the text into lines
    lines = text.split('\n')
    
    # Find the skills section
    skills_start = -1
    skills_end = -1
    
    for i, line in enumerate(lines):
        line_lower = line.lower().strip()
        
        # Check if this line is a skills header
        if any(header == line_lower or header in line_lower for header in skills_headers):
            skills_start = i + 1
            continue
        
        # If we found the start of the skills section, look for the end
        if skills_start != -1 and skills_end == -1:
            # Check if this line is the start of another section
            if line and line[0].isupper() and line[-1] == ':' or \
               line.lower().strip() in ['experience', 'education', 'work experience',
                                       'employment', 'projects', 'certifications']:
                skills_end = i
                break
    
    # If we found a skills section, extract it
    if skills_start != -1:
        if skills_end == -1:  # If we didn't find the end, use a reasonable number of lines
            skills_end = min(skills_start + 10, len(lines))
        
        skills_lines = lines[skills_start:skills_end]
        skills_text = ' '.join([line.strip() for line in skills_lines if line.strip()])
        
        # Clean up the skills text
        skills_text = re.sub(r'\s+', ' ', skills_text).strip()
        
        return skills_text
    
    return None


def score_skills(resume: Resume) -> None:
    """
    Score the skills found in the resume.
    
    Args:
        resume (Resume): The resume object to update with skill scores.
    """
    # Define skill categories and their weights
    skill_categories = {
        'technical': {
            'weight': 0.6,
            'keywords': ['programming', 'language', 'framework', 'library', 'database',
                        'cloud', 'devops', 'version control', 'testing', 'security']
        },
        'soft': {
            'weight': 0.2,
            'keywords': ['communication', 'teamwork', 'problem solving', 'critical thinking',
                        'time management', 'leadership', 'adaptability', 'creativity']
        },
        'domain': {
            'weight': 0.2,
            'keywords': ['industry', 'domain', 'sector', 'field', 'business', 'finance',
                        'healthcare', 'education', 'retail', 'manufacturing', 'technology']
        }
    }
    
    # Calculate scores for each skill category
    category_scores = {}
    for category, info in skill_categories.items():
        category_score = 0.0
        for skill in resume.skills:
            skill_lower = skill.lower()
            if any(keyword in skill_lower for keyword in info['keywords']):
                category_score += 1.0
        
        # Normalize the score (0-10)
        max_skills = 10  # Assuming 10 skills per category is a good benchmark
        normalized_score = min(10.0, (category_score / max_skills) * 10.0)
        category_scores[category] = normalized_score * info['weight']
    
    # Calculate the overall skill score
    overall_skill_score = sum(category_scores.values())
    
    # Update the resume with the skill scores
    resume.skill_scores = category_scores
    
    # Add recommendations based on skill analysis
    if overall_skill_score < 3.0:
        resume.add_recommendation("Consider adding more specific skills to your resume, especially technical skills.")
    elif overall_skill_score < 6.0:
        resume.add_recommendation("Your skills section is good, but could be improved by adding more specialized skills relevant to your target role.")
    
    # Check for balance between technical and soft skills
    if 'technical' in category_scores and 'soft' in category_scores:
        if category_scores['technical'] > 3 * category_scores['soft']:
            resume.add_recommendation("Consider adding more soft skills to balance your technical expertise.")
        elif category_scores['soft'] > 3 * category_scores['technical']:
            resume.add_recommendation("Consider adding more technical skills to complement your soft skills.")