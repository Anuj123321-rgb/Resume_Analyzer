#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Text Parser Module

This module provides functionality for parsing plain text resume files.
"""

import os
from typing import Optional

from resume_analyzer.parsers.base_parser import BaseParser


class TextParser(BaseParser):
    """
    Parser for plain text resume files.
    Handles .txt files and attempts to handle .rtf files by stripping RTF markup.
    """
    
    def parse(self, file_path: str) -> str:
        """
        Parse the text file and extract its content.
        
        Args:
            file_path (str): Path to the text file.
            
        Returns:
            str: The extracted text content from the file.
            
        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file cannot be parsed.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not os.path.isfile(file_path):
            raise ValueError(f"Not a file: {file_path}")
        
        try:
            _, ext = os.path.splitext(file_path.lower())
            
            if ext == '.rtf':
                return self._parse_rtf(file_path)
            else:  # .txt or other text files
                return self._parse_txt(file_path)
        except Exception as e:
            raise ValueError(f"Error parsing text file: {e}")
    
    def _parse_txt(self, file_path: str) -> str:
        """
        Parse a plain text file.
        
        Args:
            file_path (str): Path to the text file.
            
        Returns:
            str: The content of the text file.
        """
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            return file.read()
    
    def _parse_rtf(self, file_path: str) -> str:
        """
        Parse an RTF file by stripping RTF markup.
        This is a simple implementation and may not handle all RTF features.
        For better RTF parsing, consider using a dedicated RTF parser library.
        
        Args:
            file_path (str): Path to the RTF file.
            
        Returns:
            str: The extracted text content from the RTF file.
        """
        try:
            # Try to use striprtf if available
            from striprtf.striprtf import rtf_to_text
            
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                rtf_text = file.read()
            
            return rtf_to_text(rtf_text)
        except ImportError:
            # Fallback to a simple RTF stripping method
            with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                rtf_text = file.read()
            
            # Simple RTF stripping - this is not comprehensive
            # Remove RTF headers
            if rtf_text.startswith('{\\rtf'):
                # Find text between curly braces, ignoring RTF commands
                in_text = False
                text = []
                i = 0
                
                while i < len(rtf_text):
                    if rtf_text[i] == '{' and not in_text:
                        in_text = True
                    elif rtf_text[i] == '}' and in_text:
                        in_text = False
                    elif rtf_text[i] == '\\' and in_text:
                        # Skip RTF command
                        i += 1
                        while i < len(rtf_text) and rtf_text[i].isalpha():
                            i += 1
                    elif in_text:
                        text.append(rtf_text[i])
                    i += 1
                
                return ''.join(text)
            else:
                # If it doesn't look like RTF, treat as plain text
                return rtf_text