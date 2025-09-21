#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resume Model

This module defines the Resume class which represents a parsed resume document.
It stores all extracted information and provides methods for accessing and manipulating
the resume data.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any


class Resume:
    """
    Class representing a parsed resume with all extracted information.
    """
    
    def __init__(self, raw_text: str, filename: str):
        """
        Initialize a new Resume object.
        
        Args:
            raw_text (str): The raw text content of the resume.
            filename (str): The filename of the original resume document.
        """
        self.raw_text = raw_text
        self.filename = filename
        self.parsed_date = datetime.now()
        
        # Basic information
        self.name: Optional[str] = None
        self.email: Optional[str] = None
        self.phone: Optional[str] = None
        self.location: Optional[str] = None
        self.linkedin: Optional[str] = None
        self.website: Optional[str] = None
        
        # Resume sections
        self.summary: Optional[str] = None
        self.skills: List[str] = []
        self.education: List[Dict[str, Any]] = []
        self.experience: List[Dict[str, Any]] = []
        self.projects: List[Dict[str, Any]] = []
        self.certifications: List[Dict[str, Any]] = []
        self.languages: List[Dict[str, str]] = []
        
        # Analysis results
        self.skill_scores: Dict[str, float] = {}
        self.experience_score: float = 0.0
        self.education_score: float = 0.0
        self.overall_score: float = 0.0
        self.recommendations: List[str] = []
        
    def add_skill(self, skill: str) -> None:
        """
        Add a skill to the resume.
        
        Args:
            skill (str): The skill to add.
        """
        if skill and skill not in self.skills:
            self.skills.append(skill)
    
    def add_education(self, institution: str, degree: str, field: str = None,
                     start_date: str = None, end_date: str = None, gpa: float = None,
                     location: str = None, description: str = None) -> None:
        """
        Add an education entry to the resume.
        
        Args:
            institution (str): Name of the educational institution.
            degree (str): Degree obtained or pursued.
            field (str, optional): Field of study.
            start_date (str, optional): Start date of education.
            end_date (str, optional): End date of education.
            gpa (float, optional): Grade Point Average.
            location (str, optional): Location of the institution.
            description (str, optional): Additional description or achievements.
        """
        education = {
            'institution': institution,
            'degree': degree,
            'field': field,
            'start_date': start_date,
            'end_date': end_date,
            'gpa': gpa,
            'location': location,
            'description': description
        }
        self.education.append(education)
    
    def add_experience(self, company: str, title: str, start_date: str = None,
                      end_date: str = None, location: str = None,
                      description: str = None, responsibilities: List[str] = None) -> None:
        """
        Add a work experience entry to the resume.
        
        Args:
            company (str): Name of the company.
            title (str): Job title.
            start_date (str, optional): Start date of employment.
            end_date (str, optional): End date of employment.
            location (str, optional): Location of the job.
            description (str, optional): Job description.
            responsibilities (List[str], optional): List of job responsibilities.
        """
        experience = {
            'company': company,
            'title': title,
            'start_date': start_date,
            'end_date': end_date,
            'location': location,
            'description': description,
            'responsibilities': responsibilities or []
        }
        self.experience.append(experience)
    
    def add_project(self, name: str, description: str = None, technologies: List[str] = None,
                   start_date: str = None, end_date: str = None, url: str = None) -> None:
        """
        Add a project entry to the resume.
        
        Args:
            name (str): Name of the project.
            description (str, optional): Project description.
            technologies (List[str], optional): Technologies used in the project.
            start_date (str, optional): Start date of the project.
            end_date (str, optional): End date of the project.
            url (str, optional): URL to the project.
        """
        project = {
            'name': name,
            'description': description,
            'technologies': technologies or [],
            'start_date': start_date,
            'end_date': end_date,
            'url': url
        }
        self.projects.append(project)
    
    def add_certification(self, name: str, issuer: str = None, date: str = None,
                         expiration_date: str = None, url: str = None) -> None:
        """
        Add a certification entry to the resume.
        
        Args:
            name (str): Name of the certification.
            issuer (str, optional): Organization that issued the certification.
            date (str, optional): Date when the certification was obtained.
            expiration_date (str, optional): Expiration date of the certification.
            url (str, optional): URL to verify the certification.
        """
        certification = {
            'name': name,
            'issuer': issuer,
            'date': date,
            'expiration_date': expiration_date,
            'url': url
        }
        self.certifications.append(certification)
    
    def add_language(self, language: str, proficiency: str) -> None:
        """
        Add a language proficiency entry to the resume.
        
        Args:
            language (str): The language.
            proficiency (str): Proficiency level (e.g., 'Fluent', 'Native', 'Intermediate').
        """
        self.languages.append({
            'language': language,
            'proficiency': proficiency
        })
    
    def add_recommendation(self, recommendation: str) -> None:
        """
        Add a recommendation for improving the resume.
        
        Args:
            recommendation (str): The recommendation text.
        """
        if recommendation and recommendation not in self.recommendations:
            self.recommendations.append(recommendation)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the resume to a dictionary representation.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the resume.
        """
        return {
            'filename': self.filename,
            'parsed_date': self.parsed_date.isoformat(),
            'basic_info': {
                'name': self.name,
                'email': self.email,
                'phone': self.phone,
                'location': self.location,
                'linkedin': self.linkedin,
                'website': self.website
            },
            'summary': self.summary,
            'skills': self.skills,
            'education': self.education,
            'experience': self.experience,
            'projects': self.projects,
            'certifications': self.certifications,
            'languages': self.languages,
            'analysis': {
                'skill_scores': self.skill_scores,
                'experience_score': self.experience_score,
                'education_score': self.education_score,
                'overall_score': self.overall_score,
                'recommendations': self.recommendations
            }
        }
    
    def to_text(self) -> str:
        """
        Convert the resume to a formatted text representation.
        
        Returns:
            str: Text representation of the resume.
        """
        lines = []
        
        # Basic information
        lines.append(f"Resume Analysis: {self.filename}")
        lines.append(f"Analyzed on: {self.parsed_date.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("\n")
        
        # Personal information
        lines.append("PERSONAL INFORMATION")
        lines.append("-" * 20)
        if self.name:
            lines.append(f"Name: {self.name}")
        if self.email:
            lines.append(f"Email: {self.email}")
        if self.phone:
            lines.append(f"Phone: {self.phone}")
        if self.location:
            lines.append(f"Location: {self.location}")
        if self.linkedin:
            lines.append(f"LinkedIn: {self.linkedin}")
        if self.website:
            lines.append(f"Website: {self.website}")
        lines.append("\n")
        
        # Summary
        if self.summary:
            lines.append("SUMMARY")
            lines.append("-" * 20)
            lines.append(self.summary)
            lines.append("\n")
        
        # Skills
        if self.skills:
            lines.append("SKILLS")
            lines.append("-" * 20)
            lines.append(", ".join(self.skills))
            lines.append("\n")
        
        # Education
        if self.education:
            lines.append("EDUCATION")
            lines.append("-" * 20)
            for edu in self.education:
                edu_line = f"{edu['institution']} - {edu['degree']}"
                if edu['field']:
                    edu_line += f", {edu['field']}"
                lines.append(edu_line)
                
                dates = []
                if edu['start_date']:
                    dates.append(edu['start_date'])
                if edu['end_date']:
                    dates.append(edu['end_date'])
                
                if dates:
                    lines.append(" - ".join(dates))
                
                if edu['location']:
                    lines.append(f"Location: {edu['location']}")
                
                if edu['gpa']:
                    lines.append(f"GPA: {edu['gpa']}")
                
                if edu['description']:
                    lines.append(edu['description'])
                
                lines.append("")
            lines.append("\n")
        
        # Experience
        if self.experience:
            lines.append("EXPERIENCE")
            lines.append("-" * 20)
            for exp in self.experience:
                exp_line = f"{exp['company']} - {exp['title']}"
                lines.append(exp_line)
                
                dates = []
                if exp['start_date']:
                    dates.append(exp['start_date'])
                if exp['end_date']:
                    dates.append(exp['end_date'])
                
                if dates:
                    lines.append(" - ".join(dates))
                
                if exp['location']:
                    lines.append(f"Location: {exp['location']}")
                
                if exp['description']:
                    lines.append(exp['description'])
                
                if exp['responsibilities']:
                    lines.append("Responsibilities:")
                    for resp in exp['responsibilities']:
                        lines.append(f"- {resp}")
                
                lines.append("")
            lines.append("\n")
        
        # Projects
        if self.projects:
            lines.append("PROJECTS")
            lines.append("-" * 20)
            for proj in self.projects:
                lines.append(f"{proj['name']}")
                
                dates = []
                if proj['start_date']:
                    dates.append(proj['start_date'])
                if proj['end_date']:
                    dates.append(proj['end_date'])
                
                if dates:
                    lines.append(" - ".join(dates))
                
                if proj['description']:
                    lines.append(proj['description'])
                
                if proj['technologies']:
                    lines.append(f"Technologies: {', '.join(proj['technologies'])}")
                
                if proj['url']:
                    lines.append(f"URL: {proj['url']}")
                
                lines.append("")
            lines.append("\n")
        
        # Analysis
        lines.append("ANALYSIS")
        lines.append("-" * 20)
        lines.append(f"Overall Score: {self.overall_score:.2f}/10.0")
        
        if self.skill_scores:
            lines.append("\nSkill Scores:")
            for skill, score in self.skill_scores.items():
                lines.append(f"- {skill}: {score:.2f}/10.0")
        
        lines.append(f"\nExperience Score: {self.experience_score:.2f}/10.0")
        lines.append(f"Education Score: {self.education_score:.2f}/10.0")
        
        if self.recommendations:
            lines.append("\nRecommendations:")
            for i, rec in enumerate(self.recommendations, 1):
                lines.append(f"{i}. {rec}")
        
        return "\n".join(lines)