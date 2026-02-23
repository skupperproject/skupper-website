# MkDocs Integration Plan for Skupper Website

## Overview

This plan outlines the integration of MkDocs Material to provide sidebar navigation for the documentation section of the Skupper website, while maintaining the existing Transom-based build system for the main site.

## Current Architecture

- **Build Tool**: Transom (static site generator using Markdown → HTML)
- **Input Directory**: `input/`
- **Output Directory**: `output/` (assumed, not currently in repo)
- **Documentation Source**: `input/docs/` (contains multiple subdirectories with markdown files)
- **Build Command**: `./plano render`
- **Main Site**: Root pages, concepts, resources, commands, examples, releases, etc.

## Proposed Architecture

### Two-Stage Build Process

1. **Stage 1: Transom Build** (existing)
   - Renders the entire site from `input/` to `output/`
   - Generates all pages: home, concepts, resources, commands, examples, etc.
   - Creates `output/docs/` with initial documentation structure

2. **Stage 2: MkDocs Build** (new)
   - Runs after Transom completes
   - Takes `input/docs/` as source
   - Generates enhanced documentation with Material theme sidebar to `output/docs/`
   - Overwrites the `output/docs/` directory created by Transom

### Directory Structure

```
skupper-website/
├── input/
│   ├── index.md                    # Main site (Transom)
│   ├── concepts/                   # Main site (Transom)
│   ├── resources/                  # Main site (Transom)
│   ├── commands/                   # Main site (Transom)
│   ├── examples/                   # Main site (Transom)
│   ├── releases/                   # Main site (Transom)
│   ├── v1/                         # V1 docs (Transom) - NOT touched by MkDocs
│   │   ├── index.md
│   │   ├── docs/
│   │   ├── examples/
│   │   ├── install/
│   │   ├── releases/
│   │   └── start/
│   ├── v2/                         # V2 overview (Transom)
│   ├── docs/                       # V2 Documentation (MkDocs source)
│   │   ├── overview/
│   │   ├── install/
│   │   ├── kube-cli/
│   │   ├── kube-yaml/
│   │   ├── system-cli/
│   │   ├── system-yaml/
│   │   ├── console/
│   │   ├── troubleshooting/
│   │   └── api-docs/
│   ├── main.css                    # Main site styles
│   └── main.js                     # Main site scripts
├── output/
│   ├── index.html                  # Main site (Transom output)
│   ├── concepts/                   # Main site (Transom output)
│   ├── resources/                  # Main site (Transom output)
│   ├── commands/                   # Main site (Transom output)
│   ├── examples/                   # Main site (Transom output)
│   ├── releases/                   # Main site (Transom output)
│   ├── v1/                         # V1 docs (Transom output) - PRESERVED
│   │   ├── index.html
│   │   ├── docs/
│   │   ├── examples/
│   │   └── ...
│   ├── v2/                         # V2 overview (Transom output)
│   └── docs/                       # V2 Documentation (MkDocs output)
│       ├── index.html              # Docs home with sidebar
│       ├── overview/
│       ├── install/
│       └── ...
├── mkdocs.yml                      # MkDocs configuration (new)
└── .plano.py                       # Updated build commands
```

## Implementation Details

### 1. MkDocs Configuration (`mkdocs.yml`)

