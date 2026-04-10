# Example prompts

Real things the user might say to trigger this skill.

## Single JD — pasted text

```text
帮我看看这个岗位适不适合我，如果合适就生成一份针对性的简历：

【高级前端工程师】
公司：某 AI 创业公司
地点：武汉/远程
薪资：20-35K · 14薪
要求：
- 5 年以上前端经验
- 精通 React + TypeScript
- 有 AI Agent / LLM 应用产品经验加分
- 熟悉 React Flow、可视化工作流编排
...
```

## Single JD — open browser tab (Chrome MCP)

```text
我现在 BOSS 直聘上开了一个岗位的页面，帮我分析一下匹配度，
能投就生成简历
```

```text
看一下我浏览器现在打开的那个 LinkedIn 岗位
```

## Batch — multiple open tabs

```text
我现在 Chrome 里开了 5 个 BOSS 的岗位，帮我都过一遍，
告诉我哪几个值得投，然后给值得投的生成简历
```

## Just filter, no resume

```text
先帮我筛一遍这些岗位，简历晚点再说
```

## Just resume, JD already captured

```text
我刚把字节那个 JD 存在 ~/Desktop/面试/applications/字节-高级前端-2026-04-10/jd.md 了
帮我生成针对它的简历
```

## Update preferences

```text
把我的薪资下限改成 18K，加一个上海到城市白名单
```

```text
我后悔了，区块链项目我也愿意聊，把它从 exclude_keywords 里去掉
```

## Re-score with different priorities

```text
这次只看技术栈匹配度，其他维度都不看
```

```text
帮我把"管理经验"那一类岗位都标低分，我不想做 lead
```
