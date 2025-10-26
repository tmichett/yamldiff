# YAML Diff Test Files

This directory contains test YAML files to demonstrate the YAML Diff Tool's comparison capabilities.

## Test File Pairs

### 1. Configuration Files - Version Comparison
**Files:** `config_v1.yaml` vs `config_v2.yaml`

**Demonstrates:**
- Added fields (region, ssl_enabled, max_connections, admin server)
- Modified values (version, environment, host, password, timeout, retry_attempts, debug_mode, api port)
- Added list items (monitoring feature)

**Best Mode:** Both modes show different aspects
- Side-by-Side: Shows exact changes with visual alignment
- Semantic: Shows structural differences clearly

### 2. Configuration Files - Reordering Test
**Files:** `config_v1.yaml` vs `config_reordered.yaml`

**Demonstrates:**
- **Side-by-Side:** Shows many differences due to reordering
- **Semantic:** Shows files are semantically identical despite different order

**Best Mode:** Semantic (proves they're the same despite ordering)

### 3. User Database - Modifications
**Files:** `users_before.yaml` vs `users_after.yaml`

**Demonstrates:**
- Modified nested values (email, role)
- Removed items (charlie user)
- Added items (diana user, moderators group)
- Array modifications

**Best Mode:** Semantic for clear structural changes

### 4. Type Changes
**Files:** `types_original.yaml` vs `types_changed.yaml`

**Demonstrates:**
- Type changes (int→string, bool→string, array→string, object→string, int→float)
- DeepDiff's ability to detect type mismatches

**Best Mode:** Semantic (will show type_changes)

### 5. Identical Files
**Files:** `identical_1.yaml` vs `identical_2.yaml`

**Demonstrates:**
- Files that are completely identical
- Both modes should report "no differences"

**Best Mode:** Either (both show no differences)

### 6. Deployment Configurations
**Files:** `deployment_dev.yaml` vs `deployment_prod.yaml`

**Demonstrates:**
- Environment-specific configurations
- Scaled resources (replicas, memory, CPU)
- Added sections (annotations, health probes)
- Different values for environment variables

**Best Mode:** Both modes provide useful insights

## Usage Tips

1. **Start with identical files** to see how the tool confirms matches
2. **Try the reordered config** to understand the difference between modes
3. **Use type changes** to see how semantic comparison detects type mismatches
4. **Compare versions** to see real-world configuration evolution

## Testing Order Recommendation

1. `identical_1.yaml` vs `identical_2.yaml` - Baseline (no differences)
2. `config_v1.yaml` vs `config_reordered.yaml` - Order differences
3. `config_v1.yaml` vs `config_v2.yaml` - Version changes
4. `types_original.yaml` vs `types_changed.yaml` - Type changes
5. `users_before.yaml` vs `users_after.yaml` - Complex modifications
6. `deployment_dev.yaml` vs `deployment_prod.yaml` - Real-world example