```yaml
site_name: Skupper Documentation
site_url: https://skupper.io/docs/
docs_dir: input/docs
site_dir: output/docs

theme:
  name: material
  custom_dir: config/mkdocs-overrides  # For header/footer integration
  palette:
    primary: blue
    accent: green
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.suggest
    - search.highlight
    - content.code.copy

nav:
  - Home: index.md
  - Overview:
    - Introduction: overview/index.md
    - Connectivity: overview/connectivity.md
    - Security: overview/security.md
    - Routing: overview/routing.md
    - Load Balancing: overview/load-balancing.md
    - Resources: overview/resources.md
    - Migrating: overview/migrating.md
  - Installation:
    - Getting Started: install/index.md
  - Kubernetes CLI:
    - Overview: kube-cli/index.md
    - Site Configuration: kube-cli/site-configuration.md
    - Site Linking: kube-cli/site-linking.md
    - Service Exposure: kube-cli/service-exposure.md
  - Kubernetes YAML:
    - Overview: kube-yaml/index.md
    - Site Configuration: kube-yaml/site-configuration.md
    - Site Linking: kube-yaml/site-linking.md
    - Service Exposure: kube-yaml/service-exposure.md
  - System CLI:
    - Overview: system-cli/index.md
    - Site Configuration: system-cli/site-configuration.md
    - Site Linking: system-cli/site-linking.md
    - Service Exposure: system-cli/service-exposure.md
  - System YAML:
    - Overview: system-yaml/index.md
    - Site Configuration: system-yaml/site-configuration.md
    - Site Linking: system-yaml/site-linking.md
    - Service Exposure: system-yaml/service-exposure.md
  - Console: console/index.md
  - Troubleshooting: troubleshooting/index.md
  - API Reference: api-docs/index.html

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.tabbed:
      alternate_style: true
  - attr_list
  - md_in_html
  - toc:
      permalink: true

extra_css:
  - stylesheets/extra.css  # For Skupper branding consistency

plugins:
  - search
```

### 2. Header/Footer Integration

Create `config/mkdocs-overrides/` directory with custom templates to maintain consistent Skupper branding:

- `config/mkdocs-overrides/main.html` - Override to include Skupper header/footer
- `config/mkdocs-overrides/stylesheets/extra.css` - Additional styles for brand consistency

### 3. Updated Build Commands (`.plano.py`)

Add new command to integrate MkDocs:

```python
@command
def render_docs():
    """
    Render documentation using MkDocs after Transom build
    """
    # Ensure MkDocs is installed
    run("pip install mkdocs-material mkdocs-macros-plugin", quiet=True)
    
    # Build docs with MkDocs (only builds input/docs -> output/docs)
    # Does NOT touch output/v1/ which was rendered by Transom
    run("mkdocs build --clean")

@command
def render():
    """
    Render the entire site (Transom + MkDocs)
    
    Build order:
    1. Transom renders everything from input/ to output/
       - This includes input/v1/ -> output/v1/
       - This includes input/docs/ -> output/docs/ (basic version)
    2. MkDocs renders input/docs/ to output/docs/
       - This OVERWRITES output/docs/ with enhanced version
       - This does NOT touch output/v1/ (preserved from Transom)
    """
    # First run the existing Transom render
    from transom.planocommands import render as transom_render
    transom_render()
    
    # Then render docs with MkDocs (overwrites output/docs/ only)
    render_docs()

@command
def serve():
    """
    Serve the site locally with live reload
    """
    # For development, we could run both servers or just Transom
    # Option 1: Just use Transom serve (simpler for now)
    from transom.planocommands import serve as transom_serve
    transom_serve()
    
    # Option 2: Run MkDocs serve separately for docs development
    # run("mkdocs serve --dev-addr localhost:8001")
```

**Key Points About V1 Preservation**:

1. **MkDocs Configuration** (`mkdocs.yml`):
   ```yaml
   docs_dir: input/docs      # Only processes input/docs/
   site_dir: output/docs     # Only writes to output/docs/
   ```
   
   MkDocs is configured to ONLY read from `input/docs/` and ONLY write to `output/docs/`. It never touches `input/v1/` or `output/v1/`.

2. **Build Order Matters**:
   - Transom runs first and renders ALL of `input/` including `input/v1/` → `output/v1/`
   - MkDocs runs second and ONLY overwrites `output/docs/`
   - Result: `output/v1/` remains exactly as Transom rendered it

3. **No Configuration Needed**:
   - This is the default behavior of MkDocs
   - `docs_dir` and `site_dir` settings ensure isolation
   - No special exclusion rules needed

