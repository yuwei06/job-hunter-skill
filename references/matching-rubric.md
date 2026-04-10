# Matching Rubric

How to score a JD against the user's background. Hard filters are binary — these are the soft, weighted ones.

## Why scoring exists

The user's time is the bottleneck. The cost of applying to a bad job is not the application itself — it's the wasted screening call, the wasted technical interview, and the emotional drain of getting rejected for something that was never going to fit. A good score means *applying is worth the user's time*, not just "the keywords match".

## Scoring dimensions

Score each dimension 0–100, then take a weighted average. Default weights below — adjust per `preferences.yaml` if the user has set custom ones.

| Dimension | Default weight | What 100 looks like | What 0 looks like |
|---|---|---|---|
| **Tech stack overlap** | 30% | Every primary tech in the JD is in the user's daily-use list | None of the primaries match |
| **Seniority fit** | 20% | JD years and scope match the user's level (±1 year) | JD wants 10 years lead, user has 3 years IC |
| **Domain / industry** | 15% | User has shipped in this exact domain (e.g., 低代码、电商中台、SaaS) | Domain user has never touched and has no transferable analog |
| **Role shape** | 15% | The JD's mix of IC vs lead vs design vs ops matches what user wants | JD is 80% management, user wants pure IC |
| **Company signal** | 10% | Known good company, healthy team size, reasonable funding | Red flags (外包 in disguise, dying product, sketchy reviews) |
| **Compensation upside** | 10% | Salary upper bound is meaningfully above user's current | Salary ceiling is below user's current |

The weights should sum to 100. If the user's preferences.yaml overrides them, validate they still sum to 100 and warn if not.

## Tech stack scoring detail

This is the highest-weight dimension and the easiest to get wrong. Don't just substring-match.

**Counts as a hit** when:
- The JD lists the tech as a *requirement*, not a "加分项"
- The user has *production* experience (not just a tutorial or side project) — verify by checking the master resume and 仓库
- The version matches roughly (Vue 3 ≠ Vue 2 for a JD that explicitly says Vue 3)

**Counts as a partial hit** (50%) when:
- The user has used a sibling technology and the transfer is obvious (React → Preact, Vue 3 → Vue 2, Webpack → Vite)
- The tech is a "加分项" not a hard requirement

**Counts as a miss** when:
- The JD requires it but the user has no real exposure
- The user only knows the name from blog posts

Compute: `tech_score = (hits + 0.5 × partial_hits) / total_required_techs × 100`

## Seniority fit detail

Years on a CV are a weak proxy. What matters more:
- **Scope of work** — owned a system end to end vs. shipped features inside one
- **Cross-team work** — collaborated with backend / design / PM, or pure code monkey
- **Impact metrics** — actual numbers on revenue / latency / users, or just "做了 X"

Compare the JD's expected scope ("独立负责前端架构", "带 3 人小组") against what the user has actually done. A "5 年要求" JD is fine for a 7-year IC if the scope matches; it's wrong if the JD wants a tech lead and the user has never led.

## Hits / gaps output format

After scoring, produce two lists:

**Hits** (concrete evidence the user matches):
- "JD 要求 React + TypeScript：用户主简历项目 X 是 React 18 + TS 全栈"
- "JD 要求 5 年经验：用户 7 年前端"
- "JD 提到低代码平台：用户 仓库.docx 里有完整的低代码平台项目"

**Gaps** (concrete things to flag):
- "JD 要求 K8s 部署经验：用户简历无相关内容"
- "JD 强调英文沟通：未在简历中体现"
- "JD 期望管理过 10 人团队：用户最大带过 3 人"

Be specific. "可能不匹配" is not useful — say what doesn't match.

## Verdict thresholds

| Score | Verdict | What to do |
|---|---|---|
| ≥ 80 | `STRONG_MATCH` | Generate resume immediately, surface in summary |
| 60–79 | `WORTH_APPLYING` | Generate resume, note 1–2 main gaps to prepare for |
| 40–59 | `STRETCH` | Ask the user before generating — it's their call |
| < 40 | `WEAK` | Don't generate by default. Suggest skip. |

## Match report format

Save as `match-report.md` in the application folder:

```markdown
# Match Report — <company> · <role>

**Verdict:** STRONG_MATCH (score 84/100)
**Date:** 2026-04-10

## Summary
<one paragraph explaining the verdict>

## Hard filter
- [x] City (上海 ✓)
- [x] Salary lower bound (35K ≥ 30K ✓)
- [x] Not outsourcing
- [x] Not 996
- [x] No exclude keywords

## Score breakdown
| Dimension | Weight | Score | Notes |
|---|---|---|---|
| Tech stack | 30% | 90 | React, TS, Webpack hit; lacks Rust hint |
| Seniority | 20% | 85 | 7y user vs 5y+ ask, IC scope matches |
| Domain | 15% | 70 | 低代码经验对口，但 SaaS 计费没碰过 |
| Role shape | 15% | 90 | 纯 IC，符合预期 |
| Company | 10% | 80 | A 轮，团队 30 人，技术博客活跃 |
| Compensation | 10% | 75 | 上限 50K，比现职高 |
| **Total** | **100%** | **84** |  |

## Hits
- ...

## Gaps
- ...

## Recommended emphasis for resume
- 把低代码平台项目放第一
- 突出独立负责架构的经历
- ...
```
