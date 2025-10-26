# Visual Reference - YAML Diff Tool

## Application Layout

```
┌────────────────────────────────────────────────────────────────────────────┐
│                          YAML Diff Tool - Side-by-Side Comparison          │
├────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌─────────────────────────────────────────────────┐   │
│  │ Load File 1  │  │ /path/to/config_v1.yaml                         │   │
│  └──────────────┘  └─────────────────────────────────────────────────┘   │
│  ┌──────────────┐  ┌─────────────────────────────────────────────────┐   │
│  │ Load File 2  │  │ /path/to/config_v2.yaml                         │   │
│  └──────────────┘  └─────────────────────────────────────────────────┘   │
├────────────────────────────────────────────────────────────────────────────┤
│  Comparison Mode:  ┌──────────────┬──────────────┐  ┌─────────┐          │
│                    │ Side-by-Side │  Semantic    │  │ Compare │          │
│                    └──────────────┴──────────────┘  └─────────┘          │
├────────────────────────────────────────────────────────────────────────────┤
│  File 1: config_v1.yaml          │  File 2: config_v2.yaml               │
├──────────────────────────────────┼───────────────────────────────────────┤
│                                  │                                       │
│   1 | # Configuration            │   1 | # Configuration                │
│   2 | app:                       │   2 | app:                           │
│   3 |   name: "MyApp"            │   3 |   name: "MyApp"                │
│   4 |   version: "1.0.0"      🟡 │   4 |   version: "1.1.0"          🟡│
│   5 |   env: "production"     🟡 │   5 |   env: "staging"            🟡│
│     |                         ⚪ │   6 |   region: "us-east-1"       🟢│
│   6 | database:                  │   7 | database:                      │
│   7 |   host: "localhost"     🟡 │   8 |   host: "db.example.com"    🟡│
│   8 |   port: 5432               │   9 |   port: 5432                   │
│   9 |   ssl: false            🔴 │     |                             ⚪│
│  10 | features:                  │  10 | features:                      │
│  11 |   - auth                   │  11 |   - auth                       │
│  12 |   - logging                │  12 |   - logging                    │
│     |                         ⚪ │  13 |   - monitoring              🟢│
│                                  │                                       │
│  [Scroll...]                     │  [Scroll...]                          │
└──────────────────────────────────┴───────────────────────────────────────┘
```

## Color Legend

### Side-by-Side Mode

| Color | Meaning | Example |
|-------|---------|---------|
| ⚪ **White/Normal** | Identical lines | `1 \| app:` |
| 🟡 **Yellow** | Changed content | `4 \| version: "1.0.0"` → `4 \| version: "1.1.0"` |
| 🔴 **Red** | Removed (left only) | `9 \| ssl: false` (no corresponding line on right) |
| 🟢 **Green** | Added (right only) | `6 \| region: "us-east-1"` (no corresponding line on left) |
| ⚪ **Gray** | Empty alignment | `     \|` (spaces for alignment) |

### Visual Examples

#### Example 1: Changed Line
```
Left:    4 | version: "1.0.0"     [Yellow Background]
Right:   4 | version: "1.1.0"     [Yellow Background]
```
Both sides show the line, both highlighted yellow to indicate change.

#### Example 2: Removed Line
```
Left:    9 | ssl: false           [Red Background]
Right:     |                      [Gray Background - Empty]
```
Left shows the removed line in red, right shows empty gray space.

#### Example 3: Added Line
```
Left:      |                      [Gray Background - Empty]
Right:  13 | - monitoring          [Green Background]
```
Right shows the new line in green, left shows empty gray space.

#### Example 4: Unchanged Lines
```
Left:    2 | app:                 [Normal - White Text]
Right:   2 | app:                 [Normal - White Text]
```
Both sides show identical content with normal white text.

## Semantic Mode Display

