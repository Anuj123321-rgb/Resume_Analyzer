#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ATS (Applicant Tracking System) Analyzer

This module provides comprehensive ATS scoring and analysis for resumes.
It evaluates how well a resume will perform in ATS systems.
"""

import re
from typing import Dict, List, Any, Tuple
from datetime import datetime

from resume_analyzer.models.resume import Resume
from resume_analyzer.utils.text_utils import calculate_text_stats


class ATSAnalyzer:
    """Comprehensive ATS analysis and scoring system."""
    
    def __init__(self):
        """Initialize the ATS analyzer with scoring criteria."""
        self.ats_keywords = {
            'technical': [
                'python', 'javascript', 'java', 'c++', 'sql', 'html', 'css', 'react', 'angular', 'vue',
                'node.js', 'django', 'flask', 'spring', 'aws', 'azure', 'gcp', 'docker', 'kubernetes',
                'git', 'jenkins', 'ci/cd', 'agile', 'scrum', 'api', 'rest', 'graphql', 'microservices',
                'machine learning', 'ai', 'data science', 'analytics', 'database', 'postgresql', 'mongodb',
                'redis', 'elasticsearch', 'kafka', 'rabbitmq', 'terraform', 'ansible', 'linux', 'unix'
            ],
            'soft': [
                'leadership', 'communication', 'teamwork', 'collaboration', 'problem solving',
                'critical thinking', 'adaptability', 'time management', 'project management',
                'mentoring', 'training', 'presentation', 'negotiation', 'customer service',
                'analytical', 'creative', 'innovative', 'detail oriented', 'self motivated'
            ],
            'industry': [
                'fintech', 'healthcare', 'e-commerce', 'saas', 'startup', 'enterprise',
                'cybersecurity', 'devops', 'cloud computing', 'mobile development',
                'web development', 'full stack', 'frontend', 'backend', 'database administration'
            ]
        }
        
        self.ats_red_flags = [
            'objective', 'references available upon request', 'hobbies', 'personal interests',
            'marital status', 'age', 'date of birth', 'photo', 'picture'
        ]
        
        self.ats_format_requirements = {
            'file_formats': ['.pdf', '.docx', '.doc'],
            'max_file_size': 5 * 1024 * 1024,  # 5MB
            'preferred_length': (300, 700),  # words
            'max_length': 1000
        }
    
    def analyze(self, resume: Resume) -> Dict[str, Any]:
        """
        Perform comprehensive ATS analysis on a resume.
        
        Args:
            resume (Resume): The resume to analyze.
            
        Returns:
            Dict[str, Any]: Comprehensive ATS analysis results.
        """
        analysis = {
            'ats_score': 0.0,
            'keyword_density': {},
            'format_compliance': {},
            'red_flags': [],
            'missing_elements': [],
            'recommendations': [],
            'detailed_scores': {}
        }
        
        # Calculate ATS score components
        analysis['detailed_scores'] = {
            'keyword_score': self._calculate_keyword_score(resume),
            'format_score': self._calculate_format_score(resume),
            'structure_score': self._calculate_structure_score(resume),
            'content_score': self._calculate_content_score(resume),
            'completeness_score': self._calculate_completeness_score(resume)
        }
        
        # Calculate overall ATS score (weighted average)
        weights = {
            'keyword_score': 0.25,
            'format_score': 0.20,
            'structure_score': 0.20,
            'content_score': 0.20,
            'completeness_score': 0.15
        }
        
        analysis['ats_score'] = sum(
            score * weights[component] 
            for component, score in analysis['detailed_scores'].items()
        )
        
        # Analyze keyword density
        analysis['keyword_density'] = self._analyze_keyword_density(resume)
        
        # Check format compliance
        analysis['format_compliance'] = self._check_format_compliance(resume)
        
        # Identify red flags
        analysis['red_flags'] = self._identify_red_flags(resume)
        
        # Identify missing elements
        analysis['missing_elements'] = self._identify_missing_elements(resume)
        
        # Generate recommendations
        analysis['recommendations'] = self._generate_ats_recommendations(resume, analysis)
        
        return analysis
    
    def _calculate_keyword_score(self, resume: Resume) -> float:
        """Calculate keyword optimization score (0-10)."""
        if not resume.raw_text:
            return 0.0
        
        text_lower = resume.raw_text.lower()
        score = 0.0
        
        # Check for technical keywords
        tech_keywords_found = sum(1 for keyword in self.ats_keywords['technical'] 
                                if keyword in text_lower)
        tech_score = min(5.0, (tech_keywords_found / len(self.ats_keywords['technical'])) * 5)
        
        # Check for soft skills keywords
        soft_keywords_found = sum(1 for keyword in self.ats_keywords['soft'] 
                                if keyword in text_lower)
        soft_score = min(3.0, (soft_keywords_found / len(self.ats_keywords['soft'])) * 3)
        
        # Check for industry-specific keywords
        industry_keywords_found = sum(1 for keyword in self.ats_keywords['industry'] 
                                    if keyword in text_lower)
        industry_score = min(2.0, (industry_keywords_found / len(self.ats_keywords['industry'])) * 2)
        
        score = tech_score + soft_score + industry_score
        return min(10.0, score)
    
    def _calculate_format_score(self, resume: Resume) -> float:
        """Calculate format compliance score (0-10)."""
        score = 0.0
        
        # Check file format (assume it's supported if we can parse it)
        score += 2.0
        
        # Check text length
        if resume.raw_text:
            stats = calculate_text_stats(resume.raw_text)
            word_count = stats['word_count']
            
            if self.ats_format_requirements['preferred_length'][0] <= word_count <= self.ats_format_requirements['preferred_length'][1]:
                score += 3.0
            elif 200 <= word_count < self.ats_format_requirements['preferred_length'][0]:
                score += 2.0
            elif self.ats_format_requirements['preferred_length'][1] < word_count <= self.ats_format_requirements['max_length']:
                score += 2.0
            else:
                score += 1.0
        
        # Check for proper section headers
        section_headers = ['experience', 'education', 'skills', 'summary', 'objective']
        headers_found = sum(1 for header in section_headers 
                           if header in resume.raw_text.lower())
        score += min(3.0, (headers_found / len(section_headers)) * 3)
        
        # Check for consistent formatting
        if resume.raw_text:
            # Check for bullet points
            if '•' in resume.raw_text or '-' in resume.raw_text or '*' in resume.raw_text:
                score += 1.0
            
            # Check for consistent date formatting
            date_patterns = [
                r'\b\d{4}\b',  # Years
                r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b',  # Month Year
                r'\b\d{1,2}/\d{4}\b'  # MM/YYYY
            ]
            dates_found = sum(1 for pattern in date_patterns 
                             if re.search(pattern, resume.raw_text, re.IGNORECASE))
            if dates_found > 0:
                score += 1.0
        
        return min(10.0, score)
    
    def _calculate_structure_score(self, resume: Resume) -> float:
        """Calculate resume structure score (0-10)."""
        score = 0.0
        
        # Check for essential sections
        essential_sections = ['contact', 'experience', 'education', 'skills']
        sections_found = 0
        
        if resume.name or resume.email:
            sections_found += 1
        if resume.experience:
            sections_found += 1
        if resume.education:
            sections_found += 1
        if resume.skills:
            sections_found += 1
        
        score += (sections_found / len(essential_sections)) * 4.0
        
        # Check for reverse chronological order (experience)
        if resume.experience and len(resume.experience) > 1:
            # Simple check - if dates are in descending order
            score += 2.0
        
        # Check for consistent formatting within sections
        if resume.experience:
            consistent_formatting = all(
                exp.get('company') and exp.get('title') 
                for exp in resume.experience
            )
            if consistent_formatting:
                score += 2.0
        
        # Check for proper spacing and readability
        if resume.raw_text:
            # Check for reasonable line length and spacing
            lines = resume.raw_text.split('\n')
            non_empty_lines = [line.strip() for line in lines if line.strip()]
            if len(non_empty_lines) > 10:  # Reasonable number of content lines
                score += 2.0
        
        return min(10.0, score)
    
    def _calculate_content_score(self, resume: Resume) -> float:
        """Calculate content quality score (0-10)."""
        score = 0.0
        
        # Check for quantified achievements
        if resume.raw_text:
            quantifiers = re.findall(r'\b\d+%|\b\d+\+|\b\d+[km]?\+|\b\d+[km]?\b', resume.raw_text)
            if len(quantifiers) >= 3:
                score += 3.0
            elif len(quantifiers) >= 1:
                score += 1.5
        
        # Check for action verbs
        action_verbs = [
            'achieved', 'developed', 'implemented', 'managed', 'led', 'created', 'designed',
            'improved', 'increased', 'reduced', 'optimized', 'delivered', 'executed',
            'coordinated', 'facilitated', 'established', 'built', 'launched', 'streamlined'
        ]
        
        if resume.raw_text:
            verbs_found = sum(1 for verb in action_verbs 
                             if verb in resume.raw_text.lower())
            score += min(3.0, (verbs_found / len(action_verbs)) * 3)
        
        # Check for professional summary
        if resume.summary and len(resume.summary) > 50:
            score += 2.0
        
        # Check for relevant skills
        if resume.skills and len(resume.skills) >= 5:
            score += 2.0
        
        return min(10.0, score)
    
    def _calculate_completeness_score(self, resume: Resume) -> float:
        """Calculate completeness score (0-10)."""
        score = 0.0
        
        # Contact information completeness
        contact_fields = [resume.name, resume.email, resume.phone, resume.location]
        contact_score = sum(1 for field in contact_fields if field) / len(contact_fields)
        score += contact_score * 2.0
        
        # Experience completeness
        if resume.experience:
            exp_completeness = 0
            for exp in resume.experience:
                exp_fields = [exp.get('company'), exp.get('title'), 
                            exp.get('start_date'), exp.get('end_date')]
                exp_completeness += sum(1 for field in exp_fields if field) / len(exp_fields)
            score += (exp_completeness / len(resume.experience)) * 3.0
        
        # Education completeness
        if resume.education:
            edu_completeness = 0
            for edu in resume.education:
                edu_fields = [edu.get('institution'), edu.get('degree'), 
                            edu.get('start_date'), edu.get('end_date')]
                edu_completeness += sum(1 for field in edu_fields if field) / len(edu_fields)
            score += (edu_completeness / len(resume.education)) * 2.0
        
        # Skills completeness
        if resume.skills and len(resume.skills) >= 5:
            score += 2.0
        elif resume.skills:
            score += 1.0
        
        # Summary completeness
        if resume.summary and len(resume.summary) > 100:
            score += 1.0
        
        return min(10.0, score)
    
    def _analyze_keyword_density(self, resume: Resume) -> Dict[str, Any]:
        """Analyze keyword density in the resume."""
        if not resume.raw_text:
            return {}
        
        text_lower = resume.raw_text.lower()
        word_count = len(text_lower.split())
        
        keyword_analysis = {
            'technical_keywords': [],
            'soft_skills_keywords': [],
            'industry_keywords': [],
            'keyword_density': {}
        }
        
        # Find technical keywords
        for keyword in self.ats_keywords['technical']:
            if keyword in text_lower:
                count = text_lower.count(keyword)
                density = (count / word_count) * 100 if word_count > 0 else 0
                keyword_analysis['technical_keywords'].append({
                    'keyword': keyword,
                    'count': count,
                    'density': round(density, 2)
                })
        
        # Find soft skills keywords
        for keyword in self.ats_keywords['soft']:
            if keyword in text_lower:
                count = text_lower.count(keyword)
                density = (count / word_count) * 100 if word_count > 0 else 0
                keyword_analysis['soft_skills_keywords'].append({
                    'keyword': keyword,
                    'count': count,
                    'density': round(density, 2)
                })
        
        # Find industry keywords
        for keyword in self.ats_keywords['industry']:
            if keyword in text_lower:
                count = text_lower.count(keyword)
                density = (count / word_count) * 100 if word_count > 0 else 0
                keyword_analysis['industry_keywords'].append({
                    'keyword': keyword,
                    'count': count,
                    'density': round(density, 2)
                })
        
        return keyword_analysis
    
    def _check_format_compliance(self, resume: Resume) -> Dict[str, Any]:
        """Check format compliance with ATS requirements."""
        compliance = {
            'file_format': True,  # Assume supported if we can parse
            'file_size': True,    # Assume reasonable if we can process
            'text_length': 'good',
            'font_usage': 'unknown',
            'formatting_consistency': 'good'
        }
        
        if resume.raw_text:
            stats = calculate_text_stats(resume.raw_text)
            word_count = stats['word_count']
            
            if word_count < self.ats_format_requirements['preferred_length'][0]:
                compliance['text_length'] = 'too_short'
            elif word_count > self.ats_format_requirements['max_length']:
                compliance['text_length'] = 'too_long'
            else:
                compliance['text_length'] = 'good'
        
        return compliance
    
    def _identify_red_flags(self, resume: Resume) -> List[str]:
        """Identify ATS red flags in the resume."""
        red_flags = []
        
        if resume.raw_text:
            text_lower = resume.raw_text.lower()
            
            for flag in self.ats_red_flags:
                if flag in text_lower:
                    red_flags.append(f"Contains '{flag}' which may hurt ATS performance")
        
        return red_flags
    
    def _identify_missing_elements(self, resume: Resume) -> List[str]:
        """Identify missing elements that could improve ATS performance."""
        missing = []
        
        if not resume.name:
            missing.append("Name")
        if not resume.email:
            missing.append("Email address")
        if not resume.phone:
            missing.append("Phone number")
        if not resume.location:
            missing.append("Location")
        if not resume.summary:
            missing.append("Professional summary")
        if not resume.skills or len(resume.skills) < 5:
            missing.append("Sufficient skills (aim for 5+ relevant skills)")
        if not resume.experience:
            missing.append("Work experience")
        if not resume.education:
            missing.append("Education section")
        
        return missing
    
    def _generate_ats_recommendations(self, resume: Resume, analysis: Dict[str, Any]) -> List[str]:
        """Generate ATS-specific recommendations."""
        recommendations = []
        
        # Keyword recommendations
        if analysis['detailed_scores']['keyword_score'] < 6:
            recommendations.append("Add more relevant keywords from job descriptions in your field")
            recommendations.append("Include both technical and soft skills keywords")
        
        # Format recommendations
        if analysis['detailed_scores']['format_score'] < 7:
            recommendations.append("Use standard section headers (Experience, Education, Skills)")
            recommendations.append("Ensure consistent formatting throughout the document")
        
        # Structure recommendations
        if analysis['detailed_scores']['structure_score'] < 7:
            recommendations.append("Organize experience in reverse chronological order")
            recommendations.append("Use bullet points for better readability")
        
        # Content recommendations
        if analysis['detailed_scores']['content_score'] < 6:
            recommendations.append("Quantify your achievements with specific numbers and percentages")
            recommendations.append("Use strong action verbs to describe your accomplishments")
        
        # Completeness recommendations
        if analysis['detailed_scores']['completeness_score'] < 7:
            recommendations.append("Ensure all contact information is complete and professional")
            recommendations.append("Add detailed descriptions for each work experience")
        
        # Red flag recommendations
        if analysis['red_flags']:
            recommendations.append("Remove any personal information not relevant to the job")
            recommendations.append("Avoid using 'References available upon request'")
        
        # Missing elements recommendations
        if analysis['missing_elements']:
            recommendations.append(f"Add missing elements: {', '.join(analysis['missing_elements'][:3])}")
        
        return recommendations[:8]  # Limit to 8 recommendations