4. **Testing V1 Preservation**:
   ```bash
   # After running ./plano render
   # Check that v1 files exist and are from Transom
   ls -la output/v1/
   # Should show Transom-rendered HTML files
   
   # Check that docs files are from MkDocs
   ls -la output/docs/
   # Should show MkDocs Material-themed files with sidebar
   ```

### 4. CSS/JS Considerations

**Challenge**: MkDocs Material has its own styling that may conflict with the main site.

**Solutions**:
1. **Scoped Styles**: Keep MkDocs styles isolated to `/docs/` path
2. **Custom CSS**: Create `config/mkdocs-overrides/stylesheets/extra.css` to:
   - Match Skupper color scheme (blues, greens)
   - Ensure consistent header/footer appearance
   - Override Material theme where needed
3. **Shared Assets**: Copy necessary assets from `input/docs/main.css` and `input/docs/main.js` to MkDocs custom directory

### 5. Navigation Integration

**Main Site → Docs**:
- Update `input/index.md` and other main site pages to link to `/docs/` (MkDocs entry point)
- Existing links like `<a href="docs/overview/index.html">` will work seamlessly

**Docs → Main Site**:
- Add custom header in MkDocs override template with links back to:
  - Home (`/`)
  - Concepts (`/concepts/`)
  - Resources (`/resources/`)
  - Commands (`/commands/`)
  - Examples (`/examples/`)

## Benefits

1. **Sidebar Navigation**: MkDocs Material provides excellent sidebar navigation for documentation
2. **Search**: Built-in search functionality for docs
3. **Mobile Responsive**: Material theme is mobile-friendly
4. **Minimal Disruption**: Main site continues to use Transom unchanged
5. **Clear Separation**: Documentation has distinct UX while maintaining brand consistency
6. **Easy Updates**: Documentation can be updated independently
7. **V1 Preservation**: V1 documentation (`input/v1/`) remains untouched by MkDocs, rendered only by Transom

## CSS Alignment Strategy

### Critical Requirement: Seamless User Experience

The transition from main site to documentation must be **visually seamless**. Users should not notice they've moved from Transom-rendered pages to MkDocs-rendered pages except for the addition of the sidebar navigation.

### Current Skupper Design System

**Colors** (from `input/main.css`):
```css
--body-background-color: hsl(0, 0%, 100%)     /* White */
--footer-background-color: #365263             /* Dark blue-gray */
--text-color: hsl(0, 0%, 20%)                 /* Dark gray */
--link-color: #306b8f                          /* Blue */
--accent-color-1: #5eba7d                      /* Green */
--accent-color-2: #f08275                      /* Coral/red */
--code-background-color: hsl(0, 0%, 97%)      /* Light gray */
```

**Typography**:
- Body: `sans-serif` (Lato via Google Fonts)
- Headings: `sans-serif` (Alegreya Sans via Google Fonts)
- Code: `monospace` (Roboto Mono via Google Fonts)
- Line height: `1.5em`

**Layout**:
- Page width: `1100px`
- Grid-based layout with header, main (70%), aside (30%), footer
- Sticky header at top
- Sticky sidebar (aside) for table of contents

**Header Structure**:
- Logo + "Skupper" text on left
- Navigation tabs: Home, Getting started, Examples, Documentation, Releases, Community
- GitHub link on right
- White background with bottom border

**Footer Structure**:
- Dark blue-gray background (`#365263`)
- Three columns: Social links, Copyright, License info
- White text

### MkDocs Material Customization Approach

#### 1. Override MkDocs Material Theme

Create `config/mkdocs-overrides/main.html`:

```html
{% extends "base.html" %}

{# Remove Material's header entirely - we'll inject Skupper's header #}
{% block header %}
{% endblock %}

{# Inject Skupper header before content #}
{% block content %}
  {{ super() }}
{% endblock %}

{# Remove Material's footer - we'll inject Skupper's footer #}
{% block footer %}
{% endblock %}
```