```
┌────────────────────────────────────────────────────────────────────────────┐
│  File 1: config_v1.yaml          │  File 2: config_v2.yaml               │
├──────────────────────────────────┴───────────────────────────────────────┤
│  === Semantic Differences (Order Ignored) ===                             │
│                                                                            │
│  {'dictionary_item_added': ["root['app']['region']"],                     │ 🟢
│   'dictionary_item_removed': ["root['database']['ssl']"],                 │ 🔴
│   'values_changed': {                                                      │ 🟡
│     "root['app']['version']": {                                            │
│       'old_value': '1.0.0',                                                │
│       'new_value': '1.1.0'                                                 │
│     },                                                                     │
│     "root['app']['env']": {                                                │
│       'old_value': 'production',                                           │
│       'new_value': 'staging'                                               │
│     }                                                                      │
│   },                                                                       │
│   'iterable_item_added': {                                                 │ 🟢
│     "root['features'][2]": 'monitoring'                                    │
│   }                                                                        │
│  }                                                                         │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

Note: In Semantic mode, the same diff appears in both panes.

## Interaction Patterns

### File Loading
```
[Before Loading]
  ┌──────────────┐  ┌─────────────────────────────────────┐
  │ Load File 1  │  │ (empty)                             │
  └──────────────┘  └─────────────────────────────────────┘

[After Loading]
  ┌──────────────┐  ┌─────────────────────────────────────┐
  │ Load File 1  │  │ /Users/me/yamldiff/test/config.yaml │
  └──────────────┘  └─────────────────────────────────────┘
```

### Mode Switching
```
  Comparison Mode:  ┌──────────────┬──────────────┐
                    │ Side-by-Side │  Semantic    │  ← Click to switch
                    └──────────────┴──────────────┘
                         ▲ Active
```

### Synchronized Scrolling
```
Scroll Wheel ↓
    │
    ├──→ Left Pane scrolls
    │
    └──→ Right Pane scrolls (synchronized)
```

## Real-World Examples

### Example 1: Configuration Update

**File**: `config_v1.yaml` vs `config_v2.yaml`

Visual representation:
```
LEFT (v1)                        RIGHT (v2)
app:                             app:
  version: "1.0.0"      🟡         version: "1.1.0"       🟡
  debug: false          🔴         [empty]                ⚪
                        ⚪         region: "us-east"      🟢
```

### Example 2: Reordered (Semantic Identical)

**File**: `config_v1.yaml` vs `config_reordered.yaml`

Side-by-Side shows many yellow lines (different order)
Semantic shows: "Files are semantically identical" ✓

### Example 3: Type Change

**File**: `types_original.yaml` vs `types_changed.yaml`

```
LEFT                             RIGHT
port: 8080 (int)      🟡         port: "8080" (string)  🟡

Semantic output:
type_changes: {
  "root['port']": {
    'old_type': int,
    'new_type': str,
    'old_value': 8080,
    'new_value': "8080"
  }
}
```

## Window Controls

```
┌─┬─────────────────────────────────────────┬─┐
│●│ YAML Diff Tool - Side-by-Side Comparison│×│  ← Title Bar
└─┴─────────────────────────────────────────┴─┘
 ▲                                           ▲
Close                                     Resize
```

Default size: 1400x800 (can be resized)

## Status Indicators

### Before Comparison
```
File 1                           File 2
[Empty gray panes]
```

### After Comparison - Files Identical
```
File 1: test.yaml                File 2: test.yaml
[White text throughout]
=== Files are identical ===
```

### After Comparison - Files Different
```
File 1: old.yaml                 File 2: new.yaml
[Mixed colors: white, yellow, red, green, gray]
```

### Error State
```
File 1: missing.yaml             File 2: missing.yaml
[Orange text]
Error: File not found.
```

## Tips for Visual Understanding

1. **Line Alignment**: Corresponding lines are always horizontally aligned
2. **Empty Spaces**: Gray bars (`     |`) help maintain alignment
3. **Line Numbers**: Help you jump to specific locations in original files
4. **Color Backgrounds**: More visible than just colored text
5. **Separator Bar**: Thin gray vertical line between panes

## Comparison with Other Tools

| Feature | YAML Diff Tool | Standard `diff` | VIMDIFF |
|---------|---------------|-----------------|---------|
| Side-by-Side | ✅ Yes | ❌ No (unified) | ✅ Yes |
| Color Highlighting | ✅ Background | ⚠️ Text only | ✅ Yes |
| Line Numbers | ✅ Yes | ⚠️ Optional | ✅ Yes |
| YAML-Aware | ✅ Semantic mode | ❌ No | ❌ No |
| GUI | ✅ Yes | ❌ Terminal | ❌ Terminal |
| Synchronized Scroll | ✅ Yes | N/A | ✅ Yes |

