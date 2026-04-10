# job-hunter

A Claude Code skill for filtering job postings and generating tailored, **honest** resumes.

## What it does

1. Reads your master resume + 素材库 (`.docx`) from `~/Desktop/面试/`
2. Captures a JD — pasted text, public URL, or via chrome-devtools-mcp on a logged-in BOSS / 拉勾 / LinkedIn tab
3. Hard-filters against your `preferences.yaml` (city, salary, no 外包, no 996, blacklist keywords)
4. Soft-scores survivors (0–100) across 6 weighted dimensions (tech stack, seniority, domain, role shape, company signal, comp)
5. For roles that pass, **tailors** your resume — never invents skills, never keyword-stuffs
6. Renders the final resume to PDF via [typst](https://typst.app/)
7. Saves everything to `~/Desktop/面试/applications/<company>-<role>-<date>/`

## Why "honest"

A keyword-stuffed resume gets caught in the screening call and wastes a half-day off your week. The skill is built around one rule: **the same person, told differently — not a different person.** Anything not in your master resume or 素材库 doesn't end up in the tailored version. Gaps are surfaced so you can prepare for them, not hidden.

## Setup (one-time)

1. **Install typst** (for PDF rendering — single binary, CJK-friendly, no LaTeX):
   ```bash
   brew install typst
   ```

2. **Make sure your workspace looks like this:**
   ```
   ~/Desktop/面试/                       # or wherever you want
   ├── <your-name>-<role>-<years>.docx  # master resume — REQUIRED
   ├── <your-name>仓库.docx              # 素材库 — OPTIONAL
   ├── preferences.yaml                  # filter + scoring config
   └── applications/                     # auto-created, one folder per JD
   ```

3. **Review `preferences.yaml`** — initial values were inferred from your master resume, but salary floor and city list need a sanity check.

## Using it

Just describe what you want in plain language. Examples:

```text
帮我看看 BOSS 上现在打开的这个岗位
```

```text
这是一个 JD：
[贴文本]
帮我评估并生成简历
```

```text
我浏览器开了 5 个岗位，都过一遍
```

See [`examples/example-prompts.md`](examples/example-prompts.md) for more.

## Files

```
job-hunter/
├── SKILL.md                          # the skill spec Claude reads
├── README.md                         # you are here
├── references/
│   ├── jd-extraction.md              # browser MCP sequence + JD parsing
│   ├── matching-rubric.md            # 6-dimension scoring
│   └── resume-tailoring.md           # tailoring rules + anti-patterns
├── assets/
│   ├── preferences.template.yaml     # blank version for new users
│   └── resume.template.typ           # typst template (CJK-ready, one-page)
├── scripts/
│   ├── read_docx.py                  # stdlib-only .docx text extractor
│   └── render_pdf.py                 # markdown → PDF via typst
└── examples/
    └── example-prompts.md
```

## What it does NOT do

- **Doesn't auto-apply.** It generates the PDF, but you click "submit" yourself. This is intentional — auto-applying to jobs is a great way to get banned and burn your reputation.
- **Doesn't log in to platforms for you.** You log in to BOSS / LinkedIn yourself in Chrome, then point Claude at the open tab.
- **Doesn't fabricate experience.** If the JD asks for K8s and you don't have K8s, the resume will not say you do. The gap goes in the match report instead.
- **Doesn't write to your master resume.** Tailored resumes always go to a new `applications/<slug>/` folder. The master is sacred.

## License

Personal use. The matching rubric and tailoring rules are general enough to fork for other roles — replace `preferences.yaml` and you're 80% there.