Create `config/mkdocs-overrides/partials/header.html`:
```html
<!-- Skupper header from config/header.html -->
<header>
  <a href="{{config.site_url}}../index.html" id="-logo">
    <img src="{{config.site_url}}../images/skupper-logo.svg">
    <div>Skupper</div>
  </a>
  <div>
    <nav id="-tabs">
      <a href="{{config.site_url}}../index.html"><div>Home</div></a>
      <a href="{{config.site_url}}../start/index.html"><div>Getting started</div></a>
      <a href="{{config.site_url}}../examples/index.html"><div>Examples</div></a>
      <a href="{{config.site_url}}../docs/index.html" class="selected"><div>Documentation</div></a>
      <a href="{{config.site_url}}../releases/index.html"><div>Releases</div></a>
      <a href="{{config.site_url}}../community/index.html"><div>Community</div></a>
    </nav>
    <a href="https://github.com/skupperproject">
      <div><span class="fab fa-github fa-lg"></span> GitHub</div>
    </a>
  </div>
</header>
```

Create `config/mkdocs-overrides/partials/footer.html`:
```html
<!-- Skupper footer from config/footer.html -->
<footer>
  <div>
    <div>
      <p><a href="https://github.com/skupperproject"><span class="fab fa-github fa-lg"></span> GitHub</a></p>
      <p><a href="https://groups.google.com/forum/#!forum/skupper"><span class="fas fa-envelope fa-lg"></span> Mailing list</a></p>
      <p><a href="https://www.youtube.com/channel/UCQxHN2Qq8koCatcmKCJ4OEA"><span class="fab fa-youtube fa-lg"></span> YouTube</a></p>
    </div>
    <div>
      <h4>Skupper - Multi-platform application interconnect</h4>
      <p>Copyright © 2025 the Skupper authors</p>
    </div>
    <div>
      <p>All code and documentation is licensed under the <a href="https://www.apache.org/licenses/LICENSE-2.0">Apache License version 2.0</a>.</p>
      <nav class="links">
        <a href="{{config.site_url}}../site.html">About this site</a>
      </nav>
    </div>
  </div>
</footer>
```

#### 2. Custom CSS File Structure

Create `config/mkdocs-overrides/stylesheets/skupper.css`:

