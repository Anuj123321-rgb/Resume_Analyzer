#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resume Analyzer Dashboard

A comprehensive Streamlit dashboard for resume analysis with ATS scoring,
visualizations, and improvement recommendations.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import sys
from pathlib import Path
import tempfile
from datetime import datetime
import json

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from resume_analyzer.parsers import parser_factory
from resume_analyzer.analyzers import content_analyzer, skills_analyzer, experience_analyzer
from resume_analyzer.analyzers.ats_analyzer import ATSAnalyzer
from resume_analyzer.analyzers.scoring import score_resume, generate_recommendations
from resume_analyzer.models.resume import Resume
from resume_analyzer.utils import file_utils, text_utils


# Page configuration
st.set_page_config(
    page_title="Resume Analyzer Dashboard",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .score-excellent { color: #28a745; font-weight: bold; }
    .score-good { color: #17a2b8; font-weight: bold; }
    .score-fair { color: #ffc107; font-weight: bold; }
    .score-poor { color: #dc3545; font-weight: bold; }
    .recommendation-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 4px solid #2196f3;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        color: #1565c0;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(33, 150, 243, 0.1);
        border: 1px solid #90caf9;
    }
    .red-flag-box {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border-left: 4px solid #f44336;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        color: #c62828;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(244, 67, 54, 0.1);
        border: 1px solid #ef9a9a;
    }
    .info-box {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        border-left: 4px solid #4caf50;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        color: #2e7d32;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(76, 175, 80, 0.1);
        border: 1px solid #a5d6a7;
    }
    .warning-box {
        background: linear-gradient(135deg, #fff3e0 0%, #ffcc02 100%);
        border-left: 4px solid #ff9800;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        color: #e65100;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(255, 152, 0, 0.1);
        border: 1px solid #ffb74d;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main dashboard function."""
    # Header
    st.markdown('<h1 class="main-header">📄 Resume Analyzer Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Upload Resume")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a resume file",
            type=['pdf', 'docx', 'doc', 'txt', 'rtf'],
            help="Supported formats: PDF, DOCX, DOC, TXT, RTF"
        )
        
        st.markdown("---")
        st.header("⚙️ Analysis Options")
        
        # Analysis options
        include_ats = st.checkbox("Include ATS Analysis", value=True, help="Comprehensive ATS scoring and recommendations")
        include_keywords = st.checkbox("Keyword Analysis", value=True, help="Analyze keyword density and relevance")
        include_visualizations = st.checkbox("Generate Visualizations", value=True, help="Create charts and graphs")
        
        st.markdown("---")
        st.header("ℹ️ About")
        st.info("""
        This dashboard provides comprehensive resume analysis including:
        - ATS compatibility scoring
        - Keyword optimization
        - Skills analysis
        - Experience evaluation
        - Improvement recommendations
        """)
    
    # Main content area
    if uploaded_file is not None:
        # Process the uploaded file
        with st.spinner("Analyzing resume..."):
            resume_data = process_resume(uploaded_file, include_ats, include_keywords)
        
        if resume_data:
            display_analysis_results(resume_data, include_visualizations)
        else:
            st.error("Failed to process the resume. Please try again with a different file.")
    else:
        display_welcome_screen()


def process_resume(uploaded_file, include_ats=True, include_keywords=True):
    """Process the uploaded resume file."""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Get the appropriate parser
        parser = parser_factory.get_parser(tmp_file_path)
        
        # Parse the resume
        resume_text = parser.parse(tmp_file_path)
        
        # Create Resume object
        resume = Resume(resume_text, uploaded_file.name)
        
        # Run analysis
        content_analyzer.analyze(resume)
        skills_analyzer.analyze(resume)
        experience_analyzer.analyze(resume)
        
        # Calculate scores
        overall_score = score_resume(resume)
        recommendations = generate_recommendations(resume)
        
        # ATS Analysis
        ats_analysis = None
        if include_ats:
            ats_analyzer = ATSAnalyzer()
            ats_analysis = ats_analyzer.analyze(resume)
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        return {
            'resume': resume,
            'overall_score': overall_score,
            'recommendations': recommendations,
            'ats_analysis': ats_analysis
        }
        
    except Exception as e:
        st.error(f"Error processing resume: {str(e)}")
        return None


def display_analysis_results(data, include_visualizations=True):
    """Display the analysis results in the dashboard."""
    resume = data['resume']
    overall_score = data['overall_score']
    recommendations = data['recommendations']
    ats_analysis = data['ats_analysis']
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", "🎯 ATS Analysis", "📝 Content Analysis", 
        "💡 Recommendations", "📈 Detailed Metrics"
    ])
    
    with tab1:
        display_overview(resume, overall_score, ats_analysis)
    
    with tab2:
        if ats_analysis:
            display_ats_analysis(ats_analysis)
        else:
            st.info("ATS analysis was not performed. Enable it in the sidebar to see ATS-specific insights.")
    
    with tab3:
        display_content_analysis(resume)
    
    with tab4:
        display_recommendations(recommendations, ats_analysis)
    
    with tab5:
        display_detailed_metrics(resume, ats_analysis, include_visualizations)


def display_overview(resume, overall_score, ats_analysis):
    """Display the overview section."""
    st.header("📊 Resume Overview")
    
    # Basic information
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("👤 Personal Information")
        if resume.name:
            st.write(f"**Name:** {resume.name}")
        if resume.email:
            st.write(f"**Email:** {resume.email}")
        if resume.phone:
            st.write(f"**Phone:** {resume.phone}")
        if resume.location:
            st.write(f"**Location:** {resume.location}")
    
    with col2:
        st.subheader("📈 Overall Scores")
        
        # Overall score with color coding
        score_class = get_score_class(overall_score)
        st.markdown(f"**Overall Score:** <span class='{score_class}'>{overall_score:.1f}/10.0</span>", 
                   unsafe_allow_html=True)
        
        if ats_analysis:
            ats_score = ats_analysis['ats_score']
            ats_class = get_score_class(ats_score)
            st.markdown(f"**ATS Score:** <span class='{ats_class}'>{ats_score:.1f}/10.0</span>", 
                       unsafe_allow_html=True)
        
        # Component scores
        st.write(f"**Skills Score:** {resume.skill_score:.1f}/10.0")
        st.write(f"**Experience Score:** {resume.experience_score:.1f}/10.0")
        st.write(f"**Education Score:** {resume.education_score:.1f}/10.0")
    
    with col3:
        st.subheader("📋 Quick Stats")
        st.write(f"**Skills Count:** {len(resume.skills)}")
        st.write(f"**Experience Entries:** {len(resume.experience)}")
        st.write(f"**Education Entries:** {len(resume.education)}")
        
        if resume.raw_text:
            stats = text_utils.calculate_text_stats(resume.raw_text)
            st.write(f"**Word Count:** {stats.get('word_count', 0)}")
            st.write(f"**Character Count:** {stats.get('char_count', 0)}")


def display_ats_analysis(ats_analysis):
    """Display ATS analysis results."""
    st.header("🎯 ATS Analysis")
    
    # ATS Score
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ats_score = ats_analysis['ats_score']
        score_class = get_score_class(ats_score)
        st.metric(
            "ATS Compatibility Score",
            f"{ats_score:.1f}/10.0",
            delta=None
        )
    
    with col2:
        st.metric(
            "Format Compliance",
            "✅ Good" if ats_analysis['format_compliance']['text_length'] == 'good' else "⚠️ Needs Improvement"
        )
    
    with col3:
        red_flags_count = len(ats_analysis['red_flags'])
        st.metric(
            "Red Flags",
            red_flags_count,
            delta=None
        )
    
    # Detailed ATS Scores
    st.subheader("📊 Detailed ATS Scores")
    
    detailed_scores = ats_analysis['detailed_scores']
    score_data = {
        'Component': ['Keyword Optimization', 'Format Compliance', 'Structure', 'Content Quality', 'Completeness'],
        'Score': [
            detailed_scores['keyword_score'],
            detailed_scores['format_score'],
            detailed_scores['structure_score'],
            detailed_scores['content_score'],
            detailed_scores['completeness_score']
        ]
    }
    
    df_scores = pd.DataFrame(score_data)
    
    # Create horizontal bar chart
    fig = px.bar(
        df_scores, 
        x='Score', 
        y='Component',
        orientation='h',
        title="ATS Component Scores",
        color='Score',
        color_continuous_scale='RdYlGn',
        range_x=[0, 10]
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')
    
    # Red Flags
    if ats_analysis['red_flags']:
        st.subheader("🚨 ATS Red Flags")
        for flag in ats_analysis['red_flags']:
            st.markdown(f'<div class="red-flag-box">{flag}</div>', unsafe_allow_html=True)
    
    # Missing Elements
    if ats_analysis['missing_elements']:
        st.subheader("❌ Missing Elements")
        for element in ats_analysis['missing_elements']:
            st.write(f"• {element}")


def display_content_analysis(resume):
    """Display content analysis results."""
    st.header("📝 Content Analysis")
    
    # Skills Analysis
    if resume.skills:
        st.subheader("🛠️ Skills Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Technical Skills:**")
            tech_keywords = ['python', 'java', 'javascript', 'sql', 'aws', 'docker', 'kubernetes', 
                           'react', 'angular', 'vue', 'node', 'django', 'flask', 'spring', 'git',
                           'html', 'css', 'bootstrap', 'mongodb', 'postgresql', 'redis', 'linux',
                           'tensorflow', 'pytorch', 'machine learning', 'ai', 'data science']
            tech_skills = [skill for skill in resume.skills if any(tech in skill.lower() 
                         for tech in tech_keywords)]
            if tech_skills:
                for skill in tech_skills[:15]:  # Show first 15
                    st.write(f"• {skill}")
            else:
                st.write("No technical skills detected")
        
        with col2:
            st.write("**Soft Skills & Other:**")
            other_skills = [skill for skill in resume.skills if skill not in tech_skills]
            for skill in other_skills[:15]:  # Show first 15
                st.write(f"• {skill}")
    else:
        st.markdown('<div class="warning-box">No skills detected in the resume. Consider adding a skills section.</div>', unsafe_allow_html=True)
    
    # Summary Analysis
    if resume.summary:
        st.subheader("📋 Professional Summary")
        st.markdown(f'<div class="info-box">{resume.summary}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="warning-box">No professional summary found. Consider adding a summary section to highlight your key qualifications.</div>', unsafe_allow_html=True)
    
    # Experience Analysis
    if resume.experience:
        st.subheader("💼 Experience Analysis")
        
        for i, exp in enumerate(resume.experience, 1):
            with st.expander(f"Experience {i}: {exp.get('title', 'Unknown Title')} at {exp.get('company', 'Unknown Company')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Company:** {exp.get('company', 'N/A')}")
                    st.write(f"**Title:** {exp.get('title', 'N/A')}")
                    st.write(f"**Location:** {exp.get('location', 'N/A')}")
                
                with col2:
                    st.write(f"**Start Date:** {exp.get('start_date', 'N/A')}")
                    st.write(f"**End Date:** {exp.get('end_date', 'N/A')}")
                
                if exp.get('description'):
                    st.write(f"**Description:** {exp['description']}")
                
                if exp.get('responsibilities'):
                    st.write("**Responsibilities:**")
                    for resp in exp['responsibilities']:
                        st.write(f"• {resp}")
    else:
        st.markdown('<div class="warning-box">No work experience found. Consider adding internships, volunteer work, or projects to demonstrate your capabilities.</div>', unsafe_allow_html=True)
    
    # Education Analysis
    if resume.education:
        st.subheader("🎓 Education Analysis")
        
        for i, edu in enumerate(resume.education, 1):
            with st.expander(f"Education {i}: {edu.get('degree', 'Unknown Degree')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Institution:** {edu.get('institution', 'N/A')}")
                    st.write(f"**Degree:** {edu.get('degree', 'N/A')}")
                    st.write(f"**Field:** {edu.get('field', 'N/A')}")
                
                with col2:
                    st.write(f"**Start Date:** {edu.get('start_date', 'N/A')}")
                    st.write(f"**End Date:** {edu.get('end_date', 'N/A')}")
                    st.write(f"**GPA:** {edu.get('gpa', 'N/A')}")
                
                if edu.get('description'):
                    st.write(f"**Description:** {edu['description']}")
    else:
        st.markdown('<div class="warning-box">No education information found. Consider adding your educational background.</div>', unsafe_allow_html=True)
    
    # Projects Analysis
    if resume.projects:
        st.subheader("🚀 Projects Analysis")
        
        for i, proj in enumerate(resume.projects, 1):
            with st.expander(f"Project {i}: {proj.get('name', 'Unknown Project')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Project Name:** {proj.get('name', 'N/A')}")
                    st.write(f"**Technologies:** {', '.join(proj.get('technologies', []))}")
                
                with col2:
                    st.write(f"**Start Date:** {proj.get('start_date', 'N/A')}")
                    st.write(f"**End Date:** {proj.get('end_date', 'N/A')}")
                
                if proj.get('description'):
                    st.write(f"**Description:** {proj['description']}")
                
                if proj.get('url'):
                    st.write(f"**URL:** {proj['url']}")
    
    # Certifications Analysis
    if resume.certifications:
        st.subheader("🏆 Certifications Analysis")
        
        for i, cert in enumerate(resume.certifications, 1):
            with st.expander(f"Certification {i}: {cert.get('name', 'Unknown Certification')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Certification:** {cert.get('name', 'N/A')}")
                    st.write(f"**Issuer:** {cert.get('issuer', 'N/A')}")
                
                with col2:
                    st.write(f"**Date:** {cert.get('date', 'N/A')}")
                    st.write(f"**Expiration:** {cert.get('expiration_date', 'N/A')}")
                
                if cert.get('url'):
                    st.write(f"**URL:** {cert['url']}")


def display_recommendations(recommendations, ats_analysis):
    """Display recommendations for improvement."""
    st.header("💡 Improvement Recommendations")
    
    # General recommendations
    st.subheader("📋 General Recommendations")
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f'<div class="recommendation-box"><strong>{i}.</strong> {rec}</div>', 
                   unsafe_allow_html=True)
    
    # ATS-specific recommendations
    if ats_analysis and ats_analysis['recommendations']:
        st.subheader("🎯 ATS-Specific Recommendations")
        for i, rec in enumerate(ats_analysis['recommendations'], 1):
            st.markdown(f'<div class="recommendation-box"><strong>{i}.</strong> {rec}</div>', 
                       unsafe_allow_html=True)


def display_detailed_metrics(resume, ats_analysis, include_visualizations=True):
    """Display detailed metrics and visualizations."""
    st.header("📈 Detailed Metrics")
    
    if not include_visualizations:
        st.info("Visualizations are disabled. Enable them in the sidebar to see charts and graphs.")
        return
    
    # Keyword Analysis
    if ats_analysis and 'keyword_density' in ats_analysis:
        st.subheader("🔍 Keyword Analysis")
        
        keyword_data = ats_analysis['keyword_density']
        
        if keyword_data.get('technical_keywords'):
            st.write("**Technical Keywords Found:**")
            tech_df = pd.DataFrame(keyword_data['technical_keywords'])
            st.dataframe(tech_df, width='stretch')
        
        if keyword_data.get('soft_skills_keywords'):
            st.write("**Soft Skills Keywords Found:**")
            soft_df = pd.DataFrame(keyword_data['soft_skills_keywords'])
            st.dataframe(soft_df, width='stretch')
    
    # Skills Distribution
    if resume.skills:
        st.subheader("🛠️ Skills Distribution")
        
        # Categorize skills
        tech_skills = []
        soft_skills = []
        other_skills = []
        
        for skill in resume.skills:
            skill_lower = skill.lower()
            if any(tech in skill_lower for tech in ['python', 'java', 'javascript', 'sql', 'aws', 'docker']):
                tech_skills.append(skill)
            elif any(soft in skill_lower for soft in ['leadership', 'communication', 'teamwork', 'management']):
                soft_skills.append(skill)
            else:
                other_skills.append(skill)
        
        # Create pie chart
        categories = ['Technical Skills', 'Soft Skills', 'Other Skills']
        counts = [len(tech_skills), len(soft_skills), len(other_skills)]
        
        if sum(counts) > 0:
            fig = px.pie(
                values=counts,
                names=categories,
                title="Skills Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, width='stretch')
    
    # Text Statistics
    if resume.raw_text:
        st.subheader("📊 Text Statistics")
        
        stats = text_utils.calculate_text_stats(resume.raw_text)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Word Count", stats.get('word_count', 0))
        with col2:
            st.metric("Character Count", stats.get('char_count', 0))
        with col3:
            st.metric("Sentence Count", stats.get('sentence_count', 0))
        with col4:
            st.metric("Lexical Diversity", f"{stats.get('lexical_diversity', 0):.2f}")


def display_welcome_screen():
    """Display the welcome screen when no file is uploaded."""
    st.markdown("""
    ## Welcome to the Resume Analyzer Dashboard! 🎉
    
    This comprehensive tool helps you optimize your resume for both human readers and 
    Applicant Tracking Systems (ATS). Upload your resume to get started with:
    
    ### ✨ Features
    - **ATS Compatibility Scoring** - See how well your resume will perform in ATS systems
    - **Keyword Analysis** - Identify missing or overused keywords
    - **Skills Assessment** - Analyze your technical and soft skills
    - **Experience Evaluation** - Review your work experience presentation
    - **Improvement Recommendations** - Get actionable advice to enhance your resume
    
    ### 📁 Supported File Formats
    - PDF (.pdf)
    - Microsoft Word (.docx, .doc)
    - Plain Text (.txt)
    - Rich Text Format (.rtf)
    
    ### 🚀 Getting Started
    1. Upload your resume using the file uploader in the sidebar
    2. Configure your analysis options
    3. Review the comprehensive analysis results
    4. Implement the recommended improvements
    
    ### 💡 Pro Tips
    - Use standard section headers (Experience, Education, Skills)
    - Include relevant keywords from job descriptions
    - Quantify your achievements with specific numbers
    - Keep your resume between 300-700 words for optimal ATS performance
    - Use bullet points for better readability
    
    **Ready to optimize your resume? Upload a file to get started!** 📄
    """)


def get_score_class(score):
    """Get CSS class for score styling."""
    if score >= 8:
        return "score-excellent"
    elif score >= 6:
        return "score-good"
    elif score >= 4:
        return "score-fair"
    else:
        return "score-poor"


if __name__ == "__main__":
    main()
