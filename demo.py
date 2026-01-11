#!/usr/bin/env python3
"""
Demo script to showcase AI PDF Commander capabilities
"""

import json
import sys
import os

# Add paths
sys.path.insert(0, os.path.dirname(__file__))
from ai.command_parser import CommandParser


def print_separator():
    print("\n" + "="*70 + "\n")


def demo_command(parser, command, files):
    """Demonstrate a command"""
    print(f"📝 User Command: \"{command}\"")
    print(f"📄 Files: {', '.join(files)}")
    print()
    
    result = parser.parse(command, files)
    
    if result['success']:
        print("✨ AI Understanding:")
        for i, cmd in enumerate(result['commands'], 1):
            print(f"   {i}. {cmd['description']}")
            print(f"      → Action: {cmd['action']}")
            print(f"      → Parameters: {', '.join(cmd['params'])}")
            
            # Show what backend would execute
            cmd_string = parser.generate_command_string(cmd)
            print(f"      → Backend Command: {cmd_string}")
    else:
        print(f"❌ Error: {result['error']}")
    
    print_separator()


def main():
    """Run demo"""
    print_separator()
    print("           🤖 AI PDF Commander - DEMO")
    print("     Chat with your PDFs - No complex menus needed!")
    print_separator()
    
    parser = CommandParser()
    
    # Demo 1: Simple merge
    print("DEMO 1: Merging Documents")
    demo_command(
        parser,
        "Merge these files",
        ["quarterly_report_q1.pdf", "quarterly_report_q2.pdf", "quarterly_report_q3.pdf"]
    )
    
    # Demo 2: Remove pages
    print("DEMO 2: Removing Pages")
    demo_command(
        parser,
        "Remove the last page",
        ["confidential_document.pdf"]
    )
    
    # Demo 3: Watermark
    print("DEMO 3: Adding Watermark")
    demo_command(
        parser,
        'Add watermark "Confidential"',
        ["internal_memo.pdf"]
    )
    
    # Demo 4: Extract pages
    print("DEMO 4: Extracting Pages")
    demo_command(
        parser,
        "Extract pages 1 to 5",
        ["full_report_100_pages.pdf"]
    )
    
    # Demo 5: Complex multi-command
    print("DEMO 5: Complex Multi-Step Operation")
    demo_command(
        parser,
        "Merge these notes and remove the last page",
        ["meeting_notes_day1.pdf", "meeting_notes_day2.pdf"]
    )
    
    # Demo 6: Another watermark example
    print("DEMO 6: Custom Watermark")
    demo_command(
        parser,
        'Watermark as "Draft - Internal Use Only"',
        ["proposal_v2.pdf"]
    )
    
    # Show capabilities summary
    print("\n✨ KEY CAPABILITIES:\n")
    print("1. 🔄 Natural Language Understanding")
    print("   - No need to learn complex commands")
    print("   - Just type what you want in plain English")
    print()
    print("2. 🎯 Multiple Operations")
    print("   - Merge: Combine multiple PDFs")
    print("   - Split: Remove or extract specific pages")
    print("   - Watermark: Add text overlays")
    print("   - Extract: Get page ranges")
    print()
    print("3. ⚡ Fast Processing")
    print("   - AI parser translates instantly")
    print("   - C++ backend processes quickly")
    print()
    print("4. 🔗 Complete Integration")
    print("   - Web UI → AI Parser → C++ Backend")
    print("   - Seamless flow from chat to execution")
    print()
    print_separator()
    
    print("🚀 Ready to try it yourself?")
    print()
    print("Run: ./start.sh")
    print("Then visit: http://localhost:5000")
    print()
    print_separator()


if __name__ == "__main__":
    main()
