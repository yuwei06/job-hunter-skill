// Resume template for the job-hunter skill.
//
// This template is appended to a data block emitted by render_pdf.py. The
// data block defines these variables:
//   resume-name, resume-title, resume-contact, resume-summary,
//   resume-experience (array), resume-projects (array),
//   resume-skills, resume-education
//
// Design priorities:
//   - one page if at all possible
//   - clean, recruiter-scannable hierarchy
//   - CJK-friendly (PingFang SC on macOS, fallback to system sans)
//   - no decorative junk

#set page(
  paper: "a4",
  margin: (x: 1.6cm, y: 1.4cm),
)

#set text(
  font: ("PingFang SC", "Helvetica Neue", "Helvetica", "Arial"),
  size: 10pt,
  lang: "zh",
  region: "cn",
)

#set par(
  justify: false,
  leading: 0.55em,
)

// Header — name + title + contact
#align(center)[
  #text(size: 18pt, weight: "bold")[#resume-name]
  #if resume-title != "" [
    #text(size: 12pt, fill: rgb("#444"))[ · #resume-title]
  ]
  #if resume-contact != "" [
    #linebreak()
    #text(size: 9pt, fill: rgb("#666"))[#resume-contact]
  ]
]

#v(0.4em)
#line(length: 100%, stroke: 0.5pt + rgb("#bbb"))
#v(0.2em)

// Section heading helper
#let section(title) = {
  v(0.5em)
  text(size: 11pt, weight: "bold", fill: rgb("#0a4d8c"))[#title]
  v(0.1em)
  line(length: 100%, stroke: 0.4pt + rgb("#0a4d8c"))
  v(0.2em)
}

// Item heading helper (for experience and projects)
#let item(heading, meta) = {
  v(0.3em)
  grid(
    columns: (1fr, auto),
    align: (left, right),
    text(weight: "bold", size: 10.5pt)[#heading],
    text(size: 9pt, fill: rgb("#555"))[#meta],
  )
  v(0.05em)
}

// Bullet list helper
#let bullets(items) = {
  for b in items [
    - #b
  ]
}

// === Body ===

#if resume-summary != "" [
  #section[个人概述]
  #resume-summary
]

#if resume-experience.len() > 0 [
  #section[工作经历]
  #for exp in resume-experience [
    #item(exp.heading, exp.meta)
    #bullets(exp.bullets)
  ]
]

#if resume-projects.len() > 0 [
  #section[项目经验]
  #for proj in resume-projects [
    #item(proj.heading, proj.meta)
    #bullets(proj.bullets)
  ]
]

#if resume-skills != "" [
  #section[技术栈]
  #resume-skills
]

#if resume-education != "" [
  #section[教育背景]
  #resume-education
]