```css
/* Import Google Fonts - EXACT same as main site */
@import url('https://fonts.googleapis.com/css2?family=Alegreya+Sans:ital,wght@0,100;0,300;0,400;0,500;0,700;0,800;0,900;1,100;1,300;1,400;1,500;1,700;1,800;1,900&family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&family=Roboto+Mono:ital,wght@0,100..700;1,100..700&family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap');

/* Skupper CSS Variables - EXACT same as main site */
:root {
    --body-background-color: hsl(0, 0%, 100%);
    --code-background-color: hsl(0, 0%, 97%);
    --footer-background-color: #365263;
    --text-color: hsl(0, 0%, 20%);
    --disabled-text-color: hsl(0, 0%, 40%);
    --line-color: hsl(0, 0%, 95%);
    --link-color: #306b8f;
    --accent-color-1: #5eba7d;
    --accent-color-2: #f08275;
    --selected-item-background-color: hsla(6, 80%, 70%, 0.3);
    --body-font-family: 'Lato', sans-serif;
    --body-line-height: 1.5em;
    --code-font-family: 'Roboto Mono', monospace;
    --heading-font-family: 'Alegreya Sans', sans-serif;
    --page-width: 1100px;
}

/* Override Material Design defaults to match Skupper */
.md-header {
    display: none !important; /* Hide Material header */
}

.md-footer {
    display: none !important; /* Hide Material footer */
}

/* Skupper Header Styles - EXACT copy from main.css */
header {
    display: flex;
    background-color: var(--body-background-color);
    border-bottom: 1px solid var(--line-color);
    position: sticky;
    top: 0;
    z-index: 1000;
    padding: 1em;
    width: 100%;
}

header #-logo {
    display: flex;
    align-items: center;
    gap: 0.5em;
    text-decoration: none;
    color: var(--text-color);
    font-size: 1.2em;
    font-weight: 700;
    font-family: var(--heading-font-family);
}

header #-logo img {
    height: 2em;
}

header > div {
    display: flex;
    flex: 1;
    justify-content: space-between;
    align-items: center;
}

header nav#-tabs {
    display: flex;
    gap: 1.5em;
}

header nav#-tabs a {
    text-decoration: none;
    color: var(--text-color);
    padding: 0.5em 0;
    border-bottom: 3px solid transparent;
}

header nav#-tabs a:hover {
    border-bottom-color: var(--accent-color-1);
}

header nav#-tabs a.selected {
    border-bottom-color: var(--accent-color-2);
    font-weight: 700;
}

/* Skupper Footer Styles - EXACT copy from main.css */
footer {
    background-color: var(--footer-background-color);
    color: white;
    padding: 2em 1em;
    margin-top: 3em;
}

footer a {
    color: white;
    text-decoration: none;
}

footer a:hover {
    text-decoration: underline;
}

footer > div {
    max-width: var(--page-width);
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2em;
}

/* Main Content Area - Match Skupper layout */
.md-main {
    background-color: var(--body-background-color);
}

.md-content {
    max-width: var(--page-width);
    margin: 0 auto;
}

.md-content__inner {
    padding: 2.4em 1em;
}

/* Typography - Match Skupper exactly */
body {
    font-family: var(--body-font-family);
    line-height: var(--body-line-height);
    color: var(--text-color);
}

h1, h2, h3, h4, h5, h6 {
    font-family: var(--heading-font-family);
    color: var(--text-color);
}

h1 { font-size: 1.8em; }
h2 { font-size: 1.4em; }
h3 { font-size: 1.2em; }
h4 { font-size: 1.05em; }

a {
    color: var(--link-color);
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

/* Code blocks - Match Skupper exactly */
code {
    font-family: var(--code-font-family);
    font-size: 0.8em;
    background-color: var(--code-background-color);
    padding: 0.2em 0.4em;
    border-radius: 3px;
}

pre {
    background-color: var(--code-background-color);
    padding: 1em;
    border-radius: 3px;
    overflow: auto;
}

pre code {
    background-color: transparent;
    padding: 0;
}

/* Material Sidebar - Style to match Skupper aside */
.md-sidebar--primary {
    background-color: var(--body-background-color);
    border-right: 1px solid var(--line-color);
}

.md-sidebar--primary .md-sidebar__scrollwrap {
    background-color: var(--body-background-color);
}

.md-nav {
    font-size: 0.95em;
}

.md-nav__link {
    color: var(--text-color);
}

.md-nav__link:hover {
    color: var(--link-color);
}

.md-nav__link--active {
    color: var(--text-color);
    font-weight: 700;
}

/* Table of Contents (right sidebar) - Match Skupper aside */
.md-sidebar--secondary {
    border-left: 1px solid var(--line-color);
    padding-left: 2em;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    header nav#-tabs {
        display: none;
    }
    
    footer > div {
        grid-template-columns: 1fr;
    }
}
```

#### 3. Updated MkDocs Configuration

```yaml
site_name: Skupper Documentation
site_url: https://skupper.io/docs/
docs_dir: input/docs
site_dir: output/docs

theme:
  name: material
  custom_dir: config/mkdocs-overrides
  palette:
    primary: white  # Override to use our custom colors
    accent: white   # Override to use our custom colors
  font: false  # Disable Material fonts, use our own
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - navigation.indexes
    - search.suggest
    - search.highlight
    - content.code.copy
    - content.code.annotate

extra_css:
  - stylesheets/skupper.css  # Our custom CSS that matches main site

extra_javascript:
  - https://kit.fontawesome.com/YOUR_KIT_ID.js  # For Font Awesome icons

# ... rest of config
```

#### 4. Layout Integration Strategy

**Grid Layout Approach**:
- MkDocs Material uses flexbox for its layout
- We'll override with CSS Grid to match Skupper's main site
- Main content area: 70% width (matching Transom)
- Sidebar: 30% width (matching Transom aside)
- Both sticky positioned

