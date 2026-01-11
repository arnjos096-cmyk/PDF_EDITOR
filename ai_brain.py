#!/usr/bin/env python3
"""
AI Brain - Command Parser
Translates natural language commands into structured command codes
for the C++ PDF processing backend
"""

import re
import json
from typing import Dict, List, Optional


class PDFCommandParser:
    """
    AI Brain component that interprets natural language commands
    and converts them into structured command codes for PDF operations
    """
    
    def __init__(self):
        self.supported_actions = {
            'merge': ['merge', 'combine', 'join', 'concatenate'],
            'remove': ['remove', 'delete', 'drop', 'eliminate'],
            'watermark': ['watermark', 'stamp', 'mark'],
            'extract': ['extract', 'get', 'pull out'],
            'rotate': ['rotate', 'turn', 'flip'],
            'split': ['split', 'separate', 'divide'],
            'compress': ['compress', 'reduce', 'shrink']
        }
    
    def parse(self, command: str, files: List[str]) -> Dict:
        """
        Parse natural language command and return structured command code
        
        Args:
            command: Natural language command from user
            files: List of uploaded file names
            
        Returns:
            Dictionary containing action, parameters, and command code
        """
        command_lower = command.lower()
        
        # Detect action
        action = self._detect_action(command_lower)
        
        if action == 'merge':
            return self._parse_merge(command_lower, files)
        elif action == 'remove':
            return self._parse_remove(command_lower, files)
        elif action == 'watermark':
            return self._parse_watermark(command_lower, files)
        elif action == 'extract':
            return self._parse_extract(command_lower, files)
        elif action == 'rotate':
            return self._parse_rotate(command_lower, files)
        elif action == 'split':
            return self._parse_split(command_lower, files)
        elif action == 'compress':
            return self._parse_compress(command_lower, files)
        else:
            return {
                'action': 'UNKNOWN',
                'command_code': 'CMD_UNKNOWN',
                'description': 'Could not understand command',
                'params': {}
            }
    
    def _detect_action(self, command: str) -> Optional[str]:
        """Detect the primary action from command text"""
        for action, keywords in self.supported_actions.items():
            for keyword in keywords:
                if keyword in command:
                    return action
        return None
    
    def _parse_merge(self, command: str, files: List[str]) -> Dict:
        """Parse merge command"""
        return {
            'action': 'MERGE',
            'command_code': f'CMD_MERGE_PDF {len(files)}',
            'description': f'Merging {len(files)} PDF file(s)',
            'params': {
                'files': files,
                'output': 'merged_output.pdf'
            }
        }
    
    def _parse_remove(self, command: str, files: List[str]) -> Dict:
        """Parse remove page command"""
        params = {'file': files[0] if files else 'document.pdf'}
        
        # Detect "last page"
        if 'last' in command:
            params['page'] = 'LAST'
            cmd_code = 'CMD_REMOVE_PAGE LAST'
            desc = 'Removing the last page'
        # Detect specific page number
        else:
            page_match = re.search(r'page\s+(\d+)', command)
            if page_match:
                params['page'] = int(page_match.group(1))
                cmd_code = f"CMD_REMOVE_PAGE {params['page']}"
                desc = f"Removing page {params['page']}"
            else:
                # Default to last page
                params['page'] = 'LAST'
                cmd_code = 'CMD_REMOVE_PAGE LAST'
                desc = 'Removing the last page'
        
        return {
            'action': 'REMOVE_PAGE',
            'command_code': cmd_code,
            'description': desc,
            'params': params
        }
    
    def _parse_watermark(self, command: str, files: List[str]) -> Dict:
        """Parse watermark command"""
        params = {}
        
        # Extract watermark text from quotes
        text_match = re.search(r'[\'"]([^\'"]+)[\'"]', command)
        if text_match:
            params['text'] = text_match.group(1)
        else:
            # Default watermark
            params['text'] = 'CONFIDENTIAL'
        
        # Detect page specification
        if 'last' in command:
            params['pages'] = 'LAST'
        elif 'first' in command:
            params['pages'] = 'FIRST'
        else:
            params['pages'] = 'ALL'
        
        params['file'] = files[0] if files else 'document.pdf'
        
        return {
            'action': 'WATERMARK',
            'command_code': f'CMD_WATERMARK "{params["text"]}" {params["pages"]}',
            'description': f'Adding watermark "{params["text"]}" to {params["pages"]} page(s)',
            'params': params
        }
    
    def _parse_extract(self, command: str, files: List[str]) -> Dict:
        """Parse extract pages command"""
        params = {'file': files[0] if files else 'document.pdf'}
        
        # Look for page range (e.g., "1-5" or "pages 1 to 5")
        range_match = re.search(r'(\d+)\s*[-to]+\s*(\d+)', command)
        if range_match:
            params['start_page'] = int(range_match.group(1))
            params['end_page'] = int(range_match.group(2))
            cmd_code = f"CMD_EXTRACT_PAGES {params['start_page']}-{params['end_page']}"
            desc = f"Extracting pages {params['start_page']}-{params['end_page']}"
        else:
            # Look for single page
            page_match = re.search(r'page\s+(\d+)', command)
            if page_match:
                params['start_page'] = int(page_match.group(1))
                params['end_page'] = params['start_page']
                cmd_code = f"CMD_EXTRACT_PAGES {params['start_page']}"
                desc = f"Extracting page {params['start_page']}"
            else:
                return {
                    'action': 'UNKNOWN',
                    'command_code': 'CMD_UNKNOWN',
                    'description': 'Could not determine which pages to extract',
                    'params': {}
                }
        
        return {
            'action': 'EXTRACT',
            'command_code': cmd_code,
            'description': desc,
            'params': params
        }
    
    def _parse_rotate(self, command: str, files: List[str]) -> Dict:
        """Parse rotate pages command"""
        params = {'file': files[0] if files else 'document.pdf'}
        
        # Detect rotation angle
        if '180' in command:
            params['angle'] = 180
        elif '270' in command or '-90' in command:
            params['angle'] = 270
        else:
            params['angle'] = 90  # Default
        
        # Detect which pages
        if 'all' in command:
            params['pages'] = 'ALL'
        else:
            params['pages'] = 'ALL'  # Default to all
        
        return {
            'action': 'ROTATE',
            'command_code': f"CMD_ROTATE_PAGES {params['angle']} {params['pages']}",
            'description': f"Rotating pages by {params['angle']} degrees",
            'params': params
        }
    
    def _parse_split(self, command: str, files: List[str]) -> Dict:
        """Parse split PDF command"""
        params = {'file': files[0] if files else 'document.pdf'}
        
        # Look for split point
        page_match = re.search(r'page\s+(\d+)', command)
        if page_match:
            params['split_at'] = int(page_match.group(1))
        else:
            params['split_at'] = 'EACH'  # Split into individual pages
        
        return {
            'action': 'SPLIT',
            'command_code': f"CMD_SPLIT_PDF {params.get('split_at', 'EACH')}",
            'description': f"Splitting PDF at page {params.get('split_at', 'each page')}",
            'params': params
        }
    
    def _parse_compress(self, command: str, files: List[str]) -> Dict:
        """Parse compress PDF command"""
        params = {'file': files[0] if files else 'document.pdf'}
        
        # Detect compression level
        if 'high' in command or 'maximum' in command:
            params['level'] = 'HIGH'
        elif 'low' in command or 'light' in command:
            params['level'] = 'LOW'
        else:
            params['level'] = 'MEDIUM'
        
        return {
            'action': 'COMPRESS',
            'command_code': f"CMD_COMPRESS_PDF {params['level']}",
            'description': f"Compressing PDF with {params['level']} compression",
            'params': params
        }


def main():
    """Test the parser with example commands"""
    parser = PDFCommandParser()
    
    test_commands = [
        ("Merge these notes and remove the last page", ["notes1.pdf", "notes2.pdf"]),
        ("Remove page 3 from document.pdf", ["document.pdf"]),
        ("Watermark all pages with 'Confidential'", ["report.pdf"]),
        ("Extract pages 1-5", ["book.pdf"]),
        ("Rotate all pages by 90 degrees", ["scan.pdf"]),
    ]
    
    print("=== AI Brain Command Parser Test ===\n")
    
    for command, files in test_commands:
        result = parser.parse(command, files)
        print(f"Command: {command}")
        print(f"Files: {files}")
        print(f"Result: {json.dumps(result, indent=2)}")
        print("-" * 50)


if __name__ == '__main__':
    main()
