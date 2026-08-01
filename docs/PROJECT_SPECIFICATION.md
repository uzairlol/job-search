# PROJECT: AUTONOMOUS AI JOB ACQUISITION AGENT (AJA)

You are the lead software architect for a production-grade autonomous AI system whose only objective is:

> Maximize the probability of landing interviews and ultimately securing remote AI / Machine Learning / Data Science / Research Engineering positions worldwide.

This is NOT a chatbot.

This is NOT a resume builder.

This is NOT a job scraper.

This is an autonomous multi-agent platform that continuously searches for opportunities, researches companies, evaluates fit, customizes application materials, performs outreach, tracks responses, learns from outcomes, and continuously improves.

Think of this as building an autonomous sales pipeline where **the product being sold is the candidate**.

The system must be modular, scalable, highly testable, event-driven, locally executable, and designed to run continuously.

The user is willing to dedicate significant compute resources and storage. Paid SaaS products should be avoided wherever possible. Favor open-source software.

=================================================================

PRIMARY OBJECTIVE

=================================================================

The system optimizes ONE metric:

Expected Interview Value

NOT

Number of Applications

Applications are cheap.

Interviews are valuable.

Every design decision must maximize interview probability.

=================================================================

SECONDARY OBJECTIVES

=================================================================

• Produce truthful resumes.

• Never hallucinate achievements.

• Continuously discover new companies.

• Discover companies before they advertise jobs.

• Discover hidden hiring opportunities.

• Minimize duplicate applications.

• Continuously learn from previous applications.

• Rank opportunities intelligently.

• Maintain complete audit logs.

=================================================================

TECH STACK

=================================================================

Python 3.13

PostgreSQL

SQLAlchemy

Alembic

FastAPI

Playwright

Docker

Redis

Celery or Temporal

Sentence Transformers

FAISS

Local LLM (DeepSeek R1 / Qwen / Llama)

Ollama or vLLM

Markdown

Jinja2

Pydantic

BeautifulSoup

Trafilatura

Readability

httpx

PyMuPDF

Git

Pytest

Rich

Typer

Loguru

=================================================================

PROJECT STRUCTURE

=================================================================

Everything must be modular.

No giant files.

No god classes.

No duplicated logic.

Use dependency injection.

Everything configurable.

Use interfaces.

Each agent must have one responsibility.

=================================================================

DATABASE

=================================================================

PostgreSQL is the source of truth.

Tables should include (expand significantly):

Companies

Jobs

Recruiters

Employees

Applications

Emails

Email Threads

Resume Versions

Resume Blocks

Projects

Skills

Experiences

Achievements

Research Papers

GitHub Repositories

Publications

Certificates

Documents

Markdown Notes

Embeddings

Follow Ups

Interview Stages

Interview Notes

Offers

Rejections

Analytics

Crawler Sources

Crawler History

Company Research

Hiring Signals

ATS Systems

Company Scores

Application Scores

Agent Logs

System Logs

Every object should be versioned.

Nothing should ever be deleted.

=================================================================

PERSONAL KNOWLEDGE BASE

=================================================================

Create a directory

/user_profile/

The user will continuously dump files here.

Support:

Markdown

PDF

DOCX

TXT

Latex

JSON

CSV

GitHub README

Every document should be parsed.

Embedded.

Tagged.

Broken into chunks.

Linked to entities.

Examples

Internships

Projects

Research papers

Awards

Blog posts

Resume versions

LinkedIn exports

Github repositories

Public speaking

Everything.

Create a semantic graph.

Never fabricate facts.

Every generated sentence must reference retrieved facts.

=================================================================

COMPANY DISCOVERY

=================================================================

This is the heart of the project.

DO NOT ONLY SCRAPE LINKEDIN.

The objective is to discover every company on Earth that could realistically hire remotely.

Think globally.

Search continuously.

Potential discovery sources include (but are not limited to):

Y Combinator

Techstars

500 Global

Sequoia Portfolio

Andreessen Horowitz Portfolio

General Catalyst

Accel

NFX

Antler

OpenAI Startup Fund

RemoteOK

Wellfound

We Work Remotely

Himalayas

Otta

Arc

Greenhouse

Lever

Ashby

Workable

SmartRecruiters

BambooHR

Workday

GitHub Organizations

GitLab Organizations

HuggingFace Organizations

Research Labs

Government AI Labs

Defense Contractors

Climate Tech Companies

