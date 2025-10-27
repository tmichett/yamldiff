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
        
        self.normalize_btn = ctk.CTkButton(self.control_frame, text="Normalize & Compare", command=self.normalize_and_compare, font=("", 12))
        self.normalize_btn.grid(row=0, column=3, padx=10, pady=10, sticky="e")

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
                # Lines in this block differ - show side-by-side with appropriate coloring
                left_lines = lines1[i1:i2]
                right_lines = lines2[j1:j2]
                left_count = len(left_lines)
                right_count = len(right_lines)
                max_count = max(left_count, right_count)
                
                # Always show side-by-side, pad with empty lines as needed
                for k in range(max_count):
                    if k < left_count and k < right_count:
                        # Both sides have content - check similarity
                        left_line = left_lines[k]
                        right_line = right_lines[k]
                        similarity = difflib.SequenceMatcher(None, left_line, right_line).ratio()
                        
                        left_text = f"{left_line_num:4d} | {left_line}\n"
                        right_text = f"{right_line_num:4d} | {right_line}\n"
                        
                        if similarity > 0.3:  # Similar enough to be a modification
                            self.left_box.insert("end", left_text, "changed")
                            self.right_box.insert("end", right_text, "changed")
                        else:  # Too different - one removed, one added
                            self.left_box.insert("end", left_text, "removed")
                            self.right_box.insert("end", right_text, "added")
                        
                        left_line_num += 1
                        right_line_num += 1
                        
                    elif k < left_count:
                        # Only left has content - removed
                        left_text = f"{left_line_num:4d} | {left_lines[k]}\n"
                        self.left_box.insert("end", left_text, "removed")
                        self.right_box.insert("end", "     | \n", "empty")
                        left_line_num += 1
                        
                    else:
                        # Only right has content - added
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
        """Shows files side-by-side with semantic differences highlighted (order-agnostic)."""
        data1 = yaml.safe_load(content1)
        data2 = yaml.safe_load(content2)

        # DeepDiff with order ignored
        ddiff = DeepDiff(data1, data2, ignore_order=True, verbose_level=2)

        # Extract paths that have semantic differences
        changed_paths = set()
        
        if 'dictionary_item_added' in ddiff:
            for path in ddiff['dictionary_item_added']:
                changed_paths.add(self._extract_key_from_path(path))
        
        if 'dictionary_item_removed' in ddiff:
            for path in ddiff['dictionary_item_removed']:
                changed_paths.add(self._extract_key_from_path(path))
        
        if 'values_changed' in ddiff:
            for path in ddiff['values_changed']:
                changed_paths.add(self._extract_key_from_path(path))
        
        if 'type_changes' in ddiff:
            for path in ddiff['type_changes']:
                changed_paths.add(self._extract_key_from_path(path))
        
        if 'iterable_item_added' in ddiff:
            for path in ddiff['iterable_item_added']:
                changed_paths.add(self._extract_key_from_path(path))
        
        if 'iterable_item_removed' in ddiff:
            for path in ddiff['iterable_item_removed']:
                changed_paths.add(self._extract_key_from_path(path))
        
        # Show header
        if not ddiff:
            msg = "✅ Files are SEMANTICALLY IDENTICAL (keys/values match, order ignored)\n\n"
            self.left_box.insert("end", msg, "added")
            self.right_box.insert("end", msg, "added")
        else:
            msg = f"⚠️  Found {len(changed_paths)} semantic difference(s) (order ignored)\n\n"
            self.left_box.insert("end", msg, "changed")
            self.right_box.insert("end", msg, "changed")
        
        # Show the actual YAML content side by side with highlighting
        lines1 = content1.splitlines()
        lines2 = content2.splitlines()
        
        max_lines = max(len(lines1), len(lines2))
        for i in range(max_lines):
            # Determine if this line has a semantic change
            has_change = False
            if i < len(lines1):
                line1 = lines1[i]
                # Check if any changed path appears in this line
                for path in changed_paths:
                    if path and path in line1:
                        has_change = True
                        break
                
                left_text = f"{i+1:4d} | {line1}\n"
                tag = "changed" if (has_change and ddiff) else "normal"
                self.left_box.insert("end", left_text, tag)
            else:
                self.left_box.insert("end", "     | \n", "empty")
            
            has_change = False
            if i < len(lines2):
                line2 = lines2[i]
                # Check if any changed path appears in this line
                for path in changed_paths:
                    if path and path in line2:
                        has_change = True
                        break
                
                right_text = f"{i+1:4d} | {line2}\n"
                tag = "changed" if (has_change and ddiff) else "normal"
                self.right_box.insert("end", right_text, tag)
            else:
                self.right_box.insert("end", "     | \n", "empty")
    
    def _extract_key_from_path(self, path):
        """Extract the key name from a DeepDiff path like root['key']['subkey']."""
        import re
        # Extract all keys from the path
        keys = re.findall(r"\['([^']+)'\]", str(path))
        # Return the last (most specific) key
        return keys[-1] if keys else ""
    
    def _normalize_data(self, data):
        """Recursively normalize data: sort dict keys AND list items."""
        if isinstance(data, dict):
            # Sort dictionary by keys and recursively normalize values
            return {k: self._normalize_data(v) for k, v in sorted(data.items())}
        elif isinstance(data, list):
            # Sort list items (convert to string for comparison) and recursively normalize
            normalized_items = [self._normalize_data(item) for item in data]
            # Sort, handling both simple types and complex types
            try:
                return sorted(normalized_items, key=lambda x: str(x))
            except TypeError:
                # If items aren't comparable, just return as-is
                return normalized_items
        else:
            return data
    
    def normalize_and_compare(self):
        """Normalize both YAML files (sort keys AND lists, consistent formatting) and compare."""
        self.left_box.configure(state="normal")
        self.right_box.configure(state="normal")
        self.left_box.delete("1.0", "end")
        self.right_box.delete("1.0", "end")

        path1 = self.file1_path.get()
        path2 = self.file2_path.get()

        if not path1 or not path2:
            error_msg = "Error: Please select two files to compare."
            self.left_box.insert("end", error_msg, "error")
            self.right_box.insert("end", error_msg, "error")
            self.left_box.configure(state="disabled")
            self.right_box.configure(state="disabled")
            return

        try:
            with open(path1, 'r', encoding='utf-8') as f1:
                data1 = yaml.safe_load(f1)
            
            with open(path2, 'r', encoding='utf-8') as f2:
                data2 = yaml.safe_load(f2)

            # Update labels
            self.left_label.configure(text=f"File 1 (Normalized): {os.path.basename(path1)}")
            self.right_label.configure(text=f"File 2 (Normalized): {os.path.basename(path2)}")

            # Normalize: Sort BOTH dict keys AND list items recursively
            normalized_data1 = self._normalize_data(data1)
            normalized_data2 = self._normalize_data(data2)
            
            # Convert to YAML with consistent formatting
            normalized1 = yaml.dump(normalized_data1, sort_keys=True, default_flow_style=False, allow_unicode=True)
            normalized2 = yaml.dump(normalized_data2, sort_keys=True, default_flow_style=False, allow_unicode=True)

            # Show normalized comparison
            header = "=== NORMALIZED COMPARISON (sorted keys, consistent format) ===\n\n"
            self.left_box.insert("end", header, "header")
            self.right_box.insert("end", header, "header")

            # Now do a line-by-line diff on normalized content
            lines1 = normalized1.splitlines()
            lines2 = normalized2.splitlines()
            
            matcher = difflib.SequenceMatcher(None, lines1, lines2)
            
            left_line_num = 1
            right_line_num = 1
            
            for opcode, i1, i2, j1, j2 in matcher.get_opcodes():
                if opcode == 'equal':
                    for i in range(i1, i2):
                        left_text = f"{left_line_num:4d} | {lines1[i]}\n"
                        right_text = f"{right_line_num:4d} | {lines2[j1 + (i - i1)]}\n"
                        self.left_box.insert("end", left_text, "normal")
                        self.right_box.insert("end", right_text, "normal")
                        left_line_num += 1
                        right_line_num += 1
                        
                elif opcode == 'replace':
                    left_lines = lines1[i1:i2]
                    right_lines = lines2[j1:j2]
                    max_count = max(len(left_lines), len(right_lines))
                    
                    for k in range(max_count):
                        if k < len(left_lines) and k < len(right_lines):
                            similarity = difflib.SequenceMatcher(None, left_lines[k], right_lines[k]).ratio()
                            left_text = f"{left_line_num:4d} | {left_lines[k]}\n"
                            right_text = f"{right_line_num:4d} | {right_lines[k]}\n"
                            
                            if similarity > 0.3:
                                self.left_box.insert("end", left_text, "changed")
                                self.right_box.insert("end", right_text, "changed")
                            else:
                                self.left_box.insert("end", left_text, "removed")
                                self.right_box.insert("end", right_text, "added")
                            left_line_num += 1
                            right_line_num += 1
                        elif k < len(left_lines):
                            left_text = f"{left_line_num:4d} | {left_lines[k]}\n"
                            self.left_box.insert("end", left_text, "removed")
                            self.right_box.insert("end", "     | \n", "empty")
                            left_line_num += 1
                        else:
                            self.left_box.insert("end", "     | \n", "empty")
                            right_text = f"{right_line_num:4d} | {right_lines[k]}\n"
                            self.right_box.insert("end", right_text, "added")
                            right_line_num += 1
                            
                elif opcode == 'delete':
                    for i in range(i1, i2):
                        left_text = f"{left_line_num:4d} | {lines1[i]}\n"
                        self.left_box.insert("end", left_text, "removed")
                        self.right_box.insert("end", "     | \n", "empty")
                        left_line_num += 1
                        
                elif opcode == 'insert':
                    for j in range(j1, j2):
                        self.left_box.insert("end", "     | \n", "empty")
                        right_text = f"{right_line_num:4d} | {lines2[j]}\n"
                        self.right_box.insert("end", right_text, "added")
                        right_line_num += 1
            
            if normalized1 == normalized2:
                summary = "\n✅ Files are IDENTICAL when normalized"
                self.left_box.insert("end", summary, "added")
                self.right_box.insert("end", summary, "added")

        except Exception as e:
            error_msg = f"Error normalizing files:\n{e}"
            self.left_box.insert("end", error_msg, "error")
            self.right_box.insert("end", error_msg, "error")
        
        self.left_box.configure(state="disabled")
        self.right_box.configure(state="disabled")


if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme("blue") # Themes: "blue", "green", "dark-blue"
    
    app = YamlDiffApp()
    app.mainloop()
