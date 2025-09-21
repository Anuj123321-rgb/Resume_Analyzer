#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Resume Analyzer - Main Module

This module serves as the entry point for the resume analyzer application.
It coordinates the parsing, analysis, and presentation of resume data.
"""

import os
import sys
import argparse
from pathlib import Path

# Add the parent directory to sys.path to allow imports from the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from resume_analyzer.parsers import parser_factory
from resume_analyzer.analyzers import content_analyzer, skills_analyzer, experience_analyzer
from resume_analyzer.models.resume import Resume
from resume_analyzer.utils import file_utils, text_utils


def parse_arguments():
    """
    Parse command line arguments for the resume analyzer.
    
    Returns:
        argparse.Namespace: The parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description='Analyze resumes and extract key information')
    parser.add_argument('resume_path', type=str, help='Path to the resume file or directory containing resumes')
    parser.add_argument('--output', '-o', type=str, default='output', help='Directory to save analysis results')
    parser.add_argument('--format', '-f', choices=['text', 'json', 'html'], default='text',
                        help='Output format for analysis results')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    
    return parser.parse_args()


def analyze_resume(resume_path, output_dir, output_format, verbose=False):
    """
    Analyze a single resume file.
    
    Args:
        resume_path (str): Path to the resume file.
        output_dir (str): Directory to save analysis results.
        output_format (str): Format for output (text, json, or html).
        verbose (bool): Whether to print verbose output.
        
    Returns:
        dict: Analysis results.
    """
    if verbose:
        print(f"Analyzing resume: {resume_path}")
    
    # Get the appropriate parser based on file extension
    parser = parser_factory.get_parser(resume_path)
    
    # Parse the resume
    resume_text = parser.parse(resume_path)
    
    # Create a Resume object
    resume = Resume(resume_text, os.path.basename(resume_path))
    
    # Analyze the resume content
    content_analyzer.analyze(resume)
    skills_analyzer.analyze(resume)
    experience_analyzer.analyze(resume)
    
    # Generate output
    output_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(resume_path))[0]}.{output_format}")
    
    # Save results
    if output_format == 'json':
        file_utils.save_json(resume.to_dict(), output_path)
    elif output_format == 'html':
        file_utils.save_html(resume, output_path)
    else:  # text format
        file_utils.save_text(resume.to_text(), output_path)
    
    if verbose:
        print(f"Analysis complete. Results saved to {output_path}")
    
    return resume.to_dict()


def analyze_directory(directory_path, output_dir, output_format, verbose=False):
    """
    Analyze all resumes in a directory.
    
    Args:
        directory_path (str): Path to directory containing resumes.
        output_dir (str): Directory to save analysis results.
        output_format (str): Format for output (text, json, or html).
        verbose (bool): Whether to print verbose output.
        
    Returns:
        list: List of analysis results for each resume.
    """
    if verbose:
        print(f"Analyzing resumes in directory: {directory_path}")
    
    results = []
    
    # Get all files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
        
        # Skip files that don't have supported extensions
        if not parser_factory.is_supported_file(file_path):
            if verbose:
                print(f"Skipping unsupported file: {file_path}")
            continue
        
        # Analyze the resume
        result = analyze_resume(file_path, output_dir, output_format, verbose)
        results.append(result)
    
    return results


def main():
    """
    Main entry point for the resume analyzer application.
    """
    args = parse_arguments()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    if os.path.isdir(args.resume_path):
        # Analyze all resumes in the directory
        results = analyze_directory(args.resume_path, args.output, args.format, args.verbose)
        print(f"Analyzed {len(results)} resumes. Results saved to {args.output}")
    else:
        # Analyze a single resume
        analyze_resume(args.resume_path, args.output, args.format, args.verbose)
    
    print("Resume analysis complete.")


if __name__ == "__main__":
    main()