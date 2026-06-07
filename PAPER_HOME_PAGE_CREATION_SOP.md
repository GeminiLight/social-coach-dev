# Paper Home Page Creation SOP

## Purpose

This SOP defines a repeatable process for creating a polished research paper home page from a given paper, arXiv link, PDF, figures, project code, and preferred visual style.

The goal is to produce a page that is:

- academically clear and citation-friendly
- visually polished but not design-driven at the cost of readability
- fast, responsive, and deployable as a static site
- discoverable by search engines and AI answer engines
- easy to adapt across styles such as Apple-like, editorial, Linear-style, academic-minimal, dark-tech, or conference-branded

## Required Inputs

Collect these before implementation:

| Input | Required | Notes |
|---|---:|---|
| Paper title | Yes | Use exact title from paper/arXiv. |
| Authors | Yes | Preserve order and spelling. |
| Affiliations | Yes | Use superscripts when there are multiple institutions. |
| Abstract or project summary | Yes | Use author-approved wording when possible. |
| arXiv URL | Preferred | Use the arXiv abstract page as the primary paper link. |
| PDF | Optional | If hosted locally, compress and name predictably. |
| Code URL | Optional | GitHub repository or release URL. |
| BibTeX | Yes | Used for copy citation interaction. |
| Figures/screenshots | Yes | Prefer high-resolution originals, not screenshots from a PDF viewer. |
| Demo media | Optional | Product screenshots, GIF, video, or interactive demo. |
| Visual style | Yes | Example: Apple-like, academic-minimal, editorial, dark-tech, Linear-style. |
| Deployment target | Yes | Example: GitHub Pages branch, custom domain, subpath. |

## Output Files

For a static GitHub Pages site, use this structure:

```text
docs/
  index.html
  styles.css
  script.js
  site.webmanifest
  robots.txt
  sitemap.xml
  llms.txt
  assets/
    paper.pdf
    logo.svg
    icon-192.png
    icon-512.png
    og-image.png
    figure-*.webp
    demo-*.webp
```

Use `docs/` when deploying via GitHub Pages from a project repository. Use the repository root only if the Pages branch is dedicated solely to the site.

## Style Configuration

Choose one style direction before writing CSS. Do not mix multiple visual systems without a reason.

| Style | Best For | Visual Rules |
|---|---|---|
| Apple-like | Product-backed research, demos, mobile apps | Large calm whitespace, soft material, restrained gradients, polished device imagery, minimal text blocks. |
| Academic-minimal | Theory-heavy or conference-first papers | Clear typography, centered paper metadata, neutral palette, strong figure hierarchy, low decoration. |
| Editorial | Research with strong narrative or public-facing story | Larger type contrast, section rhythm, elegant pull statements, careful image placement. |
| Linear-style | Systems papers, tools, infrastructure | Dense but clean layout, quiet borders, precise spacing, monochrome base with one accent. |
| Dark-tech | AI systems, agents, security, robotics | Dark background, luminous diagrams, high contrast, controlled motion, avoid generic purple glow. |
| Conference-branded | Accepted papers or workshop pages | Use conference identity subtly, keep paper title and authors dominant. |

Style requirements:

- The paper title must remain readable before any decorative concern.
- Do not force long academic titles into narrow multi-column layouts.
- If the title is long, use deliberate line breaks rather than accidental wrapping.
- Author and affiliation blocks should usually be centered under the title.
- Section titles should be scannable and not oversized unless they are true hero text.
- Cards are for repeated items, resources, or framed tools; avoid cards inside cards.

## Page Information Architecture

Use this default structure unless the paper requires otherwise:

1. Header
2. Hero / paper identity
3. Core contribution summary
4. Method or system overview
5. Figures / framework
6. Results / evidence
7. Demo or product screenshots
8. Resources
9. Citation
10. Footer

## Header Requirements

Header should include:

- project logo or wordmark
- anchor links: Method, Results, Demo, Resources
- primary paper link

Rules:

