# HARCO LAB Website

Official website for the Human-Robot Collaboration (HARCO) Laboratory at Hanyang University ERICA.

🌐 **Live Site**: [https://hyharco.github.io](https://hyharco.github.io)

## Table of Contents

- [About](#about)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Development](#development)
- [Content Management](#content-management)
- [Scripts](#scripts)
- [Deployment](#deployment)
- [Contributing](#contributing)

---

## About

This is a Jekyll-based static website for HARCO LAB, featuring:

- Team member profiles
- Research projects and publications
- News and updates
- Laboratory equipment showcase
- Contact information

**Tech Stack**: Jekyll 4.4.1, GitHub Pages, SCSS, JavaScript

---

## Project Structure

```text
hyHarco.github.io/
├── _config.yaml                  # Jekyll configuration
├── CONVENTIONS.md                # File & directory naming rules
├── _data/                        # Site data (consumed by Liquid)
│   ├── links.yaml                # Social media links
│   ├── publication_metadata_cache.json # DOI metadata cache
│   ├── publication_overrides.yaml # Manual publication corrections / DOI hints
│   ├── roles.yaml                # Member role definitions
│   ├── tools.yaml                # Research tools / news cards
│   ├── youtube.json              # YouTube data (auto-scraped)
│   └── bibliography/
│       └── journal.bib           # BibTeX references
├── _includes/                    # Reusable HTML components
├── _layouts/                     # Page layouts
│   ├── default.html
│   ├── member.html
│   └── post.html
├── _members/                     # Member profiles (37 members, slug = firstname_lastname)
├── _posts/                       # Blog posts (79 total)
│   ├── news/                     # News posts (44)
│   ├── research/                 # Research posts (24)
│   ├── project/                  # Project posts (9)
│   └── workshop/                 # Workshop posts (2)
├── assets/
│   ├── documents/
│   │   ├── cv/                   # CV files
│   │   └── papers/               # Research papers
│   └── source/                   # Design source files (xlsx, ai)
├── css/                          # SCSS stylesheets (auto-loaded via _includes/styles.html)
│   ├── all.scss                  # Site shell (palettes, theme, mixins)
│   └── effects/
├── images/                       # Image assets — see CONVENTIONS.md for naming
│   ├── common/                   # Site chrome (logos, harco.png)
│   ├── equipment/                # Equipment showcase
│   ├── event_img/                # Event banners
│   ├── frontimg/                 # Homepage carousel slides
│   ├── lab/                      # Laboratory photos
│   ├── main_img/                 # Homepage hero
│   ├── members/                  # Member portraits (filename = slug)
│   │   └── _archive/             # Disabled / unreferenced portraits (build-excluded)
│   ├── news/                     # News images
│   ├── project/                  # Project images
│   ├── research/                 # Research images
│   ├── tools_yaml/               # Tool card images
│   └── _archive/                 # Unreferenced legacy images (build-excluded)
├── js/                           # JavaScript files
├── scripts/                      # Automation scripts
│   ├── start.sh                  # Start dev server
│   ├── publication_pipeline.py   # Merge Scholar data, overrides, DOI metadata
│   ├── scrape_scholar.py         # Fetch and parse Google Scholar
│   ├── update_publications.py    # Build publication/publications.json
│   ├── scrape_youtube.py         # Scrape YouTube
│   ├── update_publications.sh    # Local publication update wrapper
│   ├── update_patents_json.py    # Update patent JSON
│   └── templates/                # Post templates
├── contact/                      # Contact page
├── equipment/                    # Equipment page
├── lecture/                      # Lecture page
├── news/                         # News listing page
├── project/                      # Project listing page
├── publication/                  # Publications page and data JSON
│   ├── publications.json         # Publication data (Google Scholar)
│   └── patents.json              # Patent data
├── research/                     # Research pages (mobile_manipulator, exoskeleton_robot, ai)
├── team/                         # Team page
├── workshop/                     # Workshop page
├── favicons/                     # Site favicons / meta image
├── index.md                      # Homepage
├── 404.md                        # Error page
└── README.md                     # This file
```

> Folders prefixed with `_` (such as `images/_archive/`) are excluded from the Jekyll build output. They keep the files in source control without publishing them to the site.

---

## Getting Started

### Prerequisites

1. **Ruby** (version 2.7+)

2. **Bundler**

   ```bash
   gem install bundler
   ```

3. **Jekyll** (installed via Bundler)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/hyHarco/hyHarco.github.io.git
   cd hyHarco.github.io
   ```

2. **Install dependencies**

   ```bash
   bundle install
   ```

3. **Build the site**

   ```bash
   bundle exec jekyll build
   ```

4. **Start local development server**

   ```bash
   bundle exec jekyll serve
   ```

   Or use the convenience script:

   ```bash
   ./scripts/start.sh
   ```

5. **View the site**

   Open your browser to `http://localhost:4000`

---

## Development

### Local Development Server

#### Option 1: Basic server

```bash
bundle exec jekyll serve
```

#### Option 2: With live reload (recommended)

```bash
./scripts/start.sh
```

This will:

- Install/update dependencies
- Start Jekyll with live reload
- Automatically open browser
- Watch for file changes

### Building for Production

```bash
bundle exec jekyll build
```

Output is generated in `_site/` directory (ignored by git).

### CSS Optimization

CSS is automatically minified in production thanks to:
```yaml
# _config.yaml
sass:
  style: compressed
```

---

## Content Management

> See [CONVENTIONS.md](CONVENTIONS.md) for the full naming and placement rules.

### Adding a New Team Member

1. Create a new file in `_members/` using the canonical slug `firstname_lastname.md` (lowercase ASCII, single underscore):

   ```bash
   _members/john_doe.md
   ```

2. Add frontmatter:

   ```markdown
   ---
   name: John Doe
   image: images/members/john_doe.jpg
   description: Ph.D. Student
   aliases:
     - John Doe
   links:
     email: johndoe@example.com
     github: johndoe
   tier: third  # pi, research_professor, second, third, fourth, fifth, alumni
   ---

   # Research Interests
   - Human-Robot Interaction
   - Machine Learning
   ```

3. Add member photo to `images/members/john_doe.jpg` (filename matches the slug).

### Adding a News Post

1. Create a new file in `_posts/news/` (lowercase, snake_case):

   ```bash
   _posts/news/YYYY-MM-DD-news_title.md
   ```

2. Add frontmatter:

   ```markdown
   ---
   title: Your News Title
   author: Author Name        # display text
   member: john_doe           # member slug — links the post to the member's page
   image: images/news/your-image.jpg
   tags:
     - Conference
     - Award
   group: news
   ---

   Your news content here...
   ```

   For lab-wide posts use `member: All Member`.

### Adding Research/Project Posts

Similar to news posts, but place in:

- `_posts/research/` for research posts (set `group:` to a research area like `mobile_manipulator`, `exoskeleton`, or `ai`)
- `_posts/project/` for project posts (set `group: project`)

For research posts about a single member, prefer the slug-prefixed filename: `YYYY-MM-DD-research_<member_slug>_<n>.md` (e.g. `2025-01-02-research_jungsoo_lee_1.md`).

### Updating Publications

**Manual Corrections:**
Prefer editing `_data/publication_overrides.yaml` for corrections, DOI links,
or publications that are not on Google Scholar yet. The generated site data
still lives in `publication/publications.json`.

**Automated Update (Google Scholar + overrides + DOI enrichment):**

```bash
./scripts/update_publications.sh
```

This will:

1. Scrape publications from Google Scholar
2. Apply `_data/publication_overrides.yaml`
3. Enrich DOI entries through Manubot when enrichment is enabled
4. Save the final data to `publication/publications.json`

To skip DOI enrichment for a faster local run:

```bash
./scripts/update_publications.sh --no-enrich
```

The GitHub Actions workflow `.github/workflows/update-publications.yml`
also runs the same pipeline every day at 04:17 KST, or when related
publication pipeline files are pushed to `main`, and commits generated
publication data when it changes.

### Updating YouTube Videos

Homepage `Latest Videos` reads from `_data/youtube.json`.

**Manual Update:**

```bash
python3 scripts/scrape_youtube.py
```

**Automated Update:**
The GitHub Actions workflow `.github/workflows/update-youtube.yml`
refreshes `_data/youtube.json` every day at 04:37 KST, or when the YouTube
scraper workflow files are pushed to `main`, and commits the data when it
changes.

---

## Scripts

All scripts are located in `scripts/` directory.

### `start.sh`

Start local development server with live reload:

```bash
./scripts/start.sh
```

### `update_publications.sh`

Update publications from Google Scholar, manual overrides, and DOI metadata:

```bash
./scripts/update_publications.sh
```

Wraps `scripts/update_publications.py` and regenerates
`publication/publications.json`.

### `scrape_scholar.py`

Fetch and parse the HARCO Google Scholar profile. This is used by the
publication pipeline and can still write raw Scholar data directly:

```bash
python3 scripts/scrape_scholar.py
```

### `scrape_youtube.py`

Refresh `_data/youtube.json` from the lab YouTube channel RSS feed.

### `update_patents_json.py`

Convert the patent list in `assets/source/HARCO_patent_list.xlsx`
into JSON for the publications page.

**Requirements:**

- Python 3
- `update_publications.sh` creates a local virtual environment and installs `requests`, `pyyaml`, and `manubot`
- `update_patents_json.py` requires `openpyxl`

---

## Deployment

### GitHub Pages (Automatic)

The site is automatically deployed to GitHub Pages when changes are pushed to the `main` branch.

Deployment is handled by the repository's GitHub Pages settings.

### Manual Deployment

1. Ensure all changes are committed

2. Push to `main` branch:

   ```bash
   git push origin main
   ```

3. GitHub Pages will build and deploy automatically

---

## Contributing

### Branch Strategy

- `main` - Production branch (auto-deploys)
- `develop` - Development branch
- `feature/*` - Feature branches

### Workflow

1. Create a feature branch from `develop`:

   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit:

   ```bash
   git add .
   git commit -m "Description of changes"
   ```

3. Push and create Pull Request:

   ```bash
   git push -u origin feature/your-feature-name
   ```

4. Create PR to merge into `develop`

5. After testing, merge `develop` into `main`

### Code Style

- **Markdown**: Use consistent heading levels
- **YAML**: 2-space indentation
- **SCSS**: Follow existing patterns
- **JavaScript**: ES6+ syntax

### Testing Before Commit

Always test locally before committing:

```bash
bundle exec jekyll build
./scripts/start.sh
```

Check for:

- Build errors
- Broken links
- Image loading
- Responsive design

---

## Useful Commands

### Jekyll Commands

```bash
# Serve with drafts
bundle exec jekyll serve --drafts

# Serve with future posts
bundle exec jekyll serve --future

# Clean build artifacts
bundle exec jekyll clean

# Build with verbose output
bundle exec jekyll build --verbose

# Update dependencies
bundle update
```

### Git Commands

```bash
# View current branch
git status

# View commit history
git log --oneline -10

# Create and switch to new branch
git checkout -b branch-name

# Sync with remote
git pull origin develop
```

---

## Troubleshooting

### Jekyll won't start

1. Clean build artifacts:

   ```bash
   bundle exec jekyll clean
   ```

2. Reinstall dependencies:

   ```bash
   bundle install
   ```

3. Check Ruby version:

   ```bash
   ruby -v  # Should be 2.7+
   ```

### Images not loading

- Check file path is correct (case-sensitive)
- Ensure image is in `images/` directory
- Use relative paths: `images/folder/image.png`

### CSS not updating

1. Clear Jekyll cache:

   ```bash
   bundle exec jekyll clean
   ```

2. Hard refresh browser (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows)

---

## License

See [LICENSE.md](LICENSE.md)

---

## Contact

**HARCO LAB**
Hanyang University ERICA
Robotics Department

- **Website**: [https://hyharco.github.io](https://hyharco.github.io)
- **Email**: wansookim@hanyang.ac.kr
- **GitHub**: [github.com/hyHarco](https://github.com/hyHarco)

---

**Last Updated**: 2026-08-01
