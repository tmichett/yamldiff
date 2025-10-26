# YAML Diff Tool

A graphical side-by-side YAML comparison tool with visual diff highlighting similar to VIMDIFF.

![YAML Diff Tool](https://img.shields.io/badge/python-3.8+-blue.svg)

## Features

- **🔄 Side-by-Side Comparison**: View files side by side with synchronized scrolling
- **🎨 Visual Highlighting**: 
  - 🟢 **Green**: Added lines (only in right file)
  - 🔴 **Red**: Removed lines (only in left file)  
  - 🟡 **Yellow**: Changed lines (different between files)
  - ⚪ **Gray**: Empty spaces for alignment
- **🧠 Semantic Mode**: Compare YAML structure ignoring order differences
- **📊 Line Numbers**: Shows line numbers for easy reference
- **🖱️ Synchronized Scrolling**: Both panes scroll together

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd yamldiff
```

2. Create and activate virtual environment:
```bash
python -m venv myvenv
source myvenv/bin/activate  # On Windows: myvenv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python yamldiff.py
```

2. Click **"Load File 1"** and **"Load File 2"** to select YAML files

3. Choose comparison mode:
   - **Side-by-Side**: Line-by-line visual diff (like VIMDIFF)
   - **Semantic**: Structure-based comparison (ignores ordering)

4. Click **"Compare"** to view differences

## Test Files

The `test_files/` directory contains example YAML files demonstrating various comparison scenarios:

### Quick Start Examples

1. **Identical Files**: `identical_1.yaml` vs `identical_2.yaml`
   - Shows how the tool confirms matching files

2. **Reordering Test**: `config_v1.yaml` vs `config_reordered.yaml`
   - Side-by-Side: Shows many differences (different line order)
   - Semantic: Shows they're identical (same structure)

3. **Version Changes**: `config_v1.yaml` vs `config_v2.yaml`
   - Real-world configuration evolution with additions and modifications

4. **Type Changes**: `types_original.yaml` vs `types_changed.yaml`
   - Demonstrates type mismatch detection

5. **Complex Modifications**: `users_before.yaml` vs `users_after.yaml`
   - Nested changes, removed/added items

6. **Deployment Configs**: `deployment_dev.yaml` vs `deployment_prod.yaml`
   - Environment-specific differences

See `test_files/README.md` for detailed descriptions of all test scenarios.

## Comparison Modes

### Side-by-Side Mode
- Shows both files side by side with line numbers
- Highlights exact line differences
- Perfect for seeing what changed at the text level
- Similar to `vimdiff` or `meld`

### Semantic Mode
- Compares YAML structure, not text
- Ignores key/item ordering
- Shows logical differences (added/removed/changed values)
- Uses DeepDiff for intelligent comparison

## Requirements

- Python 3.8+
- customtkinter
- PyYAML
- deepdiff
- darkdetect

See `requirements.txt` for exact versions.

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