- The top paper link should go to the arXiv abstract page when available.
- Do not use "Download PDF" as the main link unless the PDF is the only available source.
- On mobile, hide secondary navigation if it causes crowding.
- Keep the project name visible on desktop; logo-only is acceptable on narrow mobile.

## Hero Requirements

Hero must include:

- full paper title
- authors
- affiliations
- one concise project summary
- actions: arXiv / code / copy BibTeX
- optional key metrics
- optional main visual, demo screenshots, or system preview

Title rules:

- Use the exact title.
- For long titles, author a controlled two-line or three-line layout.
- Avoid narrow columns for titles.
- Do not sacrifice academic readability for visual asymmetry.

Example:

```html
<h1>
  <span>ProjectName: Main Paper Title</span>
  <span>with Secondary Technical Clause</span>
</h1>
```

Author rules:

- Preserve author order.
- Use superscripts for affiliations.
- Keep authors and affiliations visually close to the title.
- Use slightly stronger weight for author names than affiliation names.

## Contribution Summary

Use short, direct claims. Avoid generic marketing copy.

Good examples:

- "A complete coaching loop for soft skills at scale."
- "From expert knowledge to personalized practice."
- "A theory-to-practice structure built for retrieval."
- "Measured across knowledge quality, pathway planning, and product feedback."

Rules:

- Use full-width centered layout for high-level claims.
- Do not split these statements into side-by-side columns unless they are independent cards.
- Keep font size smaller than the hero title.
- Make claims concrete and tied to the paper.

## Figures And Media

Source quality:

- Prefer original figure exports from LaTeX, Figma, Keynote, PowerPoint, or source image files.
- Avoid low-resolution screenshots from PDFs.
- If only a PDF is available, render pages at high DPI before cropping.
- Crop figures tightly but preserve labels and captions.

Recommended processing:

```bash
# Convert high-quality PNG/JPG to WebP.
cwebp -q 82 input.png -o output.webp

# For screenshots or UI images, use slightly higher quality.
cwebp -q 88 input.png -o output.webp
```

If `cwebp` is unavailable, use another reliable image tool, but verify the output visually.

Image rules:

- Use WebP for site figures and screenshots.
- Keep SVG for diagrams only when the SVG is clean, responsive, and not overly complex.
- Use PNG for social sharing images and favicons when compatibility matters.
- Use descriptive `alt` text for all important images.
- Use `loading="lazy"` below the fold.
- Use `loading="eager"` only for first-viewport hero visuals.

Layout rules:

- Related figures may be side by side on desktop.
- Stack related figures on mobile.
- Do not let figure captions become tiny or unreadable.
- Avoid placing important diagrams in decorative frames that shrink the content.

## Logo Requirements

Create a lightweight project logo when the paper does not already have one.

Logo should be:

- symbolic, not generic
- readable at favicon size
- consistent with the page style
- usable as SVG in the header
- exportable to PNG icons and OG image

Recommended logo concepts:

- monogram plus research metaphor
- system loop or pipeline abstraction
- agent, retrieval, practice, evaluation, or feedback motif
- reduced geometric mark based on the paper's core contribution

Avoid:

- random sparkles
- copied conference marks
- overcomplicated diagrams inside the logo
- text-heavy logos
- generic AI purple gradients unless explicitly part of the style

Required assets:

```text
assets/logo.svg
assets/icon-192.png
assets/icon-512.png
assets/og-image.png
```

## Resources Section

Resources should usually include:

- arXiv link
- code link
- citation copy block
- optional AI-readable summary

Recommended wording:

- "Paper, code, citation, and machine-readable project context."
- "Structured links for readers, search engines, and AI research assistants."
- "Use the arXiv page for the paper record; use the repository for code and updates."

Avoid:

- vague claims such as "everything you need"
- overexplaining SEO or AI metadata to normal readers
- making "Download PDF" more prominent than the canonical arXiv page

## Citation Section

Include:

- BibTeX block
- copy button
- citation metadata in `<meta name="citation_*">`

