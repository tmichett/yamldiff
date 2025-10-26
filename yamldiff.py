import customtkinter as ctk
import yaml
import difflib
from deepdiff import DeepDiff
from tkinter import filedialog
from pprint import pformat
import os

class YamlDiffApp(ctk.CTk):
    """
    A graphical application to compare two YAML files side-by-side
    with visual diff highlighting similar to VIMDIFF.
    """
    
    def __init__(self):
        super().__init__()

        self.title("YAML Diff Tool - Side-by-Side Comparison")
        self.geometry("1400x800")

        # --- Class variables ---
        self.file1_path = ctk.StringVar()
        self.file2_path = ctk.StringVar()
        self.diff_mode = ctk.StringVar(value="Side-by-Side")

        # --- Configure grid layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- 1. File Selection Frame ---
        self.file_frame = ctk.CTkFrame(self)
        self.file_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.file_frame.grid_columnconfigure(1, weight=1)

        # File 1
        self.file1_btn = ctk.CTkButton(self.file_frame, text="Load File 1", command=lambda: self.load_file(self.file1_path))
        self.file1_btn.grid(row=0, column=0, padx=10, pady=5)
        self.file1_entry = ctk.CTkEntry(self.file_frame, textvariable=self.file1_path, state="readonly")
        self.file1_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # File 2
        self.file2_btn = ctk.CTkButton(self.file_frame, text="Load File 2", command=lambda: self.load_file(self.file2_path))
        self.file2_btn.grid(row=1, column=0, padx=10, pady=5)
        self.file2_entry = ctk.CTkEntry(self.file_frame, textvariable=self.file2_path, state="readonly")
        self.file2_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # --- 2. Control Frame ---
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=1, column=0, padx=10, pady=0, sticky="ew")
        self.control_frame.grid_columnconfigure(1, weight=1)

        self.mode_label = ctk.CTkLabel(self.control_frame, text="Comparison Mode:")
        self.mode_label.grid(row=0, column=0, padx=(10, 5), pady=10)

        self.mode_switch = ctk.CTkSegmentedButton(
            self.control_frame, 
            values=["Side-by-Side", "Semantic"],
            variable=self.diff_mode
        )
        self.mode_switch.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        self.compare_btn = ctk.CTkButton(self.control_frame, text="Compare", command=self.perform_diff, font=("", 14, "bold"))
        self.compare_btn.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        # --- 3. Diff Display Frame (Side-by-Side) ---
        self.diff_frame = ctk.CTkFrame(self)
        self.diff_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.diff_frame.grid_columnconfigure(0, weight=1)
        self.diff_frame.grid_columnconfigure(2, weight=1)
        self.diff_frame.grid_rowconfigure(1, weight=1)

        # Left file label
        self.left_label = ctk.CTkLabel(self.diff_frame, text="File 1", font=("", 14, "bold"))
        self.left_label.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="ew")

        # Right file label
        self.right_label = ctk.CTkLabel(self.diff_frame, text="File 2", font=("", 14, "bold"))
        self.right_label.grid(row=0, column=2, padx=5, pady=(0, 5), sticky="ew")

        # Left textbox
        self.left_box = ctk.CTkTextbox(self.diff_frame, wrap="none", font=("Courier New", 11))
        self.left_box.grid(row=1, column=0, padx=(0, 2), pady=0, sticky="nsew")

        # Separator
        self.separator = ctk.CTkFrame(self.diff_frame, width=2, fg_color="gray30")
        self.separator.grid(row=1, column=1, padx=2, pady=0, sticky="ns")

        # Right textbox
        self.right_box = ctk.CTkTextbox(self.diff_frame, wrap="none", font=("Courier New", 11))
        self.right_box.grid(row=1, column=2, padx=(2, 0), pady=0, sticky="nsew")

        # Bind scrolling to synchronize both textboxes
        self.left_box.bind("<MouseWheel>", self._on_mousewheel)
        self.right_box.bind("<MouseWheel>", self._on_mousewheel)
        
        # Configure color tags for both textboxes
        for textbox in [self.left_box, self.right_box]:
            textbox.tag_config("added", background="#1a4d1a", foreground="#90EE90")  # Green bg
            textbox.tag_config("removed", background="#4d1a1a", foreground="#FFB6C1")  # Red bg
            textbox.tag_config("changed", background="#4d4d1a", foreground="#FFFF99")  # Yellow bg
            textbox.tag_config("empty", background="#2d2d2d", foreground="#666666")  # Gray bg
            textbox.tag_config("normal", foreground="#E0E0E0")  # Normal text
            textbox.tag_config("header", foreground="#00FFFF")  # Cyan (bold not allowed in CustomTkinter)
            textbox.tag_config("error", foreground="orange")


    def _on_mousewheel(self, event):
        """Synchronize scrolling between both textboxes."""
        # Scroll both textboxes together
        self.left_box.yview_scroll(int(-1*(event.delta/120)), "units")
        self.right_box.yview_scroll(int(-1*(event.delta/120)), "units")
        return "break"  # Prevent default scrolling

    def load_file(self, path_var):
        """Opens a file dialog to select a YAML file."""
        filename = filedialog.askopenfilename(
            title="Select a YAML file",
            filetypes=(("YAML files", "*.yaml *.yml"), ("All files", "*.*"))
        )
        if filename:
            path_var.set(filename)

    def perform_diff(self):
        """The main function triggered by the 'Compare' button."""
        # Clear both textboxes
        self.left_box.configure(state="normal")
        self.right_box.configure(state="normal")
        self.left_box.delete("1.0", "end")
        self.right_box.delete("1.0", "end")

        path1 = self.file1_path.get()
        path2 = self.file2_path.get()
        mode = self.diff_mode.get()

        if not path1 or not path2:
            error_msg = "Error: Please select two files to compare."
            self.left_box.insert("end", error_msg, "error")
            self.right_box.insert("end", error_msg, "error")
            self.left_box.configure(state="disabled")
            self.right_box.configure(state="disabled")
            return

        try:
            with open(path1, 'r', encoding='utf-8') as f1:
                content1 = f1.read()
            
            with open(path2, 'r', encoding='utf-8') as f2:
                content2 = f2.read()

            # Update labels with filenames
            self.left_label.configure(text=f"File 1: {os.path.basename(path1)}")
            self.right_label.configure(text=f"File 2: {os.path.basename(path2)}")

            if mode == "Side-by-Side":
                self.show_side_by_side_diff(content1, content2)
            else:  # Semantic
                self.show_semantic_diff(content1, content2)

        except FileNotFoundError as e:
            error_msg = f"Error: File not found.\n{e}"
            self.left_box.insert("end", error_msg, "error")
            self.right_box.insert("end", error_msg, "error")
        except yaml.YAMLError as e:
            error_msg = f"Error: Could not parse YAML file.\n{e}"
            self.left_box.insert("end", error_msg, "error")
            self.right_box.insert("end", error_msg, "error")
        except Exception as e:
            error_msg = f"An unexpected error occurred:\n{e}"
            self.left_box.insert("end", error_msg, "error")
            self.right_box.insert("end", error_msg, "error")
        
        self.left_box.configure(state="disabled")
        self.right_box.configure(state="disabled")

    def show_side_by_side_diff(self, content1, content2):
        """Shows files side-by-side with highlighted differences like VIMDIFF."""
        lines1 = content1.splitlines()
        lines2 = content2.splitlines()
        
        # Use SequenceMatcher to find matching and different blocks
        matcher = difflib.SequenceMatcher(None, lines1, lines2)
        
        # Build aligned output with proper line numbers
        left_line_num = 1
        right_line_num = 1
        
        for opcode, i1, i2, j1, j2 in matcher.get_opcodes():
            if opcode == 'equal':
                # Lines are the same - show them normally
                for i in range(i1, i2):
                    left_text = f"{left_line_num:4d} | {lines1[i]}\n"
                    right_text = f"{right_line_num:4d} | {lines2[j1 + (i - i1)]}\n"
                    self.left_box.insert("end", left_text, "normal")
                    self.right_box.insert("end", right_text, "normal")
                    left_line_num += 1
                    right_line_num += 1
                    
            elif opcode == 'replace':
                # Lines in this block differ - be smart about changed vs added/removed
                left_lines = lines1[i1:i2]
                right_lines = lines2[j1:j2]
                left_count = len(left_lines)
                right_count = len(right_lines)
                
                # If equal counts and lines are similar, mark as changed
                # Otherwise, mark left as removed and right as added
                if left_count == right_count:
                    # Same number of lines - check if they're modifications or completely different
                    for k in range(left_count):
                        left_line = left_lines[k]
                        right_line = right_lines[k]
                        
                        # Check similarity - if they share some common structure, it's a change
                        # Otherwise treat as remove + add
                        similarity = difflib.SequenceMatcher(None, left_line, right_line).ratio()
                        
                        if similarity > 0.3:  # 30% similar -> it's a modification
                            left_text = f"{left_line_num:4d} | {left_line}\n"
                            right_text = f"{right_line_num:4d} | {right_line}\n"
                            self.left_box.insert("end", left_text, "changed")
                            self.right_box.insert("end", right_text, "changed")
                        else:  # Too different -> treat as remove + add
                            left_text = f"{left_line_num:4d} | {left_line}\n"
                            self.left_box.insert("end", left_text, "removed")
                            self.right_box.insert("end", "     | \n", "empty")
                            
                            self.left_box.insert("end", "     | \n", "empty")
                            right_text = f"{right_line_num:4d} | {right_line}\n"
                            self.right_box.insert("end", right_text, "added")
                        
                        left_line_num += 1
                        right_line_num += 1
                else:
                    # Different counts - treat as removes + adds
                    for k in range(left_count):
                        left_text = f"{left_line_num:4d} | {left_lines[k]}\n"
                        self.left_box.insert("end", left_text, "removed")
                        self.right_box.insert("end", "     | \n", "empty")
                        left_line_num += 1
                    
                    for k in range(right_count):
                        self.left_box.insert("end", "     | \n", "empty")
                        right_text = f"{right_line_num:4d} | {right_lines[k]}\n"
                        self.right_box.insert("end", right_text, "added")
                        right_line_num += 1
                        
            elif opcode == 'delete':
                # Lines only in left file - removed
                for i in range(i1, i2):
                    left_text = f"{left_line_num:4d} | {lines1[i]}\n"
                    self.left_box.insert("end", left_text, "removed")
                    self.right_box.insert("end", "     | \n", "empty")
                    left_line_num += 1
                    
            elif opcode == 'insert':
                # Lines only in right file - added
                for j in range(j1, j2):
                    self.left_box.insert("end", "     | \n", "empty")
                    right_text = f"{right_line_num:4d} | {lines2[j]}\n"
                    self.right_box.insert("end", right_text, "added")
                    right_line_num += 1
        
        # Add summary at the bottom
        if content1 == content2:
            summary = "\n=== Files are identical ==="
            self.left_box.insert("end", summary, "added")
            self.right_box.insert("end", summary, "added")

    def show_semantic_diff(self, content1, content2):
        """Shows files side-by-side with semantic comparison (order-agnostic)."""
        data1 = yaml.safe_load(content1)
        data2 = yaml.safe_load(content2)

        # DeepDiff with order ignored
        ddiff = DeepDiff(data1, data2, ignore_order=True, verbose_level=2)

        if not ddiff:
            # Files are semantically identical - show them side by side normally
            msg = "=== Files are SEMANTICALLY IDENTICAL (order ignored) ===\n\n"
            self.left_box.insert("end", msg, "added")
            self.right_box.insert("end", msg, "added")
            
            # Show the actual YAML content side by side
            lines1 = content1.splitlines()
            lines2 = content2.splitlines()
            
            max_lines = max(len(lines1), len(lines2))
            for i in range(max_lines):
                if i < len(lines1):
                    left_text = f"{i+1:4d} | {lines1[i]}\n"
                    self.left_box.insert("end", left_text, "normal")
                else:
                    self.left_box.insert("end", "     | \n", "empty")
                
                if i < len(lines2):
                    right_text = f"{i+1:4d} | {lines2[i]}\n"
                    self.right_box.insert("end", right_text, "normal")
                else:
                    self.right_box.insert("end", "     | \n", "empty")
            return
        
        # Files have semantic differences - show summary
        header = "=== SEMANTIC DIFFERENCES FOUND (order ignored) ===\n\n"
        self.left_box.insert("end", header, "header")
        self.right_box.insert("end", header, "header")
        
        # Build a readable summary
        summary_lines = []
        
        if 'dictionary_item_added' in ddiff:
            summary_lines.append("📗 ADDED KEYS:\n")
            for path in ddiff['dictionary_item_added']:
                summary_lines.append(f"  + {path}\n")
            summary_lines.append("\n")
        
        if 'dictionary_item_removed' in ddiff:
            summary_lines.append("📕 REMOVED KEYS:\n")
            for path in ddiff['dictionary_item_removed']:
                summary_lines.append(f"  - {path}\n")
            summary_lines.append("\n")
        
        if 'values_changed' in ddiff:
            summary_lines.append("📘 CHANGED VALUES:\n")
            for path, change in ddiff['values_changed'].items():
                old_val = change.get('old_value', 'N/A')
                new_val = change.get('new_value', 'N/A')
                summary_lines.append(f"  {path}\n")
                summary_lines.append(f"    OLD: {old_val}\n")
                summary_lines.append(f"    NEW: {new_val}\n")
            summary_lines.append("\n")
        
        if 'type_changes' in ddiff:
            summary_lines.append("📙 TYPE CHANGES:\n")
            for path, change in ddiff['type_changes'].items():
                old_type = change.get('old_type', 'N/A')
                new_type = change.get('new_type', 'N/A')
                summary_lines.append(f"  {path}\n")
                summary_lines.append(f"    OLD TYPE: {old_type}\n")
                summary_lines.append(f"    NEW TYPE: {new_type}\n")
            summary_lines.append("\n")
        
        if 'iterable_item_added' in ddiff:
            summary_lines.append("📗 ADDED LIST ITEMS:\n")
            for path, value in ddiff['iterable_item_added'].items():
                summary_lines.append(f"  {path} = {value}\n")
            summary_lines.append("\n")
        
        if 'iterable_item_removed' in ddiff:
            summary_lines.append("📕 REMOVED LIST ITEMS:\n")
            for path, value in ddiff['iterable_item_removed'].items():
                summary_lines.append(f"  {path} = {value}\n")
            summary_lines.append("\n")
        
        # Color code the summary
        for line in summary_lines:
            if line.startswith('📗') or line.startswith('  +'):
                tag = "added"
            elif line.startswith('📕') or line.startswith('  -'):
                tag = "removed"
            elif line.startswith('📘') or line.startswith('📙') or 'OLD:' in line or 'NEW:' in line:
                tag = "changed"
            else:
                tag = "normal"
            
            self.left_box.insert("end", line, tag)
            self.right_box.insert("end", line, tag)


if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme("blue") # Themes: "blue", "green", "dark-blue"
    
    app = YamlDiffApp()
    app.mainloop()
