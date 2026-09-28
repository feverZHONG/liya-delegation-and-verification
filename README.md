# 委派与验收 · 把活分出去不吃亏

> 用 LLM 子代理干活的两个人问题：**任务书怎么写**（让回来的东西能用）、**验收怎么验**（让自报骗不了你）。
> 不站队的判据手册——每条都是「一条规则 ＋ 实测数字」。

## 这是什么

前提只有一句：**子代理的总结是自报，不是事实**。它说「全绿」「已推送」「一字未丢」——要么自己重跑一遍，要么等于没验。

正文按「这次要干哪种活」分节：

| 节 | 管什么 |
|:---|:---|
| 一 · 任务书：七件套 | 交付物 / 必读清单 / 验收命令＋期望数字 / 禁止清单 / 边界 / 输出 schema / 不要发明。少一样多一轮来回 |
| 二 · 并行：文件集必须不相交 | **按文件树切，不按主题切**；两个 child 都要动同一个文件就先串行 |
| 三 · 验收：自报 → 事实 | 重跑它给的命令 → 搬家类逐行找回 → 外部副作用**读回对象本身** → 数值目标另读一遍语义 |
| 四 · 坑 | 管道吞退出码、名单 ✅ ≠ 产物里有、生成器「刷新」覆盖手写件、`git add -A` 是危险动作…… |
| 五 · 挖料 / 检索型委派 | 按源切路、把硬约束当过滤器写进任务书、要负账（命中 0 也要翻译成结论） |
| 六 · 多路独立评审型委派 | 视角互不重叠、引文逐字＋真实行号、**回改之后要跑「改动清单终审」** |
| 七 · 评审产出落地成修订 | 先分发、再逐个改、先做计划；一节小样 → 点头 → 一节一停一节一账 |
| 八 · 外部评审 | 先对账后采纳；不采的连理由落档（总账里留一节「已驳回·别再回炉」） |

细读入口在 `SKILL.md`；案例与子判据（B1–B8 / V1–V26 等）在 `references/` 各档里，一个主题一档、不存两遍。

## 工具：搬家守恒复核

`scripts/conservation_check.py` —— **「一字未丢」的唯一证明方式**：原文里每一行（默认 >40 字）必须逐字出现在落点目录的任一 markdown 文件里。行数守恒只是粗筛，挡不住「把一句为什么概括掉」这种等长替换。

```bash
python3 scripts/conservation_check.py <新落点目录> <原始备份.md> [--min 40]
# 退出码：0=零丢失 / 1=有丢失 / 2=用法错
```

它在「拆薄 / 搬家 / 多单元重切」型任务的收尾验收里用得最勤：派活时把这条命令写进任务书，回来自己再跑一遍——**别读子代理交回的「0 丢失」结论**。

## 目录

| 路径 | 内容 |
|:---|:---|
| `SKILL.md` | 入口：八节判据全文（高频的「并行」「坑」两节原样留在正文） |
| `references/task-brief-cases.md` | 任务书判例 B1–B8（附属产出避开扫描目录 / 归属判据 / 跨单元接缝验收……） |
| `references/verification-cases.md` | 验收子判据 V1–V26（数值目标、字段比对、编号类引用……） |
| `references/delegate-harvest.md` | 挖料 / 检索型委派的 20 条要点与实测 |
| `references/delegate-review-panel.md` | 多路评审型委派的 15 条要点与实测 |
| `references/landing-review-findings.md` | 审读条目怎么落地成逐节修订（分发总表 / 小样 / 每节账） |
| `references/external-review.md` | 不受控第三方评审（AI 分享页、外部读者）的对账式采纳 |
| `references/verifying-external-side-effects.md` | 对外副作用（推送 / 建仓 / 写远端）的读回配方 |
| `scripts/conservation_check.py` | 搬家守恒复核（零丢失才算过） |

## 姊妹仓库

- [liya-subtraction-skill](https://github.com/feverZHONG/liya-subtraction-skill) —— 技能库做减法的方法论（拆薄 / 合并 / 出库）
- [liya-persona-authoring](https://github.com/feverZHONG/liya-persona-authoring) —— 给 AI agent 写它自己的身份文件
- [liya-vision-recognition-traps](https://github.com/feverZHONG/liya-vision-recognition-traps) —— 视觉模型识图陷阱：22 条实测陷阱 + 真 OCR 通道 + 两图差分
- [liya-sillytavern-cards](https://github.com/feverZHONG/liya-sillytavern-cards) —— 酒馆（SillyTavern）角色卡：写法、格式规格、三个 Python 工具
- [liya-sillytavern-worldbook](https://github.com/feverZHONG/liya-sillytavern-worldbook) —— 酒馆世界书（Lorebook）：触发链源码实证 + 触发体检 / 模拟 / 生成工具
- [liya-chat-game-referee](https://github.com/feverZHONG/liya-chat-game-referee) · [liya-spy-game](https://github.com/feverZHONG/liya-spy-game) · [liya-sea-turtle-soup](https://github.com/feverZHONG/liya-sea-turtle-soup) —— 聊天里能玩的三件（回合制裁判引擎 / 谁是卧底 / 海龟汤）
- [liya-tavern-card-refinement](https://github.com/feverZHONG/liya-tavern-card-refinement) —— 酒馆角色卡精修：7 字段清单 + 槽位归位 + 6 类断言校验 + 可用性验收（不装酒馆也能量）
- [liya-prose-quality-metrics](https://github.com/feverZHONG/liya-prose-quality-metrics) —— 稿子读起来「平」怎么办：先量再改（对话占比·句长σ·台词宽度·标点谱·段均句）＋ 7 个工具
- [liya-ruozhiba-wordbank](https://github.com/feverZHONG/liya-ruozhiba-wordbank) —— 弱智吧题防御手册：中文互联网逻辑陷阱题 160 道逐题拆解 + 三连防御法（拆前提→指谬误→反杀）
- [liya-subtitle-proofreading](https://github.com/feverZHONG/liya-subtitle-proofreading) —— 字幕校对/重建/外挂 SRT：对照成稿逐处修正 + 按原文重建分块 + md→SRT + 多人语音 ASR 导出件解析（5 个纯标准库工具）
- [liya-corpus-line-mining](https://github.com/feverZHONG/liya-corpus-line-mining) —— 从本地语料／会话库挖可复用原句：候选池筛选 + 人审落库（纯标准库，零依赖）

## 提思路 / 提修正

- 你那边踩到的委派坑、验不出来的自报、别的验收手段 → 开 [Issue](https://github.com/feverZHONG/liya-delegation-and-verification/issues)，写清场景（什么任务、派了几路子代理、回来报了什么、后来怎么发现不对）
- 想直接改 → Fork + PR

## 许可

**双许可**——文档与代码分开：

- **代码**（`scripts/` 下的文件）：**MIT** —— 拿去用、改、再发，保留版权声明即可。
- **文档**（`SKILL.md`、`references/`、本 README 的正文）：**[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)** —— 可以自由使用、改编、连商用都行，**但要署名**（莉娅 / [@feverZHONG](https://github.com/feverZHONG)）并注明来源。

两份许可的全文：`LICENSE`（MIT）／`LICENSE-DOCS`（CC BY 4.0）。

---

*莉娅（[@feverZHONG](https://github.com/feverZHONG)）· 宇宙美好记录官*
