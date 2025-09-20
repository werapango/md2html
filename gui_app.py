#!/usr/bin/env python3
"""
Markdown Converter GUI Application
แอปพลิเคชัน GUI สำหรับแปลงไฟล์ Markdown ที่มี Mermaid diagrams
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys
from pathlib import Path
import webbrowser

# Import จาก main.py
from main import MarkdownConverter


class MarkdownConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown Converter - แปลงไฟล์ Markdown")
        self.root.geometry("600x500")
        self.root.minsize(500, 400)
        
        # ตัวแปรสำหรับเก็บข้อมูล
        self.input_file = tk.StringVar()
        self.input_folder = tk.StringVar()
        self.output_file = tk.StringVar()
        self.document_title = tk.StringVar(value="Document")
        self.selected_format = tk.StringVar(value="html")
        self.include_images = tk.BooleanVar(value=True)
        self.input_mode = tk.StringVar(value="file")  # "file" or "folder"
        self.found_files = []  # รายการไฟล์ที่พบ
        
        # สร้าง converter
        self.converter = MarkdownConverter()
        
        self.create_widgets()
        
    def create_widgets(self):
        """สร้าง GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Markdown Converter", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input mode selection
        ttk.Label(main_frame, text="โหมดการทำงาน:").grid(row=1, column=0, sticky=tk.W, pady=5)
        mode_frame = ttk.Frame(main_frame)
        mode_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Radiobutton(mode_frame, text="ไฟล์เดียว", variable=self.input_mode, value="file", 
                       command=self.on_mode_change).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(mode_frame, text="โฟลเดอร์", variable=self.input_mode, value="folder", 
                       command=self.on_mode_change).pack(side=tk.LEFT)
        
        # Input file/folder selection
        ttk.Label(main_frame, text="ไฟล์/โฟลเดอร์:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.input_file, width=50).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(main_frame, text="เลือก", command=self.select_input).grid(row=2, column=2, pady=5)
        
        # File list (for folder mode)
        self.file_list_frame = ttk.LabelFrame(main_frame, text="ไฟล์ที่พบ", padding="5")
        self.file_list_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Create Treeview for file list
        self.file_tree = ttk.Treeview(self.file_list_frame, height=6, show="tree headings")
        self.file_tree["columns"] = ("size", "modified")
        self.file_tree.column("#0", width=300, minwidth=200)
        self.file_tree.column("size", width=80, minwidth=60)
        self.file_tree.column("modified", width=120, minwidth=100)
        
        self.file_tree.heading("#0", text="ชื่อไฟล์")
        self.file_tree.heading("size", text="ขนาด")
        self.file_tree.heading("modified", text="แก้ไขล่าสุด")
        
        # Scrollbar for file list
        file_scrollbar = ttk.Scrollbar(self.file_list_frame, orient="vertical", command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=file_scrollbar.set)
        
        self.file_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        file_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights for file list
        self.file_list_frame.columnconfigure(0, weight=1)
        self.file_list_frame.rowconfigure(0, weight=1)
        
        # Initially hide file list
        self.file_list_frame.grid_remove()
        
        # Output file selection
        ttk.Label(main_frame, text="ไฟล์ Output:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_file, width=50).grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(main_frame, text="เลือกไฟล์", command=self.select_output_file).grid(row=4, column=2, pady=5)
        
        # Document title
        ttk.Label(main_frame, text="ชื่อเอกสาร:").grid(row=5, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.document_title, width=50).grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Format selection (HTML only)
        ttk.Label(main_frame, text="รูปแบบ Output:").grid(row=6, column=0, sticky=tk.W, pady=5)
        format_frame = ttk.Frame(main_frame)
        format_frame.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(format_frame, text="HTML (เท่านั้น)", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        
        # Include images option
        ttk.Checkbutton(main_frame, text="รวม Mermaid diagrams", variable=self.include_images).grid(row=7, column=0, columnspan=3, sticky=tk.W, pady=10)
        
        # Convert button
        convert_button = ttk.Button(main_frame, text="แปลงไฟล์", command=self.convert_file)
        convert_button.grid(row=8, column=0, columnspan=3, pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="พร้อมใช้งาน")
        self.status_label.grid(row=10, column=0, columnspan=3, pady=5)
        
        # Help button
        help_button = ttk.Button(main_frame, text="ช่วยเหลือ", command=self.show_help)
        help_button.grid(row=11, column=0, columnspan=3, pady=10)
        
    def on_mode_change(self):
        """เมื่อเปลี่ยนโหมดการทำงาน"""
        if self.input_mode.get() == "folder":
            self.file_list_frame.grid()
            self.root.geometry("600x700")  # เพิ่มความสูง
        else:
            self.file_list_frame.grid_remove()
            self.root.geometry("600x500")  # ลดความสูง
            self.clear_file_list()
    
    def select_input(self):
        """เลือกไฟล์หรือโฟลเดอร์"""
        if self.input_mode.get() == "file":
            self.select_input_file()
        else:
            self.select_input_folder()
    
    def select_input_file(self):
        """เลือกไฟล์ Markdown"""
        filename = filedialog.askopenfilename(
            title="เลือกไฟล์ Markdown",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            # Auto-generate output filename
            self.auto_generate_output_filename()
    
    def select_input_folder(self):
        """เลือกโฟลเดอร์"""
        folder_path = filedialog.askdirectory(title="เลือกโฟลเดอร์ที่มีไฟล์ Markdown")
        if folder_path:
            self.input_folder.set(folder_path)
            self.input_file.set(folder_path)  # แสดงใน entry
            self.scan_markdown_files(folder_path)
    
    def scan_markdown_files(self, folder_path):
        """สแกนไฟล์ .md ในโฟลเดอร์"""
        try:
            self.found_files = []
            self.clear_file_list()
            
            # สแกนไฟล์ .md ทั้งหมดในโฟลเดอร์
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith('.md'):
                        file_path = os.path.join(root, file)
                        file_size = os.path.getsize(file_path)
                        file_mtime = os.path.getmtime(file_path)
                        
                        # แปลงขนาดไฟล์
                        if file_size < 1024:
                            size_str = f"{file_size} B"
                        elif file_size < 1024 * 1024:
                            size_str = f"{file_size // 1024} KB"
                        else:
                            size_str = f"{file_size // (1024 * 1024)} MB"
                        
                        # แปลงเวลาแก้ไข
                        import datetime
                        mtime_str = datetime.datetime.fromtimestamp(file_mtime).strftime("%Y-%m-%d %H:%M")
                        
                        # เพิ่มในรายการ
                        self.found_files.append({
                            'path': file_path,
                            'name': file,
                            'size': size_str,
                            'modified': mtime_str
                        })
            
            # แสดงใน Treeview
            for file_info in self.found_files:
                self.file_tree.insert("", "end", 
                                    text=file_info['name'],
                                    values=(file_info['size'], file_info['modified']))
            
            # อัปเดต status
            count = len(self.found_files)
            self.status_label.config(text=f"พบไฟล์ Markdown {count} ไฟล์")
            
        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถสแกนโฟลเดอร์ได้: {e}")
    
    def clear_file_list(self):
        """ล้างรายการไฟล์"""
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        self.found_files = []
    
    def select_output_file(self):
        """เลือกไฟล์ Output"""
        filename = filedialog.asksaveasfilename(
            title="บันทึกไฟล์ HTML",
            defaultextension=".html",
            filetypes=[
                ("HTML files", "*.html"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.output_file.set(filename)
    
    def auto_generate_output_filename(self):
        """สร้างชื่อไฟล์ output อัตโนมัติ"""
        input_path = self.input_file.get()
        if input_path:
            input_file = Path(input_path)
            output_name = f"{input_file.stem}.html"
            output_path = input_file.parent / output_name
            self.output_file.set(str(output_path))
    
    def convert_file(self):
        """แปลงไฟล์"""
        # ตรวจสอบข้อมูลที่จำเป็น
        if not self.input_file.get():
            messagebox.showerror("ข้อผิดพลาด", "กรุณาเลือกไฟล์หรือโฟลเดอร์")
            return
        
        if not os.path.exists(self.input_file.get()):
            messagebox.showerror("ข้อผิดพลาด", "ไฟล์หรือโฟลเดอร์ไม่พบ")
            return
        
        # เริ่มการแปลงใน thread แยก
        self.progress.start()
        self.status_label.config(text="กำลังแปลงไฟล์...")
        
        thread = threading.Thread(target=self.convert_thread)
        thread.daemon = True
        thread.start()
    
    def convert_thread(self):
        """Thread สำหรับการแปลงไฟล์"""
        try:
            if self.input_mode.get() == "file":
                # แปลงไฟล์เดียว
                self.convert_single_file()
            else:
                # แปลงหลายไฟล์
                self.convert_multiple_files()
            
            # แสดงผลสำเร็จ
            self.root.after(0, self.conversion_success)
            
        except Exception as e:
            self.root.after(0, lambda: self.conversion_error(str(e)))
    
    def convert_single_file(self):
        """แปลงไฟล์เดียว"""
        # อ่านไฟล์ Markdown
        with open(self.input_file.get(), 'r', encoding='utf-8') as f:
            content = f.read()
        
        # ตั้งค่า converter
        if not self.include_images.get():
            self.converter.mermaid_processor = None
        
        # แปลงเป็น HTML
        html_content = self.converter.convert_to_html(content, self.document_title.get())
        with open(self.output_file.get(), 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def convert_multiple_files(self):
        """แปลงหลายไฟล์"""
        if not self.found_files:
            raise Exception("ไม่พบไฟล์ Markdown ในโฟลเดอร์")
        
        # สร้างโฟลเดอร์ output
        output_dir = self.output_file.get()
        if not output_dir:
            output_dir = os.path.join(self.input_folder.get(), "html_output")
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # แปลงแต่ละไฟล์
        for i, file_info in enumerate(self.found_files):
            try:
                # อัปเดต progress
                progress_text = f"กำลังแปลงไฟล์ {i+1}/{len(self.found_files)}: {file_info['name']}"
                self.root.after(0, lambda text=progress_text: self.status_label.config(text=text))
                
                # อ่านไฟล์
                with open(file_info['path'], 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # ตั้งค่า converter
                if not self.include_images.get():
                    self.converter.mermaid_processor = None
                
                # สร้างชื่อไฟล์ output
                base_name = os.path.splitext(file_info['name'])[0]
                output_path = os.path.join(output_dir, f"{base_name}.html")
                
                # แปลงเป็น HTML
                html_content = self.converter.convert_to_html(content, base_name)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
            except Exception as e:
                print(f"Error converting {file_info['name']}: {e}")
                continue
        
        # อัปเดต output path สำหรับการแสดงผล
        self.output_file.set(output_dir)
    
    def conversion_success(self):
        """แสดงผลการแปลงสำเร็จ"""
        self.progress.stop()
        
        if self.input_mode.get() == "file":
            # แปลงไฟล์เดียว
            self.status_label.config(text="แปลงไฟล์สำเร็จ!")
            if messagebox.askyesno("สำเร็จ", "แปลงไฟล์ HTML สำเร็จ!\nต้องการเปิดไฟล์ในเบราว์เซอร์หรือไม่?"):
                try:
                    webbrowser.open(f"file://{os.path.abspath(self.output_file.get())}")
                except Exception as e:
                    messagebox.showwarning("คำเตือน", f"ไม่สามารถเปิดไฟล์ได้: {e}")
        else:
            # แปลงหลายไฟล์
            count = len(self.found_files)
            self.status_label.config(text=f"แปลงไฟล์สำเร็จ! ({count} ไฟล์)")
            if messagebox.askyesno("สำเร็จ", f"แปลงไฟล์ HTML สำเร็จ! ({count} ไฟล์)\nต้องการเปิดโฟลเดอร์ผลลัพธ์หรือไม่?"):
                try:
                    os.startfile(self.output_file.get())
                except Exception as e:
                    messagebox.showwarning("คำเตือน", f"ไม่สามารถเปิดโฟลเดอร์ได้: {e}")
    
    def conversion_error(self, error_message):
        """แสดงข้อผิดพลาด"""
        self.progress.stop()
        self.status_label.config(text="เกิดข้อผิดพลาด")
        messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการแปลงไฟล์:\n{error_message}")
    
    def show_help(self):
        """แสดงหน้าต่างช่วยเหลือ"""
        help_text = """
Markdown Converter - คู่มือการใช้งาน

โหมดการทำงาน:
1. ไฟล์เดียว - แปลงไฟล์ Markdown เดียว
2. โฟลเดอร์ - แปลงไฟล์ Markdown ทั้งหมดในโฟลเดอร์

การใช้งาน:
1. เลือกโหมดการทำงาน (ไฟล์เดียว หรือ โฟลเดอร์)
2. เลือกไฟล์หรือโฟลเดอร์ที่ต้องการแปลง
3. เลือกไฟล์ HTML ที่ต้องการบันทึก (สำหรับไฟล์เดียว)
4. ตั้งชื่อเอกสาร (ถ้าต้องการ)
5. เลือกว่าจะรวม Mermaid diagrams หรือไม่
6. กดปุ่ม "แปลงไฟล์"

หมายเหตุ:
- Mermaid diagrams จะแสดงเป็น interactive HTML
- ผลลัพธ์จะเป็นไฟล์ HTML ที่เปิดในเบราว์เซอร์ได้
- สำหรับโฟลเดอร์: จะสร้างโฟลเดอร์ "html_output" ในโฟลเดอร์ที่เลือก
- หากเกิดข้อผิดพลาด ให้ตรวจสอบไฟล์ Markdown
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("ช่วยเหลือ")
        help_window.geometry("500x400")
        
        text_widget = tk.Text(help_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)


def main():
    """ฟังก์ชันหลักสำหรับรัน GUI"""
    root = tk.Tk()
    app = MarkdownConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
