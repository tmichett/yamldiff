# Changelog

## Version 2.0 - Side-by-Side Visual Diff (Current)

### Major Changes
- **Complete UI Redesign**: Replaced single-pane unified diff with true side-by-side comparison
- **VIMDIFF-style Layout**: Both files displayed side by side with synchronized scrolling
- **Enhanced Visual Highlighting**:
  - 🟢 Green background: Lines added (only in right file)
  - 🔴 Red background: Lines removed (only in left file)
  - 🟡 Yellow background: Lines changed (different content)
  - ⚪ Gray background: Empty spaces for alignment
- **Line Numbers**: Each line now shows its line number for easy reference
- **Synchronized Scrolling**: Mouse wheel scrolls both panes together
- **Renamed Modes**:
  - "Line-by-Line" → "Side-by-Side"
  - "Key-Based" → "Semantic"

### Technical Improvements
- Uses `difflib.SequenceMatcher` for intelligent line matching
- Proper alignment of added/removed/changed blocks
- Background colors instead of just foreground colors for better visibility
- Larger default window size (1400x800) to accommodate dual panes
- Dynamic filename labels showing which files are being compared

### Features Preserved
- File selection dialogs
- YAML parsing and validation
- Semantic comparison with DeepDiff (order-agnostic)
- Error handling for missing files and invalid YAML
- Dark mode support via CustomTkinter

## Version 1.0 - Original Unified Diff

### Features
- Single-pane unified diff output
- Line-by-line comparison using `difflib.unified_diff`
- Key-based semantic comparison using DeepDiff
- Basic color coding (+ and - lines)
- File selection via dialogs

### Limitations (Addressed in v2.0)
- ❌ No visual alignment between files
- ❌ Hard to see context of changes
- ❌ Traditional diff format not intuitive for all users
- ❌ No line numbers
- ❌ Limited visual highlighting

---

## Migration Notes

If you're familiar with the old version:
- The functionality is the same, just presented differently
- Test files work exactly the same way
- All comparison logic is preserved
- The semantic/key-based mode still uses DeepDiff with order-agnostic comparison

