from __future__ import annotations

from pathlib import Path
from typing import Any


class ResumeBuilder:
    def build(self, profile: dict[str, Any], target_role: str) -> str:
        name = profile.get("name", "Your Name")
        email = profile.get("email", "you@example.com")
        phone = profile.get("phone", "")
        location = profile.get("location", "Remote")
        summary = profile.get("summary", "Applied engineer with strong software and research experience.")
        skills = profile.get("skills", [])
        experience = profile.get("experience", [])
        projects = profile.get("projects", [])

        skill_block = "\n".join(f"\\item {{{skill}}}" for skill in skills)
        experience_block = []
        for item in experience:
            bullets = "\n".join(f"\\item {{{bullet}}}" for bullet in item.get("bullets", []))
            experience_block.append(
                f"\\textbf{{{item.get('title', 'Role')}}} \\hfill {item.get('dates', '')}\\\\n"
                f"\\textit{{{item.get('company', 'Company')}}}\\\\n"
                f"\\begin{{itemize}}\n{bullets}\n\\end{{itemize}}"
            )
        project_block = []
        for item in projects:
            project_block.append(f"\\textbf{{{item.get('name', 'Project')}}}: {item.get('description', '')}\\\\n")

        latex = rf"""\documentclass[11pt]{{article}}
\usepackage[margin=0.6in]{{geometry}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}
\usepackage{{array}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\pagestyle{{empty}}
\begin{{document}}
\begin{{center}}
{{\Large \textbf{{{name}}}}}\\\\n
{email} {phone}\\\\n
{location}\\\\n
\href{{https://www.linkedin.com}}{{LinkedIn}} \quad \href{{https://github.com}}{{GitHub}}
\end{{center}}
\vspace{{0.2cm}}
\noindent\textbf{{Professional Summary}}\\\\n
{summary}\\\\n
\vspace{{0.2cm}}
\noindent\textbf{{Target Role}}: {target_role}\\\\n
\vspace{{0.2cm}}
\noindent\textbf{{Core Skills}}\\\\n
\begin{{itemize}}[leftmargin=*]
{skill_block}
\end{{itemize}}
\vspace{{0.2cm}}
\noindent\textbf{{Experience}}\\\\n
{'\n\n'.join(experience_block) if experience_block else 'No experience provided.'}
\vspace{{0.2cm}}
\noindent\textbf{{Selected Projects}}\\\\n
{'\n'.join(project_block) if project_block else 'No projects provided.'}
\end{{document}}
"""

        return latex

    def write(self, profile: dict[str, Any], target_role: str, output_path: str | Path | None = None) -> Path:
        output_path = Path(output_path or "artifacts/resume.tex")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.build(profile=profile, target_role=target_role), encoding="utf-8")
        return output_path
