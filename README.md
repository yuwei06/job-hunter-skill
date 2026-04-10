<div align="center">

# 🎯 job-hunter-skill

**一个面向求职者的 Claude Code skill —— 自动筛选招聘信息，按 JD 生成"诚实"的定制简历。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-8A2BE2)](https://docs.claude.com/en/docs/claude-code)
[![typst](https://img.shields.io/badge/PDF-typst-239DAD)](https://typst.app/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#-参与贡献)
[![中文](https://img.shields.io/badge/docs-中文-red)](#-这是什么)

[快速开始](#-快速开始) · [工作流](#-它是怎么工作的) · [示例](examples/example-prompts.md) · [Skill 规范](SKILL.md) · [English](#english)

</div>

---

## ✨ 这是什么？

大多数招聘类工具的玩法都是：**爬虫拉取 JD → 关键词匹配 → 一键群发**。结果就是你被各家平台 ban 号、HR 看一眼就把你简历扔进垃圾桶。

**job-hunter-skill 走的是另一条路** ——

> **同一个人，换种讲法。不是另一个人。**

它把求职这件事当成一个**工程化筛选问题**：

1. 你设定**硬底线**（城市、薪资、是否外包、是否 996、屏蔽词），违反一条就直接淘汰
2. 通过的岗位用**多维度加权打分**告诉你值不值得投
3. 对值得投的岗位，从你**真实的主简历和素材库**里挑出最匹配的部分，重新组织措辞 —— 但**绝不编造**任何技能、绝不堆砌关键词
4. 最后渲染成专业 PDF

每一份生成的简历都能在主简历里找到出处，每一个能力 gap 都会被明确标出来让你**面试前提前准备**，而不是让你被技术问题打个措手不及。

## 🎯 它能做什么

| 能力 | 说明 |
|---|---|
| 🔍 **多种 JD 输入** | 贴文本 / 公开 URL（WebFetch）/ 已登录 BOSS·拉勾·LinkedIn 标签页（chrome-devtools-mcp） |
| 🛡️ **硬规则一票否决** | 城市、薪资下限、外包、996、自定义黑名单关键词 |
| 📊 **6 维度软打分** | 技术栈 30% / 资历 20% / 领域 15% / 角色形态 15% / 公司信号 10% / 薪酬 10% |
| ✍️ **诚实改简历** | 重排序、重措辞、用 JD 词汇 —— 但不增项、不夸大、不堆砌 |
| 📄 **typst 渲染 PDF** | 单二进制、CJK 开箱即用、3 秒出 PDF |
| 🗂️ **每岗一个独立目录** | `applications/<公司>-<岗位>-<日期>/` 包含 JD、评分报告、定制简历 .md / .pdf |
| 🌐 **批量处理** | 浏览器开 5 个岗位让 skill 一次过完，给你汇总表 |

## 👥 谁会用得上

- 正在求职、不想浪费时间投烂岗位的**程序员 / 产品 / 设计**
- 离职面试季想**系统化管理几十个 JD** 的人
- 嫌"一键投递"工具不靠谱、想要**有质量的应聘流程**的人
- 喜欢**用工具优化重复劳动**、把求职当成工程问题的人

## 🚀 快速开始

### 1. 安装 typst（用于 PDF 渲染）

```bash
brew install typst
```

> 为什么是 typst：单个二进制 50MB、CJK 开箱即用（macOS 上自动用 PingFang SC）、不需要 LaTeX 工具链、3 秒渲染。

### 2. 安装 skill

**个人级（推荐）：**

```bash
git clone https://github.com/yuwei06/job-hunter-skill.git \
  ~/.claude/skills/job-hunter
```

**项目级：**

```bash
git clone https://github.com/yuwei06/job-hunter-skill.git \
  .claude/skills/job-hunter
```

### 3. 准备你的工作目录

在桌面（或任意位置）建一个文件夹，放好两样东西：

```text
~/Desktop/面试/                          # 或你喜欢的任何位置
├── <你的名字>-<岗位>-<年限>.docx        # 主简历 — 必需
├── <你的名字>仓库.docx                   # 素材库 — 可选但强烈推荐
└── preferences.yaml                      # 筛选配置 — 必需
```

`preferences.yaml` 直接拷贝模板：

```bash
cp ~/.claude/skills/job-hunter/assets/preferences.template.yaml \
  ~/Desktop/面试/preferences.yaml
```

打开编辑：你想去哪些城市、薪资底线多少、屏蔽哪些公司类型 / 技术栈。

### 4. 用起来

直接用自然语言描述你的需求，skill 会自动触发：

```text
帮我看看 BOSS 上现在打开的这个岗位
```

```text
这是一个 JD：
[贴文本]
如果合适就帮我生成针对性简历
```

```text
浏览器里开了 5 个岗位，都过一遍，告诉我哪几个值得投
```

更多场景见 [`examples/example-prompts.md`](examples/example-prompts.md)。

## 🧠 它是怎么工作的

skill 把求职拆成 **7 步固定流水线** ——

```
1. 加载上下文      读 preferences.yaml + 主简历 + (可选) 素材库
       ↓
2. 抓取 JD        贴文本 / WebFetch / chrome-devtools-mcp
       ↓
3. 硬规则筛选     城市 / 薪资 / 外包 / 996 / 屏蔽词 — 任何一条违反 → REJECTED
       ↓
4. 软规则打分     6 维度加权 → 0-100 分 + STRONG_MATCH / WORTH_APPLYING / STRETCH / WEAK
       ↓
5. 改简历         从主简历挑料 → 用 JD 词汇 → 不增项、不夸大、不堆砌
       ↓
6. 渲染 PDF       markdown → typst → 一页中文简历
       ↓
7. 汇报           评分 / 命中 / gap / 面试准备建议
```

每一步都可以单独触发。比如你只想筛选不想生成简历："**先帮我筛一遍这些岗位，简历晚点再说**"。

完整规范见 [`SKILL.md`](SKILL.md)。

## 📂 仓库结构

```text
job-hunter-skill/
├── SKILL.md                          # Claude 读取的 skill 主定义
├── README.md                         # 当前文件
├── LICENSE                           # MIT
├── references/
│   ├── jd-extraction.md              # 浏览器 MCP 抓 JD 的具体步骤
│   ├── matching-rubric.md            # 6 维度打分细则
│   └── resume-tailoring.md           # 改简历的"什么能做 / 不能做"
├── assets/
│   ├── preferences.template.yaml     # 偏好配置模板（拷到工作目录后修改）
│   └── resume.template.typ           # typst 简历模板（CJK 适配）
├── scripts/
│   ├── read_docx.py                  # 标准库 .docx 文本提取（零依赖）
│   └── render_pdf.py                 # markdown → typst → PDF
└── examples/
    └── example-prompts.md            # 真实场景 prompt 示例
```

## ⚠️ 它**不**做什么

- ❌ **不自动投递** —— 它生成 PDF，但点"提交"是你自己的事。**为什么**：自动投递是被各家平台 ban 号 + 烧 HR 印象的最快方式
- ❌ **不替你登录平台** —— BOSS / LinkedIn / 拉勾 你自己在 Chrome 里登录好，然后让 skill 接管那个标签页
- ❌ **不编造经历** —— JD 要 K8s 但你没碰过？简历里**不会出现** K8s。这一项会进 `match-report.md` 的 gap 列表，让你面试前提前准备
- ❌ **不动你的主简历** —— 定制简历永远去新建的 `applications/<slug>/` 子目录。主简历是你的真相之源
- ❌ **不堆砌关键词** —— 关键词堆砌的简历会被人和 ATS 同时看穿，得不偿失

## 🎯 设计理念

这个 skill 围绕 4 条核心原则：

1. **筛选比生成更重要** —— 99% 的时间应该花在判断"值不值得投"，而不是"怎么把简历写好看"。所以硬规则优先。

2. **诚实是长期最优解** —— 一份能通过技术面的简历，比 10 份吹得天花乱坠却在第一轮就翻车的简历有用得多。所以**绝不增项**。

3. **gap 透明化** —— 不匹配的能力不是隐藏起来，而是写到 match-report 里让你看见。求职者最怕的是"我以为自己 ready 了"。

4. **可以被 fork 给任何角色** —— 模板里没有任何前端 / 后端 / 设计的硬编码。你只需要替换 `preferences.yaml`，这个 skill 就能服务任何方向。

## 🤝 参与贡献

非常欢迎 PR，尤其是这些方向：

- **更多平台的 JD 抓取选择器**（BOSS / 拉勾 / 智联 / 猎聘 / 51job / LinkedIn 的 DOM 选择器）
- **更多语言 / 行业的简历模板**（设计岗、数据岗、产品岗）
- **更精细的打分维度**（比如"晋升空间"、"技术氛围"等软指标）
- **typst 模板的视觉迭代**
- **多语言 JD 支持**（英文 JD → 英文简历）

提大改前先开 issue 聊一聊。

## 📄 License

MIT —— 详见 [`LICENSE`](LICENSE)。商用、fork、改造，随便。

---

## English

A Claude Code skill for filtering job postings against your hard/soft criteria and generating tailored, **honest** PDF resumes — never fabricates skills, never keyword-stuffs.

**Core flow:** read your master resume + 素材库 → capture a JD (paste / URL / chrome-devtools-mcp on a logged-in BOSS or LinkedIn tab) → hard-filter against `preferences.yaml` → soft-score across 6 weighted dimensions → tailor your resume from real material → render to PDF via [typst](https://typst.app/).

**What it doesn't do:** auto-apply, log into platforms for you, fabricate experience, write to your master resume, or keyword-stuff. The principle is *"the same person, told differently — not a different person."*

**Quick start:**

```bash
brew install typst
git clone https://github.com/yuwei06/job-hunter-skill.git ~/.claude/skills/job-hunter
cp ~/.claude/skills/job-hunter/assets/preferences.template.yaml ~/Desktop/面试/preferences.yaml
# edit preferences.yaml, drop your master .docx in ~/Desktop/面试/, then ask Claude:
# "帮我看看 BOSS 上现在打开的这个岗位"
```

See [`SKILL.md`](SKILL.md) for the full spec and [`examples/example-prompts.md`](examples/example-prompts.md) for prompts.

---

<div align="center">

**如果它帮你避开了一份烂工作，请点个 ⭐**

Made with ❤️ for job seekers who refuse to spam.

</div>
