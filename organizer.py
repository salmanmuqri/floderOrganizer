import os
import shutil
import logging
from typing import Dict, List, Optional
import tkinter as tk
from tkinter import filedialog, messagebox

class FileOrganizer:
    def __init__(self, source_dir: Optional[str] = None):
        
        self.source_dir = source_dir
        self.log_file = None
        self.moved_files: Dict[str, str] = {}
        self.created_folders: List[str] = []
        
        self.category_rules = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
            'Videos': ['.mp4', '.avi', '.mov', '.mkv', '.wmv'],
            'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.pptx'],
            'Music': ['.mp3', '.wav', '.flac', '.aac'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'Codes': ['.py', '.java', '.c', '.cpp', '.html', '.css', '.js', '.php', '.sql', '.json', '.ts', '.sh', '.bat']
        }
    
    def setup_logging(self, directory: str):
        
        log_path = os.path.join(directory, 'organization_log.txt')
        logging.basicConfig(filename=log_path, 
                            level=logging.INFO, 
                            format='%(asctime)s - %(message)s')
        self.log_file = log_path
    
    def categorize_file(self, filename: str) -> str:
        
        file_ext = os.path.splitext(filename)[1].lower()
        for category, extensions in self.category_rules.items():
            if file_ext in extensions:
                return category
        return 'Other'
    
    def organize_files(self, custom_rules: Optional[Dict[str, List[str]]] = None):
        
        if not self.source_dir or not os.path.isdir(self.source_dir):
            raise ValueError("Invalid source directory")
        
        self.setup_logging(self.source_dir)
        
        if custom_rules:
            self.category_rules.update(custom_rules)
        
        for category in self.category_rules.keys():
            category_path = os.path.join(self.source_dir, category)
            os.makedirs(category_path, exist_ok=True)
            self.created_folders.append(category_path)
        
        for filename in os.listdir(self.source_dir):
            filepath = os.path.join(self.source_dir, filename)
            
            if os.path.isdir(filepath) or filename == 'organization_log.txt':
                continue
            
            category = self.categorize_file(filename)
            dest_path = os.path.join(self.source_dir, category, filename)
            
            try:
                shutil.move(filepath, dest_path)
                self.moved_files[filepath] = dest_path
                logging.info(f'Moved {filename} to {category} folder')
            except Exception as e:
                logging.error(f'Error moving {filename}: {e}')
    
    def undo_organization(self):
    
        if not self.source_dir:
            raise ValueError("No source directory set")
        
        for original, current in self.moved_files.items():
            try:
                shutil.move(current, original)
                logging.info(f'Restored {os.path.basename(current)} to original location')
            except Exception as e:
                logging.error(f'Error restoring {os.path.basename(current)}: {e}')
        
        for folder in self.created_folders:
            try:
                shutil.rmtree(folder, ignore_errors=True)
                logging.info(f'Removed folder {folder}')
            except Exception as e:
                logging.error(f'Error removing folder {folder}: {e}')
        
        self.moved_files.clear()
        self.created_folders.clear()
    
    def create_gui(self):

        # GuiWalaOption
        root = tk.Tk()
        root.title("File Organizer")
        root.geometry("400x300")
        
        def select_directory_and_organize():
            directory = filedialog.askdirectory()
            if directory:
                try:
                    self.source_dir = directory
                    self.organize_files()
                    messagebox.showinfo("Success", "Files organized successfully!")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        def select_directory_and_undo():
            directory = filedialog.askdirectory()
            if directory:
                try:
                    self.source_dir = directory
                    self.undo_organization()
                    messagebox.showinfo("Success", "Organization undone!")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        
        select_btn = tk.Button(root, text="Organize Directory", command=select_directory_and_organize)
        select_btn.pack(pady=20)
        
        undo_btn = tk.Button(root, text="Undo Organization", command=select_directory_and_undo)
        undo_btn.pack(pady=20)
        
        root.mainloop()

def main():
    
    # CliWalaOption
    import argparse
    
    parser = argparse.ArgumentParser(description='File Organizer')
    parser.add_argument('--dir', help='Directory to organize')
    parser.add_argument('--gui', action='store_true', help='Launch GUI')
    
    args = parser.parse_args()
    
    organizer = FileOrganizer()
    
    if args.gui:
        organizer.create_gui()
    elif args.dir:
        organizer.source_dir = args.dir
        organizer.organize_files()
    else:
        print("Please provide a directory or use --gui")

if __name__ == "__main__":
    main()