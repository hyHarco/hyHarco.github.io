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
├── _config.yaml              # Jekyll configuration
├── _data/                    # Data files
│   ├── citations.yaml        # Auto-generated citations
│   ├── links.yaml           # Social media links
│   ├── publications.json    # Publication data
│   ├── roles.yaml           # Member role definitions
│   ├── sources.yaml         # Citation sources
│   ├── tools.yaml           # Research tools
│   └── bibliography/        # Bibliography files
│       └── journal.bib      # BibTeX references
├── _includes/               # Reusable HTML components (49 files)
│   ├── header.html
│   ├── footer.html
│   ├── citation.html
│   └── ...
├── _layouts/                # Page layouts
│   ├── default.html
│   ├── member.html
│   └── post.html
├── _members/                # Member profiles (39 members)
│   └── *.md                # Individual member files
├── _posts/                  # Blog posts (72 posts)
│   ├── news/               # News posts (40)
│   ├── research/           # Research posts (27)
│   ├── project/            # Project posts (11)
│   └── workshop/           # Workshop posts (4)
├── assets/                  # Document assets
│   ├── documents/
│   │   ├── cv/             # CV files
│   │   └── papers/         # Research papers
│   └── source/             # Design source files
├── css/                     # Stylesheets (52 SCSS files)
│   ├── all.scss            # Main stylesheet
│   └── effects/            # Effect stylesheets
│       └── snow.css
├── images/                  # Image assets
│   ├── common/             # Common images
│   │   └── logos/          # Logo files
│   ├── equipment/          # Equipment photos
│   ├── lab/                # Laboratory photos
│   ├── members/            # Member photos
│   ├── news/               # News images
│   ├── project/            # Project images
│   └── research/           # Research images
├── js/                      # JavaScript files
│   ├── search.js
│   ├── anchors.js
│   └── tooltips.js
├── scripts/                 # Automation scripts
│   ├── cite.sh             # Run auto-cite
│   ├── start.sh            # Start dev server
│   ├── update_publications.sh  # Update publications
│   └── scrape_scholar.py   # Scrape Google Scholar
├── contact/                 # Contact page
├── lecture/                 # Lecture page
├── news/                    # News listing page
├── project/                 # Project listing page
├── publication/             # Publications page
├── research/                # Research pages
├── team/                    # Team page
├── workshop/                # Workshop page
├── index.md                 # Homepage
├── 404.md                   # Error page
└── README.md                # This file
```

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

### Adding a New Team Member

1. Create a new file in `_members/` directory:

   ```bash
   _members/firstname-lastname.md
   ```

2. Add frontmatter:

   ```markdown
   ---
   name: John Doe
   image: images/members/johndoe.jpg
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

3. Add member photo to `images/members/`

### Adding a News Post

1. Create a new file in `_posts/news/`:

   ```bash
   _posts/news/YYYY-MM-DD-news_title.md
   ```

2. Add frontmatter:

   ```markdown
   ---
   title: Your News Title
   author: Author Name
   member: Author-Name
   image: images/news/your-image.jpg
   tags:
     - Conference
     - Award
   group: news
   ---

   Your news content here...
   ```

### Adding Research/Project Posts

Similar to news posts, but place in:

- `_posts/research/` for research posts (set `group: research`)
- `_posts/project/` for project posts (set `group: project`)

### Updating Publications

**Manual Update:**
Edit `_data/publications.json` directly.

**Automated Update (from Google Scholar):**

```bash
./scripts/update_publications.sh
```

This will:

1. Scrape publications from Google Scholar
2. Save to `_data/publications.json`
3. Create a new branch
4. Commit and push changes
5. Prompt you to create a Pull Request

---

## Scripts

All scripts are located in `scripts/` directory.

### `start.sh`

Start local development server with live reload:

```bash
./scripts/start.sh
```

### `cite.sh`

Generate citations from sources:

```bash
./scripts/cite.sh
```

### `update_publications.sh`

Update publications from Google Scholar:

```bash
./scripts/update_publications.sh
```

**Requirements:**

- Python 3
- Virtual environment (automatically created)
- Dependencies: `requests`, `beautifulsoup4`

---

## Deployment

### GitHub Pages (Automatic)

The site is automatically deployed to GitHub Pages when changes are pushed to the `main` branch.

**Workflow**: `.github/workflows/deploy.yml`

### Manual Deployment

1. Ensure all changes are committed

2. Push to `main` branch:

   ```bash
   git push origin main
   ```

3. GitHub Actions will build and deploy automatically

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

**Last Updated**: 2026-01-23
