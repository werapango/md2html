#!/usr/bin/env python3
"""
Markdown to HTML Converter with Mermaid Diagram Support
สำหรับแปลงไฟล์ Markdown ที่มี Mermaid diagrams เป็น HTML
"""

import argparse
import os
import sys
from pathlib import Path
import re

from markdown import Markdown
from markdown.extensions import codehilite, tables, toc
# Import HTML Mermaid Processor (no API, no external dependencies)
try:
    from mermaid_processor_html import MermaidProcessorPy as HtmlMermaidProcessor
except ImportError:
    HtmlMermaidProcessor = None




class MarkdownConverter:
    """แปลงไฟล์ Markdown เป็น HTML"""
    
    def __init__(self):
        # ใช้ HTML Mermaid Processor (ไม่ใช้ API, ไม่ใช้ external dependencies)
        if HtmlMermaidProcessor is not None:
            self.mermaid_processor = HtmlMermaidProcessor()
            print("Using HTML Mermaid Processor (no API, no external dependencies)")
        else:
            self.mermaid_processor = None
            print("HTML Mermaid Processor not available - Mermaid diagrams will be skipped")
        self.md = Markdown(
            extensions=[
                'codehilite',
                'tables',
                'toc',
                'fenced_code',
                'attr_list'
            ],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight',
                    'use_pygments': True
                },
                'toc': {
                    'permalink': True,
                    'permalink_title': 'Permalink'
                }
            }
        )
    
    def read_markdown_file(self, file_path: str) -> str:
        """อ่านไฟล์ Markdown"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Error reading file {file_path}: {e}")
    
    def process_markdown(self, content: str, include_images: bool = True) -> str:
        """ประมวลผล Markdown และจัดการ Mermaid diagrams"""
        if include_images and self.mermaid_processor:
            try:
                content = self.mermaid_processor.replace_mermaid_with_images(content)
            except Exception as e:
                # หาก Mermaid API ไม่ทำงาน ให้ใช้วิธีแสดงแบบอื่น
                print(f"Warning: Mermaid API error: {e}")
                print("Using alternative Mermaid display method...")
                content = self.replace_mermaid_with_alternatives(content)
        elif not include_images:
            # หากไม่ต้องการรูปภาพ ให้ใช้วิธีแสดงแบบอื่น
            content = self.replace_mermaid_with_alternatives(content)
        
        return content
    
    def replace_mermaid_with_alternatives(self, content: str) -> str:
        """แทนที่ Mermaid diagrams ด้วยวิธีแสดงแบบอื่น"""
        import re
        
        # หา Mermaid blocks
        mermaid_pattern = r'```mermaid\n(.*?)\n```'
        
        def replace_mermaid(match):
            diagram_content = match.group(1)
            
            # สร้าง HTML สำหรับแสดง Mermaid diagram
            html_content = f"""
<div class="mermaid-diagram">
    <h4>📊 Mermaid Diagram</h4>
    <div class="mermaid-code">
        <pre><code class="language-mermaid">{diagram_content}</code></pre>
    </div>
    <div class="mermaid-alternatives">
        <p><strong>💡 วิธีแสดงแผนภาพ:</strong></p>
        <ol>
            <li><strong>ใช้ Mermaid Live Editor:</strong> <a href="https://mermaid.live" target="_blank">https://mermaid.live</a></li>
            <li><strong>ใช้ VS Code:</strong> ติดตั้ง Mermaid Preview extension</li>
            <li><strong>ใช้ GitHub:</strong> GitHub จะแสดง Mermaid diagrams อัตโนมัติ</li>
            <li><strong>ใช้ Mermaid CLI:</strong> ติดตั้ง mermaid-cli และแปลงเป็นรูปภาพ</li>
        </ol>
        <details>
            <summary>📋 คัดลอกโค้ด Mermaid</summary>
            <textarea readonly style="width: 100%; height: 100px;">{diagram_content}</textarea>
        </details>
    </div>
