#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF Parser Module

This module provides functionality for parsing PDF resume files.
"""

import os
from typing import Optional

from resume_analyzer.parsers.base_parser import BaseParser


class PDFParser(BaseParser):
    """
    Parser for PDF resume files.
    Uses PyPDF2 or pdfminer.six to extract text from PDF files.
    """
    
    def __init__(self):
        """
        Initialize the PDF parser.
        Tries to import required libraries and raises ImportError if they are not available.
        """
        try:
            # Try to import PyPDF2 first
            import PyPDF2
            self._use_pypdf2 = True
        except ImportError:
            try:
                # If PyPDF2 is not available, try to import pdfminer.six
                from pdfminer.high_level import extract_text
                self._use_pypdf2 = False
            except ImportError:
                raise ImportError(
                    "Neither PyPDF2 nor pdfminer.six is installed. "
                    "Please install one of them using pip: "
                    "pip install PyPDF2 or pip install pdfminer.six"
                )
    
    def parse(self, file_path: str) -> str:
        """
        Parse the PDF file and extract its text content.
        
        Args:
            file_path (str): Path to the PDF file.
            
        Returns:
            str: The extracted text content from the PDF.
            
        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file cannot be parsed.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not os.path.isfile(file_path):
            raise ValueError(f"Not a file: {file_path}")
        
        try:
            if self._use_pypdf2:
                return self._parse_with_pypdf2(file_path)
            else:
                return self._parse_with_pdfminer(file_path)
        except Exception as e:
            raise ValueError(f"Error parsing PDF file: {e}")
    
    def _parse_with_pypdf2(self, file_path: str) -> str:
        """
        Parse the PDF file using PyPDF2.
        
        Args:
            file_path (str): Path to the PDF file.
            
        Returns:
            str: The extracted text content from the PDF.
        """
        import PyPDF2
        
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
        
        return text
    
    def _parse_with_pdfminer(self, file_path: str) -> str:
        """
        Parse the PDF file using pdfminer.six.
        
        Args:
            file_path (str): Path to the PDF file.
            
        Returns:
            str: The extracted text content from the PDF.
        """
        from pdfminer.high_level import extract_text
        
        text = extract_text(file_path)
        return text