Citation metadata checklist:

```html
<meta name="citation_title" content="..." />
<meta name="citation_author" content="Last, First" />
<meta name="citation_publication_date" content="2026" />
<meta name="citation_conference_title" content="..." />
<meta name="citation_pdf_url" content="..." />
<meta name="citation_keywords" content="..." />
```

Use one `citation_author` tag per author.

## Metadata Requirements

Every page should include:

```html
<title>ProjectName | Short Paper Description</title>
<meta name="description" content="..." />
<meta name="keywords" content="..." />
<meta name="author" content="..." />
<meta name="robots" content="index, follow, max-image-preview:large" />
<link rel="canonical" href="https://example.com/project/" />
<link rel="icon" href="./assets/logo.svg" type="image/svg+xml" />
<link rel="apple-touch-icon" href="./assets/icon-192.png" />
<link rel="manifest" href="./site.webmanifest" />
```

Open Graph:

```html
<meta property="og:type" content="website" />
<meta property="og:site_name" content="ProjectName" />
<meta property="og:title" content="..." />
<meta property="og:description" content="..." />
<meta property="og:url" content="https://example.com/project/" />
<meta property="og:image" content="https://example.com/project/assets/og-image.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="..." />
```

Twitter/X:

```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="..." />
<meta name="twitter:description" content="..." />
<meta name="twitter:image" content="https://example.com/project/assets/og-image.png" />
```

Structured data:

- Use `ScholarlyArticle` for the paper.
- Use `SoftwareSourceCode` if there is a repository.
- Use `FAQPage` only when the FAQ contains real, useful answers.

Minimum JSON-LD:

```json
{
  "@context": "https://schema.org",
  "@type": "ScholarlyArticle",
  "headline": "Exact Paper Title",
  "name": "ProjectName",
  "description": "One-sentence paper summary.",
  "datePublished": "2026",
  "isAccessibleForFree": true,
  "url": "https://example.com/project/",
  "image": "https://example.com/project/assets/og-image.png",
  "author": [
    {
      "@type": "Person",
      "name": "Author Name",
      "affiliation": "Institution"
    }
  ],
  "keywords": ["keyword 1", "keyword 2"]
}
```

## AI-Readable Files

Create `llms.txt` for AI answer engines and research assistants.

Include:

- project title
- canonical URL
- arXiv URL
- code URL
- one-paragraph summary
- core claims
- resource links
- citation

Keep it factual. Do not use marketing language.

Create `robots.txt`:

```text
User-agent: *
Allow: /

Sitemap: https://example.com/project/sitemap.xml
```

Create `sitemap.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/project/</loc>
  </url>
</urlset>
```

## Web Manifest

Use:

```json
{
  "name": "ProjectName",
  "short_name": "ProjectName",
  "description": "Short project description.",
  "start_url": "./",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#111111",
  "icons": [
    {
      "src": "./assets/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "./assets/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ]
}
```

## Implementation Checklist

Before coding:

- Confirm paper title, authors, affiliations, and links.
- Confirm visual style.
- Confirm deployment URL and subpath.
- Gather original figures or high-resolution exports.
- Decide whether PDF is hosted locally or linked externally.

During coding:

- Build `index.html`, `styles.css`, and optional `script.js`.
- Use semantic sections and accessible labels.
- Use a responsive title layout.
- Add buttons for arXiv, code, and BibTeX copy.
- Add optimized WebP assets.
- Add logo, icons, and OG image.
- Add citation metadata, Open Graph, Twitter metadata, JSON-LD, manifest, sitemap, robots, and `llms.txt`.

After coding:

- Open the page locally.
- Check desktop and mobile screenshots.
- Check all links.
- Check image loading.
- Check copy BibTeX.
- Validate JSON files.
- Validate JSON-LD parsing.
- Check that no long title or metric card causes horizontal overflow.

## Local Verification Commands

Run a local static server:

```bash
python3 -m http.server 4173 --directory docs
```

Validate manifest:

```bash
python3 -m json.tool docs/site.webmanifest >/dev/null
```

Check metadata:

```bash
rg -n "canonical|og:image|twitter:image|citation_|application/ld\\+json|llms.txt" docs
```

Check asset sizes:

```bash
ls -lh docs/assets
```

Check for broken local references:

```bash
rg -n "src=|href=" docs/index.html
```

Use browser screenshots for at least:

- desktop: 1440 px wide
- tablet: 768 px wide
- mobile: 390 px or 430 px wide

## Design QA Checklist

Typography:

- Paper title is readable and not overly fragmented.
- Authors and affiliations are close to the title.
- Section headings are smaller than the hero title.
- Text does not overflow buttons, cards, or figure captions.

Layout:

- No horizontal scrolling on mobile.
- Header does not crowd on mobile.
- Related figures align well on desktop and stack on mobile.
- Hero leaves enough context below the fold when possible.

Visual quality:

- Logo reads at small sizes.
- OG image has no overlapping text.
- Figures are sharp and not visibly upscaled.
- Palette is not a generic one-note AI gradient.
- Visual style supports the paper rather than distracting from it.

Performance:

- Large figures are WebP.
- Hero images are not unnecessarily huge.
- Below-fold images use lazy loading.
- Local PDF is compressed if hosted.

Metadata:

- Canonical URL matches deployment URL.
- OG image URL is absolute.
- Twitter image URL is absolute.
- Manifest icons exist.
- JSON-LD is valid JSON.
- `robots.txt`, `sitemap.xml`, and `llms.txt` use the final public URL.

## Deployment SOP For GitHub Pages

If deploying from `docs/` on the main branch:

1. Commit the site.
2. Configure GitHub Pages source as `main` branch `/docs`.
3. Verify the Pages URL.

If deploying to a dedicated `gh-pages` branch:

```bash
DEPLOY_COMMIT=$(git commit-tree HEAD:docs -m "Deploy paper home page")
git branch -f gh-pages "$DEPLOY_COMMIT"
git push origin gh-pages:gh-pages --force-with-lease
```

If deploying to a different repository:

```bash
DEPLOY_COMMIT=$(git commit-tree HEAD:docs -m "Deploy paper home page")
git branch -f gh-pages "$DEPLOY_COMMIT"
git push https://github.com/OWNER/REPO.git gh-pages:gh-pages --force-with-lease
```

After deployment:

```bash
curl -s -L "https://example.com/project/" | rg -n "canonical|og:image|twitter:image|logo|manifest"
curl -I -L "https://example.com/project/assets/og-image.png"
```

If the site uses a CDN or custom domain, wait for cache invalidation or use a query parameter:

```bash
curl -s -L "https://example.com/project/?v=COMMIT_SHA"
```

## Acceptance Criteria

The page is ready when:

- The live URL loads successfully.
- Paper title, authors, affiliations, arXiv link, code link, and citation are correct.
- The design matches the requested style.
- Images are sharp and optimized.
- Logo appears in the header and browser metadata.
- OG preview image is available at a public absolute URL.
- Citation metadata and JSON-LD are present.
- `llms.txt`, `robots.txt`, and `sitemap.xml` are present.
- Desktop and mobile layouts have no obvious overlap or horizontal overflow.
- GitHub Pages or the target hosting platform reports a successful build.

## Reuse Template

Use this short project brief to start each new paper page:

```text
Paper title:
Authors:
Affiliations:
arXiv URL:
PDF URL or local PDF:
Code URL:
BibTeX:
Conference or venue:
Preferred style:
Deployment URL:
Key contributions:
Main figures:
Demo assets:
Special requirements:
```

## Recommended Default

When no style is specified, use academic-minimal with a light, polished product-research feel:

- neutral off-white background
- one accent color
- centered paper title, authors, and affiliations
- large but readable title
- full-width contribution summary
- figure-first method/results sections
- arXiv as the primary paper link
- GitHub as the primary code link
- custom lightweight logo only if the project name benefits from it