</div>
"""
            return html_content
        
        # แทนที่ Mermaid blocks
        content = re.sub(mermaid_pattern, replace_mermaid, content, flags=re.DOTALL)
        
        return content
    
    def convert_to_html(self, content: str, title: str = "Document") -> str:
        """แปลง Markdown เป็น HTML"""
        processed_content = self.process_markdown(content)
        html_content = self.md.convert(processed_content)
        
        # สร้าง HTML template
        html_template = f"""
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #2c3e50;
            margin-top: 2em;
            margin-bottom: 1em;
        }}
        h1 {{
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 5px;
        }}
        code {{
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #3498db;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding: 10px 20px;
            background-color: #f8f9fa;
        }}
        .toc {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        
        /* Mermaid Diagram Styles */
        .mermaid-diagram {{
            border: 2px solid #e1e5e9;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            background-color: #f8f9fa;
        }}
        
        .mermaid-diagram h4 {{
            margin-top: 0;
            color: #0366d6;
            border-bottom: 1px solid #e1e5e9;
            padding-bottom: 10px;
        }}
        
        .mermaid-container {{
            background-color: white;
            border: 1px solid #e1e5e9;
            border-radius: 6px;
            padding: 15px;
            margin: 15px 0;
            overflow-x: auto;
        }}
        
        .mermaid {{
            text-align: center;
        }}
        
        .mermaid-code {{
            background-color: #f6f8fa;
            border: 1px solid #e1e5e9;
            border-radius: 6px;
            padding: 15px;
            margin: 15px 0;
        }}
        
        .mermaid-code pre {{
            margin: 0;
            overflow-x: auto;
        }}
        
        .mermaid-alternatives {{
            margin-top: 15px;
        }}
        
        .mermaid-alternatives ol {{
            margin: 10px 0;
        }}
        
        .mermaid-alternatives li {{
            margin: 5px 0;
        }}
        
        .mermaid-alternatives a {{
            color: #0366d6;
            text-decoration: none;
        }}
        
        .mermaid-alternatives a:hover {{
            text-decoration: underline;
        }}
        
        details {{
            margin-top: 15px;
        }}
        
        summary {{
            cursor: pointer;
            font-weight: bold;
            color: #0366d6;
        }}
        
        textarea {{
            font-family: 'Courier New', monospace;
            font-size: 12px;
            border: 1px solid #e1e5e9;
            border-radius: 4px;
            padding: 10px;
            resize: vertical;
        }}
    </style>
    <!-- Mermaid.js for interactive diagrams -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            themeVariables: {{
                primaryColor: '#3498db',
                primaryTextColor: '#2c3e50',
                primaryBorderColor: '#2980b9',
                lineColor: '#34495e',
                secondaryColor: '#ecf0f1',
                tertiaryColor: '#ffffff'
            }}
        }});
    </script>
</head>
<body>
    {html_content}
</body>
</html>
        """
        
        return html_template
    
    def cleanup(self):
        """ลบไฟล์ชั่วคราว"""
        if self.mermaid_processor:
            self.mermaid_processor.cleanup()


def main():
    """ฟังก์ชันหลักสำหรับ command line interface"""
    parser = argparse.ArgumentParser(
        description="Convert Markdown files with Mermaid diagrams to HTML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py input.md --output output.html
  python main.py input.md --title "My Document"
        """
    )
    
    parser.add_argument('input_file', help='Input Markdown file path')
    parser.add_argument('--output', '-o', 
                       help='Output HTML file path')
    parser.add_argument('--title', '-t',
                       default='Document',
                       help='Document title (default: Document)')
    parser.add_argument('--no-images', 
                       action='store_true',
                       help='Skip Mermaid diagram processing')
    
    args = parser.parse_args()
    
    # ตรวจสอบไฟล์อินพุต
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found")
        sys.exit(1)
    
    # สร้าง converter
    converter = MarkdownConverter()
    
    # ถ้าใช้ --no-images ให้ปิดการประมวลผล Mermaid
    if args.no_images:
        converter.mermaid_processor = None
        print("Skipping Mermaid diagram processing...")
    
    try:
        # อ่านไฟล์ Markdown
        content = converter.read_markdown_file(args.input_file)
        
        # กำหนดชื่อไฟล์เอาต์พุต
        base_name = Path(args.input_file).stem
        
        if not args.output:
            # สร้างชื่อไฟล์อัตโนมัติ
            args.output = f"{base_name}.html"
        
        # สร้างไฟล์ HTML
        html_content = converter.convert_to_html(content, args.title)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML created successfully: {args.output}")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    finally:
        converter.cleanup()


if __name__ == "__main__":
    main()
