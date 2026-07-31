# File & Directory Conventions

This document defines naming and placement rules for the HARCO LAB site. Follow these when adding new content so the repo stays consistent.

> **Note:** Existing files do not all match these rules yet. The conventions describe the *target* state; older files will be migrated incrementally.

---

## 1. Member slugs

Every member has a canonical **slug** in the form `firstname_lastname` (lowercase ASCII, single underscore). The same slug is used as:

- Member profile filename: `_members/firstname_lastname.md`
- `member:` field value in posts (renders as the link to the member's page)
- Image filename prefix: `firstname_lastname_*`

The `author:` field is the human-readable display name (e.g., `Wansoo Kim`) — it is *not* a slug and is rendered as-is on the post.

### Examples

| Member             | Slug          | Profile file                | Image prefix    |
| ------------------ | ------------- | --------------------------- | --------------- |
| Wansoo Kim         | `wansoo_kim`  | `_members/wansoo_kim.md`    | `wansoo_kim_`   |
| Jungsoo Lee        | `jungsoo_lee` | `_members/jungsoo_lee.md`   | `jungsoo_lee_`  |
| Miseon Jo          | `miseon_jo`   | `_members/miseon_jo.md`     | `miseon_jo_`    |

For non-Korean members, romanize given name first, family name second (e.g. `le_bao`, `kai_li`). Use the romanization the member self-identifies with.

The special value `member: All Member` is reserved for posts that apply to the whole lab (group photos, lab-wide news). Other prose values are accepted but disable the auto-link to a member page.

---

## 2. Posts

All posts live in `_posts/<category>/` and follow Jekyll's required date-prefixed naming:

```text
_posts/<category>/YYYY-MM-DD-<category>_<slug>[_<n>].md
```

| Field        | Rule                                                                     |
| ------------ | ------------------------------------------------------------------------ |
| `<category>` | one of `news`, `research`, `project`, `workshop`                         |
| `YYYY-MM-DD` | ISO date — for research posts, use the publication or post date          |
| `<slug>`     | lowercase ASCII, words separated by `_` (snake_case)                     |
| `<n>`        | optional sequence number when one member has multiple posts of same kind |

Required frontmatter keys:

| Key       | Used by              | Example                       |
| --------- | -------------------- | ----------------------------- |
| `title`   | all                  | `"ICRA 2025"`                 |
| `image`   | most categories      | `images/news/icra2025_1.png`  |
| `author`  | all                  | `Jungsoo Lee` (display name)  |
| `member`  | all                  | `jungsoo_lee` or `All Member` |
| `group`   | all                  | see "Groups" below            |
| `tags`    | research/project     | YAML list                     |

### 2.1 Filename rules

- All-lowercase, snake_case. No spaces, no `.`, no CamelCase, no trailing whitespace.
- For member-tied posts, use the member slug lowercased and joined with `_` (e.g. `jungsoo_lee`, not `jungsoolee` or `JungsooLee`).
- Numbered series: append `_1`, `_2`, … starting from `1` *even for the first post* — do not leave the first one unnumbered if there will be a `_2`.
- For events/seminars, use a short kebab/snake identifier of the event, not a full sentence.

#### Good (posts)

```text
2025-05-22-news_icra2025.md
2025-01-02-research_jungsoo_lee_1.md
2025-01-02-research_jungsoo_lee_2.md
2024-04-01-project_handshaking.md
2025-09-29-news_thomas_kwok_seminar.md
```

#### Avoid (posts)

```text
2025-05-15-news_teachers_day .md             # trailing space
2025-09-29-news_Dr.Thomas M.Kwok_seminar copy.md  # spaces, dots, "copy"
2025-12-22-news_christmas_vedio.md            # typo
2022-04-28-project-khidi_project.md           # hyphen separator (use underscore)
2022-08-01-project-Mobis_MobileManipulator.md # CamelCase
```

### 2.2 Categories vs. groups

The directory determines the *category*. The `group:` frontmatter field is a finer label used by templates for filtering/strips. Pick from the values already in use under `_data/` and `_includes/` rather than inventing new ones.

---

## 3. Images

All images live under `images/<category>/`. The category should match the consumer:

```text
images/members/      # member portraits
images/news/         # news post images
images/research/     # research post images
images/project/      # project post images
images/equipment/    # equipment showcase
images/lab/          # lab/group photos
images/common/       # site chrome (logos, favicons handled separately)
images/main_img/     # homepage hero
images/event_img/    # event banners
```

### 3.1 Filename rules

- All-lowercase ASCII, snake_case.
- Extension lowercase: `.png`, `.jpg`, `.gif` (not `.JPG`, `.PNG`).
- No Korean filenames — use the romanized member slug.
- Member-tied images: `<member-slug-lower>_<n>.png` and `<member-slug-lower>_main.png` for the post's hero image.

#### Good (images)

```text
images/research/jungsoo_lee_1.png
images/research/jungsoo_lee_main.png
images/members/wansoo_kim.jpg
images/news/icra2024_1.jpg
```

#### Avoid (images)

```text
images/members/김완수교수님.png       # Korean filename
images/research/dc_research_2.png   # initials prefix (use full slug)
images/research/keunwoo_main.png    # romanization differs from member slug (Geunwoo)
images/news/IROS_2022_kyoto.jpg     # mixed case
images/christmas.png.sb-...         # editor temp file
```

---

## 4. Data files

`_data/` is for YAML/JSON consumed by Liquid templates. Do not put binary files (xlsx, images) here — they will not render. Move binary source data to `assets/source/` or a more appropriate location and export the relevant fields to YAML/JSON for site consumption.

---

## 5. Adding a new post — checklist

1. Confirm the member slug exists in `_members/`. If not, create the profile first.
2. Add images to `images/<category>/` using the slug-prefixed naming above.
3. Create the post file under `_posts/<category>/` with the dated, snake_case filename.
4. Fill frontmatter (`title`, `image`, `author`, `member`, `group`, `tags` if applicable).
5. Run `bundle exec jekyll build` (or `./scripts/start.sh`) and confirm no warnings.

---

## 6. Migration history

These conventions were introduced on the `chore/cleanup-file-structure` branch and applied incrementally:

- **Phase 1:** Removed stray and broken filenames.
- **Phase 2:** This document.
- **Phase 3:** Renamed posts to snake_case.
- **Phase 4:** Switched member slugs to lowercase + underscore (`Wansoo-Kim` → `wansoo_kim`), renamed Korean image filenames to ASCII, updated all references.
