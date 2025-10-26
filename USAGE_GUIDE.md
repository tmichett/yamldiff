# YAML Diff Tool - Usage Guide

## Quick Start

1. **Launch the application**:
   ```bash
   python yamldiff.py
   ```

2. **Load files to compare**:
   - Click "Load File 1" button → Select your first YAML file
   - Click "Load File 2" button → Select your second YAML file

3. **Choose comparison mode**:
   - **Side-by-Side**: Visual line-by-line comparison (default)
   - **Semantic**: Structure-based comparison ignoring order

4. **Click "Compare"** to see the differences

## Understanding the Display

### Side-by-Side Mode

The display shows both files next to each other with color-coded highlighting:

```
┌─────────────────────────────┬─────────────────────────────┐
│ File 1: config_v1.yaml      │ File 2: config_v2.yaml      │
├─────────────────────────────┼─────────────────────────────┤
│   1 | app:                  │   1 | app:                  │ ← Same (white)
│   2 |   version: "1.0.0"    │   2 |   version: "1.1.0"    │ ← Changed (yellow)
│   3 |   debug: false        │     |                       │ ← Removed (red)
│     |                       │   3 |   region: "us-east"   │ ← Added (green)
└─────────────────────────────┴─────────────────────────────┘
```

#### Color Guide:
- **White text**: Unchanged lines (identical in both files)
- **Yellow background**: Changed lines (different content)
- **Red background**: Removed lines (only in left file)
- **Green background**: Added lines (only in right file)
- **Gray background**: Empty alignment spaces

#### Line Numbers:
- Format: `LINE_NUMBER | content`
- Empty lines show as `     |` (5 spaces for alignment)
- Line numbers help you locate changes in the original files

### Semantic Mode

This mode compares the YAML structure rather than the text:

```
=== Semantic Differences (Order Ignored) ===

{'values_changed': {"root['app']['version']": {
    'old_value': '1.0.0',
    'new_value': '1.1.0'
  }},
 'dictionary_item_added': {"root['app']['region']": 'us-east'},
 'dictionary_item_removed': {"root['app']['debug']"}
}
```

**Use Semantic mode when**:
- Files might have different key/item ordering
- You want to see what actually changed in the data structure
- Order doesn't matter (e.g., dictionary keys, unordered lists)

**Key indicators**:
- `values_changed`: Values that are different (yellow)
- `dictionary_item_added`: New keys/fields (green)
- `dictionary_item_removed`: Deleted keys/fields (red)
- `type_changes`: Data type mismatches (yellow)

## Navigation

- **Mouse Wheel**: Scroll both panes together (synchronized)
- **Horizontal Scroll**: Files don't wrap, use horizontal scrollbar for long lines
- **Text Selection**: You can select and copy text from either pane

## Common Use Cases

### 1. Configuration Changes
**Scenario**: Compare config before and after deployment

**Best Mode**: Side-by-Side
- Shows exact changes with context
- Easy to spot what was modified
- Great for code reviews

**Example**:
```bash
# Load config_v1.yaml and config_v2.yaml
# Choose "Side-by-Side"
# Click "Compare"
```

### 2. Reordered Files
**Scenario**: Files with same content but different ordering

**Best Mode**: Semantic
- Side-by-Side will show many "changes" due to reordering
- Semantic will show "Files are semantically identical"

**Example**:
```bash
# Load config_v1.yaml and config_reordered.yaml
# Choose "Semantic"
# Result: "Files are semantically identical"
```

### 3. Type Checking
**Scenario**: Ensure data types are correct

**Best Mode**: Semantic
- Detects type changes (string vs int, etc.)
- Shows `type_changes` section

**Example**:
```bash
# Load types_original.yaml and types_changed.yaml
# Choose "Semantic"
# See type_changes in output
```

### 4. Complex Nested Structures
**Scenario**: Deep YAML with nested objects and arrays

**Best Mode**: Both
- Side-by-Side for visual overview
- Semantic for precise path-based differences

## Tips and Tricks

### Tip 1: Start with Identical Files
Load two identical files to see how the tool confirms they match:
- Side-by-Side: All white text
- Semantic: "Files are semantically identical"

### Tip 2: Understanding Empty Lines
Gray lines (`     |`) represent alignment spaces where one file has content and the other doesn't.

### Tip 3: File Path Display
The labels show filenames being compared:
- Before comparison: "File 1" and "File 2"
- After comparison: "File 1: filename.yaml" and "File 2: filename.yaml"

### Tip 4: Long Lines
Files with very long lines won't wrap. Use the horizontal scrollbar to see the full content.

### Tip 5: Switch Modes
You can switch between Side-by-Side and Semantic without reloading files. Just select a different mode and click "Compare" again.

## Keyboard Shortcuts

- **Ctrl/Cmd + O**: Not implemented (use buttons)
- **Mouse Wheel**: Scroll both panes
- **Ctrl/Cmd + C**: Copy selected text

## Troubleshooting

### "Error: Could not parse YAML file"
- One or both files contain invalid YAML syntax
- Check for proper indentation, quotes, and structure
- Use a YAML validator to find the syntax error

### Files appear identical but show differences
- You might be in Side-by-Side mode with reordered content
- Try Semantic mode to see if they're structurally identical

### Scrolling is out of sync
- This is a known limitation with manual scrollbar dragging
- Use mouse wheel for synchronized scrolling
- Click in a pane to focus it before scrolling

### Colors look wrong
- Check your system dark/light mode settings
- The app adapts to system appearance mode
- Colors are optimized for dark mode

## Test Files

The `test_files/` directory contains example files:

| File Pair | Purpose | Recommended Mode |
|-----------|---------|------------------|
| `identical_1.yaml` vs `identical_2.yaml` | Verify matching | Either |
| `config_v1.yaml` vs `config_reordered.yaml` | Test ordering | Semantic |
| `config_v1.yaml` vs `config_v2.yaml` | Version changes | Side-by-Side |
| `types_original.yaml` vs `types_changed.yaml` | Type checking | Semantic |
| `users_before.yaml` vs `users_after.yaml` | Complex changes | Both |
| `deployment_dev.yaml` vs `deployment_prod.yaml` | Environment configs | Side-by-Side |

See `test_files/README.md` for detailed descriptions.

## Advanced Usage

### Comparing Non-YAML Files
While designed for YAML, the Side-by-Side mode works with any text file. Semantic mode requires valid YAML.

### Large Files
The tool handles large files well, but very large files (>10,000 lines) may take a moment to process.

### Custom Color Themes
The application uses CustomTkinter themes. You can modify the color theme in the code:
```python
ctk.set_default_color_theme("blue")  # or "green", "dark-blue"
```

