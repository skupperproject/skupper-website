# MkDocs MVP - Testing Instructions

## What's Been Created

The MVP integrates MkDocs Material with the existing Transom-based Skupper website to provide sidebar navigation for the V2 documentation.

### Files Created/Modified

1. **`mkdocs.yml`** - MkDocs configuration
   - Configures Material theme
   - Defines navigation structure for V2 docs
   - Sets up markdown extensions and plugins

2. **`config/mkdocs_macros.py`** - Variable substitution
   - Reads from `input/data/releases.json` (same as Transom)
   - Provides `{{skupper_cli_version}}` and other variables
   - Ensures consistency with main site

3. **`.plano.py`** - Updated build commands
   - `render_docs()` - Renders docs with MkDocs
   - `render_all()` - Renders entire site (Transom + MkDocs)

## Testing the MVP

### Prerequisites

```bash
# Ensure you have Python 3.8+ and pip installed
python --version

# Install dependencies
pip install mkdocs-material mkdocs-macros-plugin
```

### Step 1: Test MkDocs Only

Test that MkDocs can build the documentation:

```bash
# Build docs only (without Transom)
mkdocs build --clean

# Check output
ls -la output/docs/
```

**Expected Result**: 
- `output/docs/` directory created
- Contains HTML files with Material theme
- Sidebar navigation visible

### Step 2: Test Full Build

Test the complete build process (Transom + MkDocs):

```bash
# Build everything
./plano render_all

# Or use individual commands
./plano render        # Transom only
./plano render_docs   # MkDocs only
```

**Expected Result**:
- `output/` directory contains full site
- `output/v1/` exists (Transom-rendered V1 docs)
- `output/docs/` exists (MkDocs-rendered V2 docs with sidebar)

### Step 3: Verify V1 Preservation

Check that V1 documentation is NOT overwritten by MkDocs:

```bash
# Check V1 exists
ls -la output/v1/

# Check V1 files are HTML (not markdown)
file output/v1/index.html

# Verify V1 has Transom styling (not Material theme)
grep -l "Transom" output/v1/index.html || echo "V1 preserved correctly"
```

**Expected Result**:
- `output/v1/` directory exists
- Contains Transom-rendered HTML files
- Does NOT have Material theme styling

### Step 4: Test Variable Substitution

Check that Transom variables work in MkDocs:

```bash
# Check that version variables are substituted
grep -r "{{skupper_cli_version}}" output/docs/

# Should return NO results (variables should be replaced)
# If it returns results, variables are not being substituted
```

**Expected Result**:
- No `{{skupper_cli_version}}` in output files
- Version numbers appear as actual values (e.g., "2.1.1")

### Step 5: Serve Locally

Test the site locally:

```bash
# Serve with MkDocs (docs only)
mkdocs serve

# Open browser to http://localhost:8000
```

**Expected Result**:
- Documentation loads with sidebar navigation
- Material theme styling visible
- Navigation works
- Search works

### Step 6: Visual Inspection

Open the generated files in a browser:

```bash
# Open main site
open output/index.html

# Open V1 docs
open output/v1/index.html

# Open V2 docs
open output/docs/index.html
```

**Check**:
- ✅ Main site looks normal (Transom styling)
- ✅ V1 docs look normal (Transom styling)
- ✅ V2 docs have Material theme with sidebar
- ⚠️ V2 docs styling may differ from main site (expected in MVP)

## Known MVP Limitations

1. **CSS Not Aligned**: V2 docs use default Material theme, not Skupper branding
2. **No Custom Header/Footer**: V2 docs use Material's default header/footer
3. **Navigation Incomplete**: Some pages may not be in the nav tree yet
4. **No Search Integration**: Search only works within docs, not site-wide

These will be addressed in the refinement phase.

## Troubleshooting

### Error: "Module 'mkdocs_macros' not found"

```bash
pip install mkdocs-macros-plugin
```

### Error: "No module named 'transom'"

```bash
# Make sure you're in the project root
cd /path/to/skupper-website

# Check Python path includes the project
export PYTHONPATH="${PYTHONPATH}:$(pwd)/python"
```

### Variables Not Substituting

Check that `input/data/releases.json` exists:

```bash
ls -la input/data/releases.json

# If missing, generate it
./plano generate_releases
```

### V1 Directory Missing

Make sure Transom runs first:

```bash
./plano render        # Run Transom first
./plano render_docs   # Then run MkDocs
```

## Next Steps

After MVP validation:

1. **CSS Alignment** - Match Skupper branding
2. **Custom Templates** - Add Skupper header/footer
3. **Complete Navigation** - Add all doc pages
4. **Testing** - Visual regression tests
5. **Documentation** - Update main README

## Success Criteria

The MVP is successful if:

- ✅ MkDocs builds without errors
- ✅ V2 docs have sidebar navigation
- ✅ V1 docs are preserved (not overwritten)
- ✅ Variables substitute correctly
- ✅ Site serves locally
- ✅ No broken links in docs

## Questions or Issues?

Refer to `mkdocs-plan.md` for the complete integration plan and design decisions.