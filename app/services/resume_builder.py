from __future__ import annotations

from pathlib import Path
from typing import Any


class ResumeBuilder:
    def _escape_latex(self, value: Any) -> str:
        text = "" if value is None else str(value)
        return (
            text.replace("\\", r"\textbackslash{}")
            .replace("&", r"\&")
            .replace("%", r"\%")
            .replace("$", r"\$")
            .replace("#", r"\#")
            .replace("_", r"\_")
            .replace("{", r"\{")
            .replace("}", r"\}")
            .replace("~", r"\textasciitilde{}")
            .replace("^", r"\textasciicircum{}")
        )

    def build(self, profile: dict[str, Any], target_role: str) -> str:
        name = self._escape_latex(profile.get("name", "Your Name"))
        email = self._escape_latex(profile.get("email", "you@example.com"))
        phone = self._escape_latex(profile.get("phone", ""))
        location = self._escape_latex(profile.get("location", "Remote"))
        summary = self._escape_latex(profile.get("summary", "Applied engineer with strong software and research experience."))
        skills = [self._escape_latex(skill) for skill in profile.get("skills", [])]
        experience = profile.get("experience", [])
        projects = profile.get("projects", [])

        skill_block = "\n".join(f"\\item {{{skill}}}" for skill in skills)
        experience_block = []
        for item in experience:
            bullets = "\n".join(f"\\item {{{self._escape_latex(bullet)}}}" for bullet in item.get("bullets", []))
            experience_block.append(
                f"\\textbf{{{self._escape_latex(item.get('title', 'Role'))}}} \\hfill {self._escape_latex(item.get('dates', ''))}\\\\n"
                f"\\textit{{{self._escape_latex(item.get('company', 'Company'))}}}\\\\n"
                f"\\begin{{itemize}}\n{bullets}\n\\end{{itemize}}"
            )
        project_block = []
        for item in projects:
            project_block.append(f"\\textbf{{{self._escape_latex(item.get('name', 'Project'))}}}: {self._escape_latex(item.get('description', ''))}\\\\n")

        target_role_escaped = self._escape_latex(target_role)

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
{{\Large \textbf{{{name}}}}}\\
{email} {phone}\\
{location}\\
\href{{https://www.linkedin.com}}{{LinkedIn}} \quad \href{{https://github.com}}{{GitHub}}
\end{{center}}
\vspace{{0.2cm}}
\noindent\textbf{{Professional Summary}}\\
{summary}\\
\vspace{{0.2cm}}
\noindent\textbf{{Target Role}}: {target_role_escaped}\\
\vspace{{0.2cm}}
\noindent\textbf{{Core Skills}}\\
\begin{{itemize}}[leftmargin=*]
{skill_block}
\end{{itemize}}
\vspace{{0.2cm}}
\noindent\textbf{{Experience}}\\
{'\n\n'.join(experience_block) if experience_block else 'No experience provided.'}
\vspace{{0.2cm}}
\noindent\textbf{{Selected Projects}}\\
{'\n'.join(project_block) if project_block else 'No projects provided.'}
\end{{document}}
"""

        return latex

    def write(self, profile: dict[str, Any], target_role: str, output_path: str | Path | None = None) -> Path:
        output_path = Path(output_path or "artifacts/resume.tex")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.build(profile=profile, target_role=target_role), encoding="utf-8")
        return output_path
