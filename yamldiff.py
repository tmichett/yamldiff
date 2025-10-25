import customtkinter as ctk
import yaml
import difflib
from deepdiff import DeepDiff
from tkinter import filedialog
from pprint import pformat
import os

class YamlDiffApp(ctk.CTk):
    """
    A graphical application to compare two YAML files either line-by-line
    or semantically (key-based).
    """
    
    def __init__(self):
        super().__init__()

        self.title("YAML Diff Tool")
        self.geometry("900x750")

        # --- Class variables ---
        self.file1_path = ctk.StringVar()
        self.file2_path = ctk.StringVar()
        self.diff_mode = ctk.StringVar(value="Line-by-Line")

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
            values=["Line-by-Line", "Key-Based"],
            variable=self.diff_mode
        )
        self.mode_switch.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        self.compare_btn = ctk.CTkButton(self.control_frame, text="Compare", command=self.perform_diff, font=("", 14, "bold"))
        self.compare_btn.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        # --- 3. Result Textbox ---
        self.result_box = ctk.CTkTextbox(self, wrap="none", font=("Courier New", 12))
        self.result_box.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Configure color tags for the textbox
        self.result_box.tag_config("added", foreground="#00C000") # Green
        self.result_box.tag_config("removed", foreground="#FF4040") # Red
        self.result_box.tag_config("header", foreground="#00FFFF") # Cyan
        self.result_box.tag_config("error", foreground="orange")


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
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", "end")

        path1 = self.file1_path.get()
        path2 = self.file2_path.get()
        mode = self.diff_mode.get()

        if not path1 or not path2:
            self.result_box.insert("end", "Error: Please select two files to compare.", "error")
            self.result_box.configure(state="disabled")
            return

        try:
            with open(path1, 'r', encoding='utf-8') as f1:
                content1 = f1.read()
            
            with open(path2, 'r', encoding='utf-8') as f2:
                content2 = f2.read()

            if mode == "Line-by-Line":
                self.run_line_diff(content1, content2, path1, path2)
            else: # Key-Based
                self.run_key_diff(content1, content2)

        except FileNotFoundError as e:
            self.result_box.insert("end", f"Error: File not found.\n{e}", "error")
        except yaml.YAMLError as e:
            self.result_box.insert("end", f"Error: Could not parse YAML file.\n{e}", "error")
        except Exception as e:
            self.result_box.insert("end", f"An unexpected error occurred:\n{e}", "error")
        
        self.result_box.configure(state="disabled")

    def run_line_diff(self, content1, content2, path1, path2):
        """Performs a line-by-line diff and inserts colored output."""
        self.result_box.insert("end", "Showing Line-by-Line (Direct) Diff:\n\n", "header")
        
        lines1 = content1.splitlines()
        lines2 = content2.splitlines()
        
        # Get file names for the diff header
        file1_name = os.path.basename(path1)
        file2_name = os.path.basename(path2)

        diff = difflib.unified_diff(
            lines1, 
            lines2, 
            fromfile=file1_name, 
            tofile=file2_name, 
            lineterm=''
        )

        diff_lines = list(diff)
        if not diff_lines:
            self.result_box.insert("end", "Files are identical (line-by-line).", "added")
            return

        for line in diff_lines:
            if line.startswith('+++') or line.startswith('---'):
                self.result_box.insert("end", line + '\n', "header")
            elif line.startswith('@@'):
                self.result_box.insert("end", line + '\n', "header")
            elif line.startswith('+'):
                self.result_box.insert("end", line + '\n', "added")
            elif line.startswith('-'):
                self.result_box.insert("end", line + '\n', "removed")
            else:
                self.result_box.insert("end", line + '\n')

    def run_key_diff(self, content1, content2):
        """Performs a semantic, key-based diff and inserts the result."""
        self.result_box.insert("end", "Showing Key-Based (Semantic) Diff (Order Ignored):\n\n", "header")
        
        data1 = yaml.safe_load(content1)
        data2 = yaml.safe_load(content2)

        # DeepDiff is excellent for this. ignore_order=True handles 
        # differing list orders and, by default, dict key order.
        ddiff = DeepDiff(data1, data2, ignore_order=True, verbose_level=0)

        if not ddiff:
            self.result_box.insert("end", "Files are semantically identical (keys/values match).", "added")
            return
        
        # Format the DeepDiff output for readability
        pretty_diff = pformat(ddiff, indent=2)
        
        # We can do basic coloring for the key-based diff too
        for line in pretty_diff.splitlines():
            if "'values_changed'" in line or "'type_changes'" in line:
                self.result_box.insert("end", line + '\n', "error")
            elif "'dictionary_item_added'" in line or "'iterable_item_added'" in line:
                self.result_box.insert("end", line + '\n', "added")
            elif "'dictionary_item_removed'" in line or "'iterable_item_removed'" in line:
                self.result_box.insert("end", line + '\n', "removed")
            else:
                 self.result_box.insert("end", line + '\n')


if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme("blue") # Themes: "blue", "green", "dark-blue"
    
    app = YamlDiffApp()
    app.mainloop()
