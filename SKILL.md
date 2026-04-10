---
name: job-hunter
description: Filter job postings against the user's hard/soft criteria and generate a tailored, evidence-based PDF resume for each promising role. Use this whenever the user mentions job hunting, evaluating a JD (job description), 招聘信息, 投简历, "帮我看看这个岗位", "改一下简历", BOSS 直聘, 智联, 拉勾, 51job, LinkedIn, or wants to score how well a posting matches their background. Reads the user's master resume and 素材库 from ~/Desktop/面试/, can use chrome-devtools-mcp to capture JDs from the user's logged-in browser, scores against preferences.yaml, and emits a per-application folder containing the JD snapshot, a match report, and a tailored PDF resume.
user-invocable: true
---

# Job Hunter

Help the user evaluate job postings and produce a tailored resume for each promising one. The user is a working professional with limited time — every minute spent on a bad-fit role is wasted, and every generic resume is a wasted shot.

The skill has two jobs:

1. **Filter ruthlessly.** Most postings are not worth applying to. Reject them fast and explain why.
2. **Tailor honestly.** For postings that pass, generate a resume that highlights the user's *real* matching experience — never invent skills, never keyword-stuff.

## Workspace

Everything lives in `~/Desktop/面试/`:

```
~/Desktop/面试/                    # or any folder the user prefers
├── <name>-<role>-<years>.docx    # master resume — REQUIRED
├── <name>仓库.docx                # 素材库 (story pool) — OPTIONAL but recommended
├── 面试问题及回答.docx            # interview Q&A reference — OPTIONAL
├── preferences.yaml              # hard + soft criteria, never goes into the resume — REQUIRED
└── applications/
    └── <company>-<role>-<YYYY-MM-DD>/
        ├── jd.md                 # captured JD text
        ├── match-report.md       # score, hits, gaps, verdict
        ├── resume.md             # tailored resume markdown
        └── resume.pdf            # rendered PDF
```

Only the master resume and `preferences.yaml` are strictly required. If a 仓库 file is missing, work from the master alone — most of the user's material is usually already in the master, and the 仓库 is a bonus source for adapting to unusual JDs.

The skill auto-discovers the master resume by globbing `~/Desktop/面试/*.docx` and picking the most recent one that doesn't have "仓库" in the filename. If the user keeps their workspace elsewhere, ask once and remember.

If `preferences.yaml` doesn't exist, copy `assets/preferences.template.yaml` from this skill into the workspace and ask the user to fill it in before going further. Without preferences there's no way to filter.

## Workflow

The skill runs as a pipeline. Don't skip steps unless the user tells you to.

### Step 1 — Load context

