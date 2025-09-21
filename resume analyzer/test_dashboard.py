#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for the Resume Analyzer Dashboard
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from resume_analyzer.parsers import parser_factory
from resume_analyzer.analyzers import content_analyzer, skills_analyzer, experience_analyzer
from resume_analyzer.analyzers.ats_analyzer import ATSAnalyzer
from resume_analyzer.analyzers.scoring import score_resume, generate_recommendations
from resume_analyzer.models.resume import Resume


def test_ats_analyzer():
    """Test the ATS analyzer with the sample resume."""
    print("Testing ATS Analyzer...")
    
    # Parse the sample resume
    sample_file = "data/sample_resume.txt"
    parser = parser_factory.get_parser(sample_file)
    resume_text = parser.parse(sample_file)
    
    # Create Resume object
    resume = Resume(resume_text, "sample_resume.txt")
    
    # Run analysis
    content_analyzer.analyze(resume)
    skills_analyzer.analyze(resume)
    experience_analyzer.analyze(resume)
    
    # Calculate scores
    overall_score = score_resume(resume)
    recommendations = generate_recommendations(resume)
    
    # ATS Analysis
    ats_analyzer = ATSAnalyzer()
    ats_analysis = ats_analyzer.analyze(resume)
    
    print(f"Overall Score: {overall_score:.2f}/10.0")
    print(f"ATS Score: {ats_analysis['ats_score']:.2f}/10.0")
    print(f"Number of Recommendations: {len(recommendations)}")
    print(f"Number of ATS Recommendations: {len(ats_analysis['recommendations'])}")
    print(f"Red Flags: {len(ats_analysis['red_flags'])}")
    print(f"Missing Elements: {len(ats_analysis['missing_elements'])}")
    
    print("\nDetailed ATS Scores:")
    for component, score in ats_analysis['detailed_scores'].items():
        print(f"  {component}: {score:.2f}/10.0")
    
    print("\nTop 5 Technical Keywords Found:")
    if ats_analysis['keyword_density'].get('technical_keywords'):
        for keyword in ats_analysis['keyword_density']['technical_keywords'][:5]:
            print(f"  {keyword['keyword']}: {keyword['count']} times ({keyword['density']:.2f}%)")
    
    print("\nSample Recommendations:")
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"  {i}. {rec}")
    
    print("\nSample ATS Recommendations:")
    for i, rec in enumerate(ats_analysis['recommendations'][:3], 1):
        print(f"  {i}. {rec}")
    
    print("\n✅ ATS Analyzer test completed successfully!")


if __name__ == "__main__":
    test_ats_analyzer()