**Key CSS Override**:
```css
/* Force MkDocs to use Skupper's grid layout */
.md-container {
    display: grid;
    grid-template-columns: minmax(2em, 1fr) calc(var(--page-width) * 0.7) calc(var(--page-width) * 0.3) minmax(2em, 1fr);
    grid-template-areas: ". main sidebar .";
}

.md-content {
    grid-area: main;
}

.md-sidebar--secondary {
    grid-area: sidebar;
}
```

### Implementation Checklist

- [ ] Copy exact CSS variables from `input/main.css` to `skupper.css`
- [ ] Copy exact header HTML from `config/header.html` to MkDocs override
- [ ] Copy exact footer HTML from `config/footer.html` to MkDocs override
- [ ] Import same Google Fonts (Lato, Alegreya Sans, Roboto Mono)
- [ ] Match typography sizes exactly (h1: 1.8em, h2: 1.4em, etc.)
- [ ] Match color scheme exactly (link color: #306b8f, etc.)
- [ ] Match code block styling (background: hsl(0, 0%, 97%))
- [ ] Match grid layout (70/30 split, 1100px max width)
- [ ] Test header navigation highlighting (Documentation tab selected)
- [ ] Test footer links work correctly
- [ ] Test responsive breakpoints match (768px)
- [ ] Verify Font Awesome icons load correctly
- [ ] Test sticky header behavior matches
- [ ] Test sticky sidebar behavior matches

### Visual Regression Testing

Before deployment, perform side-by-side comparison:

1. **Header**: Screenshot Transom page header vs MkDocs page header
2. **Typography**: Compare h1, h2, h3, p, code rendering
3. **Colors**: Verify links, backgrounds, text colors match
4. **Layout**: Verify 70/30 split, max-width, padding match
5. **Footer**: Screenshot and compare footer layout
6. **Responsive**: Test mobile view matches

### Fallback Strategy

If perfect CSS alignment proves difficult:

**Option A**: Iframe approach
- Keep Transom header/footer as-is
- Embed MkDocs content in iframe
- Pros: Perfect isolation
- Cons: SEO issues, complexity

**Option B**: Simplified Material theme
- Use Material's minimal theme
- Heavy CSS overrides
- Accept minor visual differences in sidebar only

**Option C**: Custom MkDocs theme
- Build custom theme from scratch
- Copy all Skupper CSS
- Full control but more work

## Potential Issues & Solutions

### Issue 1: Build Time
**Problem**: Two-stage build may be slower
**Solution**: MkDocs is very fast; impact should be minimal (< 1 second for docs)

### Issue 2: CSS Specificity Conflicts
**Problem**: MkDocs Material has high-specificity selectors that may override our styles
**Solution**:
- Use `!important` sparingly but strategically
- Increase specificity with `.md-content .md-content__inner` prefixes
- Test thoroughly and document any necessary overrides

### Issue 3: Font Loading
**Problem**: Loading fonts twice (main site + docs) may cause FOUT
**Solution**:
- Use same Google Fonts URL in both places
- Browser will cache fonts
- Consider preloading fonts in header

### Issue 4: Development Workflow
**Problem**: Running two servers for development
**Solution**:
- Primary: Use `./plano serve` (Transom) for main site development
- Docs: Use `mkdocs serve` separately when working on docs
- Or integrate both into single serve command with different ports

### Issue 5: JavaScript Conflicts
**Problem**: Material theme JS may conflict with Skupper's main.js
**Solution**:
- Material JS is scoped to `.md-` classes
- Skupper JS targets specific IDs
- Should not conflict, but test thoroughly
- Consider disabling Material JS features if conflicts arise

### Issue 6: Maintaining CSS Parity
**Problem**: When main site CSS changes, docs CSS must be updated
**Solution**:
- Document the CSS copying process
- Create a script to extract and convert CSS variables
- Add to update checklist: "Update MkDocs CSS when main.css changes"
- Consider automated testing for visual regression

### Issue 7: Transom Template Variables
**Problem**: Documentation markdown files use Transom template variables like `{{skupper_cli_version}}`, `{{site.prefix}}`, etc. MkDocs doesn't support these variables natively.

**Examples from current docs**:
```markdown
# From input/docs/console/index.md
helm install skupper-network-observer oci://quay.io/skupper/helm/network-observer --version {{skupper_cli_version}}

# From input/docs/install/index.md
kubectl apply -f https://github.com/skupperproject/skupper/releases/download/{{skupper_cli_version}}/skupper-cluster-scope.yaml
```

**Transom Variables Used** (from `config/transom.py`):
- `{{skupper_version}}` - Current Skupper version (e.g., "2.1.1")
- `{{skupper_cli_version}}` - CLI version (same as skupper_version)
- `{{latest_release_version}}` - Latest release version
- `{{latest_release_date}}` - Latest release date
- `{{site.prefix}}` - Site URL prefix (e.g., "" or "/skupper-website")
- `{{skupper_version_v1}}` - V1 version (e.g., "1.9.2")

**Solution Options**:

**Option A: MkDocs Macros Plugin** (Recommended)
```bash
pip install mkdocs-macros-plugin
```

Add to `mkdocs.yml`:
```yaml
plugins:
  - search
  - macros:
      module_name: config/mkdocs_macros

extra:
  skupper_version: "2.1.1"  # Read from data/releases.json
  skupper_cli_version: "2.1.1"
  skupper_version_v1: "1.9.2"
  site_prefix: ""
  latest_release_version: "2.1.1"
  latest_release_date: "2025-01-15"
```

Create `config/mkdocs_macros.py`:
```python
import json
from pathlib import Path

def define_env(env):
    """
    Define variables and macros for MkDocs
    Reads from the same data sources as Transom
    """
    # Read release data (same as Transom)
    releases_file = Path("input/data/releases.json")
    if releases_file.exists():
        releases = json.loads(releases_file.read_text())
        latest = releases.get("latest", {})
        
        env.variables['skupper_version'] = latest.get("version", "2.1.1")
        env.variables['skupper_cli_version'] = latest.get("version", "2.1.1")
        env.variables['latest_release_version'] = latest.get("version", "2.1.1")
        env.variables['latest_release_date'] = latest.get("date", "")
    
    # Other variables
    env.variables['skupper_version_v1'] = "1.9.2"
    env.variables['site_prefix'] = ""  # Or read from config
    
    # Define macros if needed
    @env.macro
    def get_download_url(version):
        return f"https://github.com/skupperproject/skupper/releases/download/{version}"
```

Usage in markdown (compatible with Transom syntax):
```markdown
helm install skupper-network-observer oci://quay.io/skupper/helm/network-observer --version {{ skupper_cli_version }}

kubectl apply -f https://github.com/skupperproject/skupper/releases/download/{{ skupper_cli_version }}/skupper-cluster-scope.yaml
```

**Option B: Pre-processing Script**
Create a script that runs before MkDocs build:
```python
# scripts/preprocess_docs.py
import json
import re
from pathlib import Path

def preprocess_markdown_files():
    """Replace Transom variables with actual values before MkDocs build"""
    
    # Read variables from same source as Transom
    releases = json.loads(Path("input/data/releases.json").read_text())
    latest = releases["latest"]
    
    variables = {
        'skupper_version': latest["version"],
        'skupper_cli_version': latest["version"],
        'latest_release_version': latest["version"],
        'site.prefix': '',
        'skupper_version_v1': '1.9.2',
    }
    
    # Process all markdown files in input/docs
    for md_file in Path("input/docs").rglob("*.md"):
        content = md_file.read_text()
        
        # Replace {{variable}} with actual values
        for var, value in variables.items():
            content = re.sub(
                r'\{\{' + re.escape(var) + r'\}\}',
                value,
                content
            )
        
        md_file.write_text(content)
```

Update `.plano.py`:
```python
@command
def render_docs():
    """Render documentation using MkDocs after Transom build"""
    # Pre-process markdown files to replace variables
    run("python scripts/preprocess_docs.py")
    
    # Build docs with MkDocs
    run("pip install mkdocs-material mkdocs-macros-plugin", quiet=True)
    run("mkdocs build --clean")
```

**Option C: Jinja2 Templates in MkDocs**
MkDocs Material supports Jinja2 templates natively for some features, but not in markdown content by default. Would require custom plugin.

**Recommendation**: Use **Option A (MkDocs Macros Plugin)** because:
- Maintains same variable syntax as Transom (`{{ variable }}`)
- Reads from same data sources (`input/data/releases.json`)
- No pre-processing needed
- Variables stay dynamic
- Easy to maintain

**Implementation Steps**:
1. Install `mkdocs-macros-plugin`
2. Create `config/mkdocs_macros.py` to read from `input/data/releases.json`
3. Add plugin to `mkdocs.yml`
4. Test that all variables render correctly
5. Document variable mapping in README

**Variable Mapping Table**:

| Transom Variable | MkDocs Variable | Source | Example Value |
|-----------------|-----------------|--------|---------------|
| `{{skupper_version}}` | `{{ skupper_version }}` | `input/data/releases.json` | "2.1.1" |
| `{{skupper_cli_version}}` | `{{ skupper_cli_version }}` | `input/data/releases.json` | "2.1.1" |
| `{{latest_release_version}}` | `{{ latest_release_version }}` | `input/data/releases.json` | "2.1.1" |
| `{{latest_release_date}}` | `{{ latest_release_date }}` | `input/data/releases.json` | "2025-01-15" |
| `{{site.prefix}}` | `{{ site_prefix }}` | Config | "" |
| `{{skupper_version_v1}}` | `{{ skupper_version_v1 }}` | Config | "1.9.2" |

**Testing Checklist**:
- [ ] Verify all `{{skupper_cli_version}}` references render correctly
- [ ] Verify all `{{site.prefix}}` references render correctly
- [ ] Test that version updates in `releases.json` propagate to docs
- [ ] Check that URLs with variables are valid
- [ ] Verify code blocks with variables render properly

## Migration Steps

1. **Install MkDocs Material**
   ```bash
   pip install mkdocs-material
   ```

2. **Create `mkdocs.yml`** with configuration above

3. **Create MkDocs overrides directory**
   ```bash
   mkdir -p config/mkdocs-overrides/stylesheets
   ```

4. **Create custom templates** for header/footer integration

5. **Update `.plano.py`** with new render commands

6. **Test build**
   ```bash
   ./plano render
   ```

7. **Test local serving**
   ```bash
   ./plano serve
   ```

8. **Update CI/CD** workflow if needed

9. **Update documentation** (README.md) with new build process

## Alternative Approaches Considered

### Alternative 1: Full MkDocs Migration
**Description**: Convert entire site to MkDocs
**Pros**: Single build system, consistent navigation everywhere
**Cons**: Major rewrite, lose Transom features, complex migration

### Alternative 2: Keep Transom Only
**Description**: Enhance Transom templates for sidebar navigation
**Pros**: No new dependencies, single build system
**Cons**: Significant custom development, reinventing MkDocs features

### Alternative 3: Separate Docs Site
**Description**: Host docs at `docs.skupper.io` with full MkDocs
**Pros**: Complete separation, independent deployment
**Cons**: Split user experience, separate domain management

## Recommendation

**Proceed with the proposed two-stage build approach** because:
- Minimal disruption to existing site
- Leverages MkDocs Material's excellent documentation features
- Maintains brand consistency through custom overrides
- Clear separation of concerns (main site vs. docs)
- Easy to implement and test incrementally

## Timeline Estimate

- **Setup & Configuration**: 2-3 hours
- **Custom Templates/Styling**: 3-4 hours
- **Testing & Refinement**: 2-3 hours
- **Documentation Updates**: 1 hour
- **Total**: 8-11 hours

## Next Steps for Approval

1. Review this plan
2. Approve or request modifications
3. Begin implementation with `mkdocs.yml` creation
4. Iterate on styling and navigation
5. Test thoroughly before deployment