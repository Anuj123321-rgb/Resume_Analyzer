#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Parser Factory Module

This module provides a factory for creating appropriate parser objects
based on the file type of the resume.
"""

import os
from typing import List, Type

from resume_analyzer.parsers.base_parser import BaseParser
from resume_analyzer.parsers.pdf_parser import PDFParser
from resume_analyzer.parsers.docx_parser import DocxParser
from resume_analyzer.parsers.text_parser import TextParser


# List of supported file extensions
SUPPORTED_EXTENSIONS = {
    '.pdf': PDFParser,
    '.docx': DocxParser,
    '.doc': DocxParser,  # Note: .doc files might not parse correctly with DocxParser
    '.txt': TextParser,
    '.rtf': TextParser,  # Note: .rtf files might not parse correctly with TextParser
}


def get_parser(file_path: str) -> BaseParser:
    """
    Get the appropriate parser for the given file.
    
    Args:
        file_path (str): Path to the resume file.
        
    Returns:
        BaseParser: An instance of the appropriate parser for the file type.
        
    Raises:
        ValueError: If the file type is not supported.
    """
    _, ext = os.path.splitext(file_path.lower())
    
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}. Supported types are: {', '.join(SUPPORTED_EXTENSIONS.keys())}")
    
    parser_class = SUPPORTED_EXTENSIONS[ext]
    return parser_class()


def is_supported_file(file_path: str) -> bool:
    """
    Check if the file type is supported by the parser factory.
    
    Args:
        file_path (str): Path to the file to check.
        
    Returns:
        bool: True if the file type is supported, False otherwise.
    """
    _, ext = os.path.splitext(file_path.lower())
    return ext in SUPPORTED_EXTENSIONS


def get_supported_extensions() -> List[str]:
    """
    Get a list of supported file extensions.
    
    Returns:
        List[str]: List of supported file extensions.
    """
    return list(SUPPORTED_EXTENSIONS.keys())