Bioinformatics

Robotics Companies

Computer Vision Companies

Satellite Companies

Economic Consulting Firms

Think Tanks

NGOs

Universities

University Spinouts

Conference Sponsors

Conference Speakers

Kaggle Competitions

OSS Foundations

Engineering Blogs

AI News

Funding announcements

New startup launches

Crunchbase alternatives

Product Hunt launches

HN Who's Hiring

RSS feeds

AI newsletters

Open-source maintainers

Research authors

Build discovery strategies.

Score discovery quality.

Continuously add new sources.

=================================================================

COMPANY RESEARCH

=================================================================

Once discovered:

Research aggressively.

Collect:

Products

Mission

Funding

Revenue estimates

Tech stack

Cloud providers

Languages

ML stack

Open source repos

Engineering blogs

Founders

Executives

Recruiters

Hiring managers

Employee count

Hiring velocity

Remote policy

Glassdoor

GitHub

Papers

Patents

Recent news

Conference talks

Documentation

API docs

Everything publicly available.

Generate a company intelligence report.

=================================================================

JOB DISCOVERY

=================================================================

Some companies advertise jobs.

Some don't.

If no job exists:

Detect hiring signals.

Examples:

Rapid growth

Funding

New engineering blog

Massive GitHub activity

New offices

New ML projects

Research publications

New products

Assume proactive outreach may outperform waiting.

=================================================================

MATCHING ENGINE

=================================================================

Evaluate:

Technical fit

Research fit

Industry fit

Career growth

Salary

Remote compatibility

Time zone

Likelihood of interview

Likelihood of offer

Personal interest

Generate scores.

Explain reasoning.

=================================================================

RESUME ENGINE

=================================================================

Do NOT write resumes from scratch.

Retrieve facts.

Rank relevance.

Construct resume.

Validate every bullet.

Measure ATS compatibility.

Export PDF.

Export DOCX.

Version everything.

=================================================================

EMAIL ENGINE

=================================================================

Every email must be unique.

Never generic.

Mention specific company research.

Reference engineering blogs.

Reference repositories.

Reference research.

Reference founders.

Reference products.

Reference hiring trends.

Maximum personalization.

=================================================================

APPLICATION ENGINE

=================================================================

Prefer APIs.

Use browser automation only if necessary.

Track failures.

Retry intelligently.

Capture screenshots.

Log everything.

=================================================================

FOLLOW UPS

=================================================================

Automatically determine when follow-up is appropriate.

Generate different wording.

Never send duplicate messages.

=================================================================

INTERVIEW AGENT

=================================================================

When interview scheduled:

Research interviewer.

Research company.

Generate briefing.

Generate technical questions.

Generate behavioral questions.

Generate mock interview.

Generate suggested questions.

=================================================================

ANALYTICS

=================================================================

Dashboard.

Track:

Applications

Replies

Interview rate

Offer rate

Industry response

Resume performance

Email performance

Company response

Country response

Average response time

Everything visualized.

=================================================================

LEARNING LOOP

=================================================================

Every outcome updates future decisions.

Rejected?

Determine why.

Interview?

Increase similar applications.

No reply?

Evaluate resume.

Evaluate email.

Evaluate company selection.

Continuously improve.

=================================================================

CODING REQUIREMENTS

=================================================================

Strict typing.

Pydantic models.

100% modular.

Unit tests.

Logging.

Retry logic.

Rate limiting.

Caching.

Configuration files.

No hardcoded secrets.

.env support.

Docker Compose.

CI ready.

GitHub Actions.

Everything documented.

=================================================================

IMPORTANT

=================================================================

Do NOT simplify.

Do NOT use placeholders.

Build this as if it were a venture-backed startup expected to process millions of companies over multiple years.

Whenever uncertainty exists, choose the architecture that is:

more modular

more scalable

more testable

more observable

more maintainable

Assume future features will include:
- multiple users
- distributed workers
- autonomous planning
- reinforcement learning from application outcomes
- graph databases
- knowledge graphs
- voice interview preparation
- recruiter relationship management
- portfolio generation
- personal website generation
- LinkedIn optimization
- GitHub optimization
- automated networking
- referral discovery
- conference discovery
- scholarship discovery
- fellowship discovery

Your responsibility is not merely to write code.

Your responsibility is to design and implement an autonomous career acquisition platform that systematically maximizes the user's probability of securing world-class AI/ML opportunities.