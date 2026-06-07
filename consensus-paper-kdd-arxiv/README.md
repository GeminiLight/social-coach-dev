# Consensus Paper - arXiv Working Draft

arXiv-oriented working draft of "Scaling Human-AI Coding Collaboration Requires a Governable Consensus Layer", formatted in ACM sigconf style.

See [`consensus-paper/README.md`](../consensus-paper/README.md) for full paper description.

## Structure

```
main.tex              # Main paper (ACM sigconf format)
main.pdf              # Compiled PDF
review-1/2/3          # Reviewer comments
*.md                  # Draft notes (add_citations, cases, idea, etc.)
```

## Building

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```
