# job-search

A modular, local-first autonomous job acquisition platform focused on remote opportunities and interview generation.

## What this phase includes
- rule-based company discovery for globally remote-friendly targets
- profile loading from a local user profile directory
- ATS-oriented LaTeX resume generation
- PDF compilation through pdflatex when available
- tailored outreach email drafting
- a terminal-driven workflow entrypoint backed by SQLite

## Quick start

1. Put your profile context into a folder named user_profile.
2. Run:

```powershell
python -m app.cli --focus "remote ai ml research" --limit 3
```

3. The workflow will:
- discover candidate companies
- write artifacts/resume.tex
- compile artifacts/resume.pdf with pdflatex
- print drafted outreach emails in the terminal

## Notes
- This is intentionally local-first and modular so it can later grow into an automated outreach system with email sending, recruiter tracking, and richer discovery providers.
- The default persistence layer is SQLite, so no separate database server is required.
