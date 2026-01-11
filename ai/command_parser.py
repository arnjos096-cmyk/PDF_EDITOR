#!/usr/bin/env python3
"""
AI Command Parser - Translates natural language to PDF operation commands
This is the "brain" that interprets user requests and generates command codes
"""

import re
import json
from typing import Dict, List, Optional


class CommandParser:
    """Parse natural language commands into structured PDF operations"""
    
    def __init__(self):
        self.command_patterns = {
            'merge': [
                r'merge\s+(?:these\s+)?(?:files?|pdfs?|documents?|notes?)',
                r'combine\s+(?:these\s+)?(?:files?|pdfs?|documents?)',
                r'join\s+(?:these\s+)?(?:files?|pdfs?|documents?)',
            ],
            'remove_pages': [
                r'remove\s+(?:the\s+)?(?:last|first|\d+(?:st|nd|rd|th)?)\s+pages?',
                r'delete\s+(?:the\s+)?(?:last|first|\d+(?:st|nd|rd|th)?)\s+pages?',
                r'take\s+out\s+(?:the\s+)?(?:last|first|\d+(?:st|nd|rd|th)?)\s+pages?',
            ],
            'watermark': [
                r'watermark\s+(?:as\s+)?["\']([^"\']+)["\']',
                r'add\s+watermark\s+["\']([^"\']+)["\']',
                r'mark\s+(?:as\s+)?["\']([^"\']+)["\']',
            ],
            'extract': [
                r'extract\s+pages?\s+(\d+)\s*(?:to|-)\s*(\d+)',
                r'get\s+pages?\s+(\d+)\s*(?:to|-)\s*(\d+)',
                r'save\s+pages?\s+(\d+)\s*(?:to|-)\s*(\d+)',
            ],
        }
    
    def parse(self, user_input: str, uploaded_files: List[str] = None) -> Dict:
        """
        Parse natural language input into a command structure
        
        Args:
            user_input: The user's natural language command
            uploaded_files: List of uploaded PDF filenames
            
        Returns:
            Dictionary with command details
        """
        user_input = user_input.lower().strip()
        uploaded_files = uploaded_files or []
        
        result = {
            'raw_input': user_input,
            'commands': [],
            'success': True,
            'error': None
        }
        
        # Check for merge operations
        if self._matches_pattern(user_input, self.command_patterns['merge']):
            result['commands'].append({
                'action': 'MERGE',
                'params': uploaded_files + ['merged_output.pdf'],
                'description': 'Merge uploaded PDF files'
            })
        
        # Check for page removal
        remove_match = self._find_pattern_match(user_input, self.command_patterns['remove_pages'])
        if remove_match:
            pages_to_remove = self._extract_page_numbers(user_input)
            if pages_to_remove:
                result['commands'].append({
                    'action': 'REMOVE_PAGES',
                    'params': [uploaded_files[0] if uploaded_files else 'input.pdf'] + 
                              [str(p) for p in pages_to_remove] + ['output_removed.pdf'],
                    'description': f'Remove pages: {pages_to_remove}'
                })
        
        # Check for watermark
        watermark_match = self._find_pattern_match(user_input, self.command_patterns['watermark'])
        if watermark_match:
            watermark_text = self._extract_watermark_text(user_input)
            if watermark_text:
                result['commands'].append({
                    'action': 'WATERMARK',
                    'params': [uploaded_files[0] if uploaded_files else 'input.pdf',
                              watermark_text, 'output_watermarked.pdf'],
                    'description': f'Add watermark: {watermark_text}'
                })
        
        # Check for extract
        extract_match = self._find_pattern_match(user_input, self.command_patterns['extract'])
        if extract_match:
            page_range = self._extract_page_range(user_input)
            if page_range:
                result['commands'].append({
                    'action': 'EXTRACT',
                    'params': [uploaded_files[0] if uploaded_files else 'input.pdf',
                              str(page_range[0]), str(page_range[1]), 'output_extracted.pdf'],
                    'description': f'Extract pages {page_range[0]} to {page_range[1]}'
                })
        
        if not result['commands']:
            result['success'] = False
            result['error'] = 'Could not understand command. Try: "Merge these files", "Remove the last page", or "Add watermark \'Confidential\'"'
        
        return result
    
    def _matches_pattern(self, text: str, patterns: List[str]) -> bool:
        """Check if text matches any of the given patterns"""
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _find_pattern_match(self, text: str, patterns: List[str]) -> Optional[re.Match]:
        """Find the first pattern that matches"""
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match
        return None
    
    def _extract_page_numbers(self, text: str) -> List[int]:
        """Extract page numbers to remove from text"""
        if 'last' in text:
            # Extract number if specified, default to 1
            match = re.search(r'last\s+(\d+)', text)
            if match:
                return [-1 * int(match.group(1))]  # Negative means from end
            return [-1]
        elif 'first' in text:
            match = re.search(r'first\s+(\d+)', text)
            if match:
                return list(range(1, int(match.group(1)) + 1))
            return [1]
        else:
            # Extract specific page numbers
            numbers = re.findall(r'\d+', text)
            return [int(n) for n in numbers]
    
    def _extract_watermark_text(self, text: str) -> Optional[str]:
        """Extract watermark text from quotes"""
        match = re.search(r'["\']([^"\']+)["\']', text)
        if match:
            return match.group(1)
        return None
    
    def _extract_page_range(self, text: str) -> Optional[tuple]:
        """Extract page range like '1-5' or '1 to 5'"""
        match = re.search(r'(\d+)\s*(?:to|-)\s*(\d+)', text)
        if match:
            return (int(match.group(1)), int(match.group(2)))
        return None
    
    def generate_command_string(self, command: Dict) -> str:
        """Generate command string for C++ backend"""
        return f"{command['action']} {' '.join(command['params'])}"


def main():
    """Example usage"""
    parser = CommandParser()
    
    # Test examples
    examples = [
        ("Merge these notes and remove the last page.", ["note1.pdf", "note2.pdf"]),
        ("Add watermark 'Confidential' to the document", ["document.pdf"]),
        ("Extract pages 1 to 5", ["report.pdf"]),
        ("Combine these files", ["file1.pdf", "file2.pdf", "file3.pdf"]),
    ]
    
    for text, files in examples:
        print(f"\nInput: {text}")
        print(f"Files: {files}")
        result = parser.parse(text, files)
        print(f"Result: {json.dumps(result, indent=2)}")


if __name__ == "__main__":
    main()
