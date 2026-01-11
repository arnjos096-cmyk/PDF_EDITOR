#!/usr/bin/env python3
"""
Integration test for AI PDF Commander
Tests the complete flow from command parsing to backend execution
"""

import sys
import os
import subprocess

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from ai.command_parser import CommandParser


def test_command_parser():
    """Test AI command parser"""
    print("Testing AI Command Parser...")
    parser = CommandParser()
    
    # Test 1: Merge command
    result = parser.parse("Merge these files", ["file1.pdf", "file2.pdf"])
    assert result['success'], "Parse failed for merge command"
    assert len(result['commands']) == 1, "Should have 1 command"
    assert result['commands'][0]['action'] == 'MERGE', "Should be MERGE action"
    print("  ✓ Merge command parsing works")
    
    # Test 2: Watermark command
    result = parser.parse('Add watermark "Confidential"', ["doc.pdf"])
    assert result['success'], "Parse failed for watermark command"
    assert result['commands'][0]['action'] == 'WATERMARK', "Should be WATERMARK action"
    assert 'confidential' in result['commands'][0]['params'][1].lower(), "Should extract watermark text"
    print("  ✓ Watermark command parsing works")
    
    # Test 3: Extract command
    result = parser.parse("Extract pages 1 to 10", ["report.pdf"])
    assert result['success'], "Parse failed for extract command"
    assert result['commands'][0]['action'] == 'EXTRACT', "Should be EXTRACT action"
    print("  ✓ Extract command parsing works")
    
    # Test 4: Multi-command
    result = parser.parse("Merge these notes and remove the last page", ["n1.pdf", "n2.pdf"])
    assert result['success'], "Parse failed for multi-command"
    assert len(result['commands']) >= 2, "Should have multiple commands"
    print("  ✓ Multi-command parsing works")
    
    print("✅ All command parser tests passed!\n")


def test_cpp_backend():
    """Test C++ backend"""
    print("Testing C++ Backend...")
    
    backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'pdf_operations')
    
    if not os.path.exists(backend_path):
        print("  ⚠ Backend not built, skipping C++ tests")
        return
    
    # Test 1: MERGE command
    result = subprocess.run(
        [backend_path, 'MERGE', 'f1.pdf', 'f2.pdf', 'out.pdf'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "MERGE command failed"
    assert 'SUCCESS' in result.stdout, "MERGE should return SUCCESS"
    print("  ✓ MERGE operation works")
    
    # Test 2: WATERMARK command
    result = subprocess.run(
        [backend_path, 'WATERMARK', 'in.pdf', 'Test', 'out.pdf'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "WATERMARK command failed"
    assert 'SUCCESS' in result.stdout, "WATERMARK should return SUCCESS"
    print("  ✓ WATERMARK operation works")
    
    # Test 3: EXTRACT command
    result = subprocess.run(
        [backend_path, 'EXTRACT', 'in.pdf', '1', '5', 'out.pdf'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "EXTRACT command failed"
    assert 'SUCCESS' in result.stdout, "EXTRACT should return SUCCESS"
    print("  ✓ EXTRACT operation works")
    
    print("✅ All C++ backend tests passed!\n")


def test_command_generation():
    """Test command string generation"""
    print("Testing Command String Generation...")
    parser = CommandParser()
    
    # Parse a command
    result = parser.parse("Merge these files", ["a.pdf", "b.pdf"])
    
    # Generate command string
    for cmd in result['commands']:
        cmd_str = parser.generate_command_string(cmd)
        assert cmd['action'] in cmd_str, "Command string should contain action"
        print(f"  ✓ Generated: {cmd_str}")
    
    print("✅ Command generation works!\n")


def main():
    """Run all tests"""
    print("\n" + "="*50)
    print("  AI PDF Commander - Integration Tests")
    print("="*50 + "\n")
    
    try:
        test_command_parser()
        test_cpp_backend()
        test_command_generation()
        
        print("="*50)
        print("  ✅ ALL TESTS PASSED!")
        print("="*50)
        return 0
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
