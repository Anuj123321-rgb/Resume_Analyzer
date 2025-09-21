#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Base Parser Module

This module defines the BaseParser abstract class that all resume parsers must implement.
"""

from abc import ABC, abstractmethod


class BaseParser(ABC):
    """
    Abstract base class for resume parsers.
    All specific file format parsers should inherit from this class.
    """
    
    @abstractmethod
    def parse(self, file_path: str) -> str:
        """
        Parse the resume file and extract its text content.
        
        Args:
            file_path (str): Path to the resume file.
            
        Returns:
            str: The extracted text content from the resume.
            
        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file cannot be parsed.
        """
        pass