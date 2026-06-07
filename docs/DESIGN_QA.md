# SocialCoach Project Page Design QA

Date: 2026-06-07

## Design Direction

Research project page for a technical AI/education audience. The visual system uses a crisp research-product language: neutral paper background, graphite typography, a single teal accent, real EQoach screenshots, restrained glass material, and dense evidence sections for researchers and search/AI retrieval systems.

## Five Optimization Rounds

1. Information architecture
   - Prioritized paper actions, authorship/citation metadata, method, evidence, product demo, and BibTeX.
   - Replaced generic landing-page feature cards with a research reading path.

2. Desktop hero refinement
   - Initial H1 was too long and pushed the first content section below the viewport.
   - Changed the H1 to the brand signal `SocialCoach` and moved the full paper title into supporting copy and metadata.

3. Mobile first-viewport refinement
   - Initial mobile hero was too tall because product visuals consumed vertical layout space.
   - Removed the mobile hero visual from layout flow and kept metrics compact so the next section is visible.

4. Readability and visual polish
   - Fixed desktop H1 word breaking by disabling arbitrary word breaks on the display heading and reducing max display size.
   - Checked button text, metric tiles, visual hierarchy, and line lengths across desktop and mobile.

5. SEO/GEO and rendering QA
   - Added canonical, Open Graph, Twitter Card, citation metadata, JSON-LD, sitemap, robots.txt, manifest, and llms.txt.
   - Verified local HTTP serving, PDF response, image loading, no horizontal overflow, visible next section, and unclipped buttons with Playwright.

## Verification Evidence

- Desktop viewport: 1440 x 1100.
- Mobile viewport: 390 x 844.
- All images loaded successfully after scroll inspection.
- Desktop and mobile both expose the next section within the first viewport.
- No horizontal overflow detected.
- No clipped button text detected.
- JSON-LD parsed successfully with `ScholarlyArticle`, `SoftwareSourceCode`, and `FAQPage` graph nodes.
- `llms.txt`, `robots.txt`, `sitemap.xml`, and PDF asset return HTTP 200 locally.
