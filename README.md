# job-search

A modular, local-first platform for discovering remote-friendly companies, tailoring resumes to each target, and preparing outreach drafts without depending on cloud services.

## What it does

- discovers company targets using a rule-based, prompt-driven workflow
- loads profile context from a local profile directory
- generates ATS-oriented LaTeX resumes
- compiles resumes to PDF locally with pdflatex when available
- writes separate artifact folders for each company target so resumes are not overwritten
- drafts personalized outreach emails
- stores lightweight structured data in SQLite by default

## Project structure

- app/cli.py — terminal entrypoint
- app/services/ — discovery, resume generation, emailing, and orchestration services
- app/infrastructure/database/ — SQLite-backed persistence layer
- app/prompts/ — prompt templates for discovery and outreach
- user_profile/ — place your resume, notes, and supporting context here
- storage/artifacts/ — generated runs, resumes, and manifest files

## Quick start

1. Add your profile context to the folder named user_profile.
2. Run:

```powershell
python -m app.cli --focus "remote ai ml research" --limit 3
```

3. The workflow will:
   - discover candidate companies
   - create a separate artifact folder per company
   - generate and compile a resume for each target
   - save a manifest describing the generated artifacts
   - draft outreach emails for the selected companies

## Configuration

The app uses a local SQLite database by default. You can override the storage path with the DATABASE_URL environment variable if needed.

## Notes

- This project is intentionally local-first and modular so it can evolve into a more automated outreach system later.
- The default persistence layer is SQLite, so no separate database server is required.
- If pdflatex is unavailable, the workflow still writes the LaTeX source and skips PDF compilation.
