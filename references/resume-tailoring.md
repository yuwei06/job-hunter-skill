# Resume Tailoring

How to take the user's master resume + 仓库 and produce a JD-specific version that is *real*, not keyword-stuffed.

## The core principle

A tailored resume is **the same person, told differently** — not a different person.

The user has spent years building actual experience. Tailoring means choosing which of those real experiences to lead with, how to frame them in this particular JD's language, and what evidence to attach. It does not mean inventing anything.

Recruiters and engineers can smell a fake resume. So can ATS systems trained on millions of them. The user's competitive advantage is their *real* track record — protect it.

## What you can do

| Move | Why it's OK |
|---|---|
| **Reorder** sections and bullets | Putting the JD-relevant project first is just being responsive |
| **Reword** to use the JD's vocabulary | "微前端" vs "module federation" — same thing, recruiter scans for one word |
| **Expand** a bullet using detail from 仓库 | The 仓库 has the raw material that didn't fit in the master |
| **Trim** a bullet that's not serving this JD | A 5-line description of an irrelevant project hurts more than it helps |
| **Adjust the headline / summary** | "前端工程师，专注 X" should match the JD's emphasis |
| **Foreground different metrics** | Same project, lead with the metric this JD cares about (perf vs scale vs DX) |
| **Drop a side project** that's irrelevant | Fine to omit, never fine to lie about |

## What you cannot do

| Move | Why it's not OK |
|---|---|
| **Add a skill** the user doesn't have | This is the lie that gets caught in the technical interview |
| **Inflate a title** (Junior → Senior, IC → Lead) | Reference checks exist |
| **Fabricate metrics** ("提升 50%" when there's no measurement) | If the interviewer asks how it was measured, the user is dead |
| **Claim ownership** of someone else's work | Same problem |
| **Stretch dates** to hide gaps | Background checks |
| **Keyword-stuff** an irrelevant skill list | Insults the reader and triggers ATS spam filters |

If you're tempted to do any of these, stop and put the missing item in the **gaps** section of the match report instead. The user can decide whether to study up before the interview, or whether this JD just isn't a fit.

## The tailoring algorithm

1. **Read the match report.** It already tells you which dimensions hit and which don't. Use the hits as the structural skeleton — those go first, big and bold. The gaps tell you what *not* to lean on.

2. **Pick the lead project.** The first project bullet on a resume gets read; the last one usually doesn't. Pick the project from the master resume (or 仓库) that has the strongest overlap with this JD's responsibilities. If two are close, prefer the more recent one.

3. **Rewrite the headline.** One-line professional summary at the top. It should:
   - State years of experience
   - State the user's specialty (frontend, full-stack, etc.)
   - Name 1–2 things from the JD that the user genuinely has
   - Avoid fluff ("热爱技术", "积极主动" — recruiters skip these)

4. **Rewrite each lead project bullet** to use the JD's vocabulary where the underlying meaning is the same. Don't paraphrase if the master resume already says it well — minimum-edit principle.

5. **Pull from 仓库 if needed.** If the master resume's framing of a project is too thin for this JD, look in 仓库.docx for the longer version and lift specific details (numbers, tech choices, problem statements). Cite the source so the user can verify.

6. **Adjust the skills section.** Reorder so the JD's primary techs come first. Don't add anything that wasn't there before. It's fine to break "loosely familiar" out of "core skills" and demote it.

7. **Trim aggressively.** A tailored resume should be shorter than a master resume, not longer. Drop side projects, hobbies, certifications that aren't relevant.

8. **Re-read with the JD next to you.** For every bullet in the resume, ask: "would the recruiter reading this JD care?" If no, drop it.

## Output structure

The tailored resume should follow the user's existing master resume structure (don't reinvent layout — they've iterated on this). Standard sections for a 前端 resume:

```markdown
# Name · Title
联系方式 / 城市 / 求职意向

## 个人概述
<3-4 line summary tailored to this JD>

## 工作经历
### <最近一段经历>
**职位** · 公司 · 时间
- <bullet 1, JD-relevant>
- <bullet 2, JD-relevant>
- ...

### <上一段>
...

## 项目经验
### <对口项目 1>
**角色 / 时间 / 技术栈**
- 背景：...
- 我做了什么：...
- 结果：...（数字优先）

### <对口项目 2>
...

## 技术栈
- 核心：<JD primaries first>
- 熟悉：...
- 了解：...

## 教育背景
...
```

Save as `resume.md` — the typst renderer in `scripts/render_pdf.py` reads this and produces the PDF.

## Tone and length

- **One page is the goal**, two pages is acceptable for a 7-year senior. Three pages is a sign you didn't trim.
- **Concrete > abstract.** "用 React + Webpack 重构构建链路，构建时长 4min → 40s" beats "优化前端构建效率"
- **Active voice.** "主导 X" not "参与 X"
- **No filler adjectives.** Drop 优秀的, 良好的, 扎实的, 丰富的 — they add nothing
- **Use the JD's exact phrasing** for shared concepts when it sounds natural — recruiters scan for it

## Self-check before declaring done

Before saving the resume and rendering to PDF, walk through this checklist:

- [ ] Every claim in this resume is traceable to the master resume or 仓库
- [ ] No skill listed that the user can't speak to in an interview
- [ ] The lead project matches the JD's main domain
- [ ] The headline mentions something specific from the JD
- [ ] No filler adjectives
- [ ] At most one page of content (for typst, that's roughly 60–80 lines of markdown)
- [ ] The tone matches the user's master resume — if the master is reserved, don't suddenly write hype copy

If any of these fail, fix it before rendering.
