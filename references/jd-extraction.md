# JD Extraction

How to get a clean job description into the workspace, regardless of where it lives.

## Three input modes

### Mode A — Pasted text

Easiest case. The user pastes a JD blob directly. Just clean it up and save it.

Cleanup steps:
1. Strip platform UI noise (按钮文案、"立即沟通"、"投递简历"、客服话术、推荐岗位)
2. Normalize whitespace
3. Try to identify these fields even if they're scattered: company name, role title, location, salary, work model (远程/坐班/混合), 学历要求, 工作年限, 岗位职责, 任职要求

Save with frontmatter as described in SKILL.md step 2.

### Mode B — Public URL

Use WebFetch first. It works for company career pages, smaller job boards, and most overseas sites.

If WebFetch returns a login wall, an empty page, or "请登录后查看", **don't retry** — switch to Mode C.

Known platforms that need login (skip WebFetch, go straight to Mode C):
- BOSS 直聘 (zhipin.com)
- 拉勾 (lagou.com)
- 智联招聘 (zhaopin.com)
- 51job (51job.com)
- 猎聘 (liepin.com)
- LinkedIn (linkedin.com — even public JDs often need login from China)

### Mode C — Browser MCP (chrome-devtools-mcp)

This is the path for any logged-in platform. **Precondition: the user already has Chrome open and is logged in to the platform.** If they're not, ask them to log in first — don't try to automate the login flow.

#### Tool sequence

1. **`mcp__plugin_chrome-devtools-mcp_chrome-devtools__list_pages`**
   Lists all open Chrome tabs. Find the one with the JD — match by URL pattern (`zhipin.com/job_detail`, `lagou.com/jobs`, etc.) or by title.

2. **`mcp__plugin_chrome-devtools-mcp_chrome-devtools__select_page`**
   Switch to the right tab.

3. **`mcp__plugin_chrome-devtools-mcp_chrome-devtools__take_snapshot`**
   Returns a structured DOM snapshot. This is usually enough to read the JD off — most platforms put the title, salary, requirements, and responsibilities in plain text divs.

4. **(Optional) `evaluate_script`**
   If the snapshot is messy or paginated, run a small JS snippet against `document.querySelector` to grab the right section. Example for BOSS 直聘:
   ```js
   ({
     title: document.querySelector('.job-name')?.innerText,
     salary: document.querySelector('.salary')?.innerText,
     company: document.querySelector('.company-name')?.innerText,
     location: document.querySelector('.location-address')?.innerText,
     requirements: document.querySelector('.job-detail-section')?.innerText,
   })
   ```
   Selectors change — if one fails, take a fresh snapshot and look at the actual DOM rather than guessing.

5. **(Optional) `take_screenshot`**
   Save a screenshot of the JD page next to `jd.md` for the user's records. Useful for postings that get taken down later.

#### Multi-tab batches

If the user has 5 tabs open and says "look at all of them":

1. `list_pages` once
2. For each candidate tab: `select_page` → `take_snapshot` → extract → save
3. Don't try to parallelize — Chrome MCP is single-threaded, and switching tabs while reading is the safest approach
4. After capture, give the user a summary table before doing any filtering

#### Failure modes

- **"无法找到 Chrome"**: The user doesn't have Chrome running, or chrome-devtools-mcp isn't connected. Tell them to open Chrome and try again.
- **Snapshot is mostly empty**: The page is still loading, or it's a SPA that hasn't hydrated. Use `wait_for` with a selector that should be present, then re-snapshot.
- **JD content is behind a "查看更多" button**: Use `click` to expand it before snapshotting.
- **Salary is hidden ("面议")**: Mark `salary: 面议` in the frontmatter and treat the `salary_min` hard rule as `unknown` rather than violated. Ask the user whether to proceed.

## JD field extraction

Regardless of input mode, you're trying to populate these fields:

```yaml
company: <name>
role: <title>
location: <city, or 远程>
salary: <range with K, e.g., "30-50K·15薪"> | 面议
work_model: 坐班 | 远程 | 混合 | unknown
years_required: <e.g., "5年以上"> | unknown
education: <e.g., "本科"> | unknown
source_url: <if available>
captured_at: <YYYY-MM-DD>
```

Plus the free-text body split into 岗位职责 and 任职要求 sections. If the JD doesn't separate them cleanly, do your best to split — they map to "what you'll do" and "what we need from you" respectively.

## Privacy

JD captures may include the recruiter's name or contact info. Don't paste these into your reply or report unnecessarily — keep them in `jd.md` for the user's reference but don't surface them.