Read these files (in order, lazily — don't read 仓库 until you actually need it):

1. `~/Desktop/面试/preferences.yaml` — hard vetoes and soft scoring weights (required)
2. The most recent `*.docx` in the workspace that doesn't contain "仓库" in its name — master resume, the canonical statement of what's already been polished (required)
3. The `*仓库.docx` file, if it exists — 素材库, only when you need a detail not in the master resume (optional — skip silently if missing)

To read .docx files, run `scripts/read_docx.py <path>` — it returns clean text without needing python-docx.

### Step 2 — Capture the JD

The user will hand you a JD in one of three ways. Detect which:

- **Pasted text** — they paste the posting directly. Just use it.
- **URL to a public page** — try WebFetch first. If the page is behind a login (BOSS 直聘, 智联, LinkedIn, 拉勾), fall back to browser MCP.
- **"the page I have open" / "this BOSS link"** — use chrome-devtools-mcp. The user's Chrome should already be open and logged in.

For the browser MCP path, see `references/jd-extraction.md` for the exact tool sequence. Briefly:

1. `mcp__plugin_chrome-devtools-mcp_chrome-devtools__list_pages` to find the right tab
2. `select_page` then `take_snapshot` to get the rendered DOM
3. Pull the JD text out of the snapshot — title, company, salary, location, requirements, responsibilities

Save the cleaned JD as `applications/<slug>/jd.md` with this front section so the match report can reference it:

```markdown
---
company: 字节跳动
role: 高级前端工程师
location: 上海
salary: 30-50K·15薪
source_url: https://...
captured_at: 2026-04-10
---

## 岗位职责
...

## 任职要求
...
```

The slug is `<company>-<role>-<date>`, romanized or kept in Chinese — whichever the user prefers, default to Chinese.

### Step 3 — Hard filter (vetoes)

Read `preferences.yaml`. For every key under `hard:`, check whether the JD violates it. Hard rules are veto rules — *one violation kills the application*.

Typical hard rules and how to detect them:

| Rule | What to look for in the JD |
|---|---|
| `cities` (whitelist) | Posting location must be in this list. Remote-friendly counts if `remote_ok: true` |
| `salary_min` | Posting's lower bound must meet this. If salary is hidden, mark as `unknown` and ask the user |
| `no_outsourcing` | Reject if 外包/驻场/乙方/人力外包 appears, or company name is a known outsourcing vendor |
| `no_996` | Reject if 996/大小周/单休/弹性 in a way that signals long hours |
| `exclude_keywords` | Free-form blacklist (e.g., "Vue2", "jQuery", "传统行业") |

If anything trips, write a `match-report.md` with `verdict: REJECTED`, list the violated rules, and **stop**. Don't generate a resume for rejected postings — that wastes the user's time and tokens.

### Step 4 — Soft scoring

If the JD survives the hard filter, score it on the soft dimensions. Use `references/matching-rubric.md` for the scoring scheme. The output is:

- **Overall match score** (0–100)
- **Per-dimension breakdown** (tech stack, domain, seniority, company size, etc.)
- **Hits** — concrete things in the user's background that match the JD
- **Gaps** — things the JD asks for that the user doesn't clearly have
- **Verdict** — `STRONG_MATCH` (≥80), `WORTH_APPLYING` (60–79), `STRETCH` (40–59), `WEAK` (<40)

Save this as `match-report.md`. Show the user the verdict and per-dimension scores in your reply, and ask whether to generate the tailored resume. Don't just barrel ahead — the user might want to skim the rubric first or skip resume generation for `WEAK` matches.

### Step 5 — Tailor the resume

Only do this if the user confirms (or if the prompt clearly says "score AND generate"). Read `references/resume-tailoring.md` for the rules. The short version:

1. Start from the master resume — never from a blank page
2. Reorder bullets so the most JD-relevant ones come first
3. Pull stronger evidence from 仓库.docx if the master resume's framing is too generic for this JD
4. Adjust the headline / summary line to reflect the JD's emphasis (e.g., "low-code platform" vs "data viz")
5. Remove or downplay sections that don't help this JD (within reason — never lie about experience by hiding it, but it's fine to drop one sentence about a side project that's irrelevant)
6. **Never invent**: no skills the user doesn't have, no inflated job titles, no fake metrics

Write the result as `resume.md` first. This is the source of truth — the PDF is just a render of it.

### Step 6 — Render to PDF

Run `scripts/render_pdf.py applications/<slug>/resume.md`. It will:

1. Check that `typst` is installed; if not, tell the user to `brew install typst` and stop
2. Pipe the markdown into the typst template at `assets/resume.template.typ`
3. Output `resume.pdf` next to the markdown

The typst template handles CJK fonts, page breaks, and styling. Don't write your own PDF generator.

### Step 7 — Report back

Tell the user:
- Verdict and score
- Where the files are (`~/Desktop/面试/applications/<slug>/`)
- One-sentence summary of what you adjusted in the resume vs. the master
- Top 1–2 gaps to be ready for in an interview

Be concise. The user is in the middle of job hunting, not reading a report.

## Working in batches

If the user says "look at these 5 BOSS jobs I have open", do them in parallel where possible:
- Capture all 5 JDs first (browser MCP one tab at a time, but JD extraction can be sequential and fast)
- Run the hard filter on all 5 in one pass
- For survivors, ask the user "3 of 5 passed the filter, generate resumes for all 3?"
- Generate resumes one at a time (each one needs its own tailoring decisions)

Always show a summary table at the end: `company | role | salary | verdict | score`.

## What to avoid

- **Don't fabricate experience.** If the JD asks for K8s and the user has never touched K8s, the resume must not say they have. Mark it as a gap instead.
- **Don't keyword-stuff.** Keyword-stuffed resumes get flagged by humans and ATS both. Use the user's real language.
- **Don't generate a resume for a rejected JD.** That's the entire point of hard filtering.
- **Don't ignore the 仓库.** It exists because the master resume is a *summary*. The 仓库 has the raw material for adapting to specific JDs — use it.
- **Don't write to the master resume file.** Tailored resumes always go to a new `applications/<slug>/` folder. The master is sacred.
- **Don't ask 20 clarifying questions before starting.** If `preferences.yaml` is missing, ask once. Otherwise, make reasonable defaults and ship a draft the user can correct.

## Bilingual behavior

The user is a Chinese-speaking frontend engineer. Default to Chinese for all conversation, match reports, and resume content. If the JD is in English (e.g., a foreign company), generate the resume in English to match the JD language — recruiters at English-speaking companies expect English resumes.

## References

- `references/jd-extraction.md` — exact browser-MCP sequence and JD parsing
- `references/matching-rubric.md` — scoring dimensions and weights
- `references/resume-tailoring.md` — tailoring principles and anti-patterns
- `assets/preferences.template.yaml` — preferences schema with examples
- `assets/resume.template.typ` — typst template for PDF rendering
- `scripts/read_docx.py` — stdlib-only docx text extractor
- `scripts/render_pdf.py` — markdown → PDF via typst
