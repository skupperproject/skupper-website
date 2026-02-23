# MkDocs Integration Plan for Skupper Website

## Overview
Integrate MkDocs Material to provide enhanced sidebar navigation for documentation at `https://skupper.io/docs/` while preserving the existing Transom-based site structure.

## Current Situation
- **Problem**: Transom and MkDocs both want to process files in `input/docs/`
- **Conflict**: `input/docs/index.md` (MkDocs) vs `input/docs/index.html.in` (Transom)
- **Transom limitation**: `ignored_file_patterns` only matches filenames, not directory paths

## Proposed Solution: Rename Directories

### New Directory Structure
```
skupper-website/
├── doc-input/                # RENAMED: Transom source (main site)
│   ├── index.md
│   ├── main.css
│   ├── commands/
│   ├── concepts/
│   ├── community/
│   ├── examples/
│   ├── releases/
│   ├── resources/
│   ├── start/
│   └── v1/                   # V1 docs (preserved)
│       └── docs/
├── input/                    # REPURPOSED: MkDocs source directory
│   └── docs/                 # MkDocs content (already here!)
│       ├── index.md
│       ├── overview/
│       ├── install/
│       ├── kube-cli/
│       ├── kube-yaml/
│       ├── system-cli/
│       ├── system-yaml/
│       ├── console/
│       ├── troubleshooting/
│       └── api-docs/
├── output/                   # Build output
│   ├── index.html            # From Transom
│   ├── v1/                   # From Transom (preserved)
│   └── docs/                 # From MkDocs (overwrites)
└── mkdocs.yml
```

### Why This Approach?

✅ **Minimal changes**: MkDocs already expects `input/docs/` structure  
✅ **Clear naming**: `doc-input` = Transom source, `input` = MkDocs source  
✅ **No config changes**: mkdocs.yml stays as `docs_dir: input/docs`  
✅ **V1 preserved**: Moves with `doc-input/v1/`  

### Build Process
1. **Stage 1 - Transom**: `./plano render`
   - Processes `doc-input/` → `output/`
   - Generates entire site including placeholder for `/docs/`
   - V1 docs remain untouched

2. **Stage 2 - MkDocs**: `mkdocs build`
   - Processes `input/docs/` → `output/docs/`
   - Overwrites only the `/docs/` directory
   - Adds Material theme with sidebar navigation

3. **Combined**: `./plano render_all`
   - Runs both stages in sequence
   - Final output has Transom site + MkDocs docs

### Configuration Changes

#### .plano.py
```python
# Update input_dir reference
input_dir = "doc-input"  # Changed from "input"

@command
def render():
    """Render the site using Transom"""
    run(f"transom render {input_dir} output")

@command
def render_docs():
    """Render documentation using MkDocs"""
    run("mkdocs build")

@command  
def render_all():
    """Render entire site (Transom + MkDocs)"""
    render()      # Transom first
    render_docs() # MkDocs second (overwrites /docs/)
```

#### config/transom.py
```python
# Update any hardcoded "input" references if needed
# Most likely no changes needed as Transom gets input_dir from command
```

#### mkdocs.yml
```yaml
# NO CHANGES NEEDED!
docs_dir: input/docs
site_dir: output/docs
use_directory_urls: false
```

### Migration Steps

1. **Rename Transom input directory**:
   ```bash
   git mv input doc-input
   ```

2. **Move MkDocs files back to input/docs**:
   ```bash
   mkdir -p input/docs
   mv doc-input/docs/* input/docs/
   # Remove now-empty doc-input/docs/
   rmdir doc-input/docs
   ```

3. **Update .plano.py**:
   - Change `input_dir` references to `doc-input`
   - Update `render()` command

4. **Update any other references**:
   - Check `config/transom.py` for hardcoded paths
   - Check `.gitignore` if it references `input/`
   - Check GitHub Actions workflow
   - Check Netlify config

5. **Test build**:
   ```bash
   ./plano render_all
   ```

6. **Verify**:
   - Main site works: `output/index.html`
   - V1 docs preserved: `output/v1/docs/`
   - V2 docs with sidebar: `output/docs/index.html`

## Benefits

✅ **Clean separation**: Transom uses `doc-input/`, MkDocs uses `input/`  
✅ **Minimal config changes**: mkdocs.yml unchanged  
✅ **Clear ownership**: Each tool has its own source directory  
✅ **V1 preservation**: V1 docs move with Transom content  
✅ **Sidebar navigation**: MkDocs Material provides rich navigation  
✅ **Brand consistency**: Custom theme reuses Skupper header/footer/CSS  
✅ **Intuitive naming**: `doc-input` clearly indicates Transom source  

## Alternative Considered

**Move MkDocs to `docs/`**: Would require changing mkdocs.yml and is less intuitive since MkDocs conventionally uses `docs/` as the output directory name, not source.

## Recommendation

**Proceed with renaming `input/` → `doc-input/` and repurposing `input/` for MkDocs**. This is the cleanest solution that:
- Minimizes configuration changes
- Clearly separates concerns
- Follows each tool's conventions
- Preserves all existing content

## Next Steps

1. ✅ Get approval for this plan
2. Execute migration (rename directories, update configs)
3. Test build locally
4. Update CI/CD (GitHub Actions, Netlify)
5. Deploy and verify

---

**Status**: Awaiting approval  
**Date**: 2026-02-23  
**Approach**: Rename `input/` → `doc-input/`, repurpose `input/` for MkDocs