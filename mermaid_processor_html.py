#!/usr/bin/env python3
"""
Mermaid Processor using pure HTML + Mermaid.js
ใช้ Mermaid.js library ใน HTML โดยตรง ไม่ต้องใช้ API หรือ mermaid-py
"""

import re
import tempfile
from pathlib import Path

class MermaidProcessorPy:
    """Mermaid processor ที่ใช้ Mermaid.js ใน HTML โดยตรง"""
    
    def __init__(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        print(f"MermaidProcessorPy (HTML) initialized. Temp directory: {self.temp_dir}")
        
    def replace_mermaid_with_images(self, content: str) -> str:
        """แทนที่ Mermaid diagrams ด้วย interactive HTML"""
        mermaid_pattern = r'```mermaid\n(.*?)\n```'
        
        def replace_mermaid(match):
            diagram_content = match.group(1)
            
            # สร้าง interactive HTML สำหรับ Mermaid diagram
            html_content = f"""
<div class="mermaid-diagram">
    <h4>📊 Mermaid Diagram</h4>
    <div class="mermaid-container">
        <div class="mermaid">
{diagram_content}
        </div>
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
        
        content = re.sub(mermaid_pattern, replace_mermaid, content, flags=re.DOTALL)
        return content
    
    def cleanup(self):
        """ลบไฟล์ชั่วคราว"""
        try:
            import shutil
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
                print(f"Cleaned up temp directory: {self.temp_dir}")
        except Exception as e:
            print(f"Error cleaning up temp directory: {e}")
    
    def create_mermaid_fallback(self, diagram_content: str) -> str:
        """สร้าง fallback HTML สำหรับ Mermaid diagram"""
        return f"""
<div class="mermaid-diagram">
    <h4>📊 Mermaid Diagram</h4>
    <div class="mermaid-container">
        <div class="mermaid">
{diagram_content}
        </div>
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
