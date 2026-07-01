# paper-writing-agent

[English](#english) · [简体中文](#简体中文) · [日本語](#日本語)

## English

> Write the paper your experiments already earned. paper-writing-agent drafts and
> revises computer-science and software-engineering manuscripts from your own
> code, logs, and numbers, so the prose is precise, the statistics are honest, the
> citations are real, and the text carries no AI fingerprints. Built to maximize
> acceptance at a high-impact venue.

### The problem it solves

A paper is a lossy compression of your experiments, and most of the loss happens
in translation. A number is retyped from a figure and is quietly wrong. A method
is half-remembered a month after the run. A citation says something the cited work
does not. Prose reads like a language model and gets flagged in review. Each gap
costs you accuracy, or costs you a reviewer's trust.

paper-writing-agent closes those gaps. You point it at the artifacts that already
define your result: the source code, the run scripts, the config files, the logs,
the environment recipe, and the full-precision statistics. It writes from those,
not from memory. It will not invent a citation or call a result significant
without a test and a verdict. And it removes the AI-writing patterns that make an
otherwise sound draft look machine-made.

### Who it is for

Researchers who run computational (dry-lab) experiments, in bioinformatics,
machine learning, computational science, or software engineering, who own the
code, logs, and configuration behind their results, and who want to turn them into
a paper aimed at a strong venue. If you can point at the directory where a
figure's numbers were produced, this tool keeps your draft grounded in it.

### What it is

paper-writing-agent is a hybrid of two layers:

- a **Claude Code plugin** (the intended way to use it): an agent that plans,
  drafts, and revises with you under a plan-confirm-execute-verify workflow, with
  a knowledge base of journal-agnostic writing templates; and
- a deterministic **Python core** (`pip install paper-writing-agent`, command
  `pwa`): the engine underneath, which lints prose, indexes a bibliography, tracks
  completion, and checks definitions, with no editor dependency and full test
  coverage.

The plugin gives you the experience; the core gives you checks you can trust
because they are code, not judgment. Sensible defaults out of the box; everything
is overridable through `pwa init`.

### Requirements

- **[Claude Code](https://claude.com/claude-code)** (required): the agent runs as
  a Claude Code plugin, and this is the primary interface.
- **Python 3.10 or newer**: for the `pwa` core that the plugin calls.
- Your manuscript, and read access to the experiment artifacts behind it.

You can run the `pwa` core on its own as a set of linters, but the writing
workflow assumes Claude Code.

### Install

```bash
pip install paper-writing-agent        # provides the `pwa` command
# or, from a clone:
pip install -e ".[dev]"
```

For the Claude Code plugin (skills, commands, agents, knowledge base), see
[plugin/README.md](plugin/README.md).

### Setup: point the agent at your experiment

This step is what lets the agent write without losing information. After
`pwa init`, open `PROJECT_PROFILE.md` in your workspace, record where each kind of
evidence lives, and tell the agent to read it:

| Source | What the agent uses it for |
| --- | --- |
| Results and outputs | the numbers behind every figure and table |
| Experiment source code | the true description of the method |
| Run scripts and job files | how each run was launched and configured |
| Config files | hyperparameters and experimental conditions |
| Logs | what actually happened during a run |
| Environment recipe | versions, for a reproducible Methods section |
| Statistics store (`stats/`) | full-precision numbers, rounded only in prose |

The agent records the figure-to-code chain in `provenance_map.md`, so any number
in the manuscript traces back to the script and data that produced it. Given these
paths, the Methods follow the code, the numbers come from the store rather than
your memory, and nothing is asserted that the sources do not support.

### Quickstart

```bash
# 1. Set up a manuscript workspace (interactive; or add --yes for defaults).
pwa init my-paper/

# 2. Record your experiment sources in my-paper/PROJECT_PROFILE.md. Then, in
#    Claude Code, ask the agent to draft a section from them:
#    /pwa-draft introduction

# 3. Check your prose against every rule.
pwa check my-paper/

# 4. Build a citation context index from your bibliography.
pwa bib build my-paper/bib/refs.bib --output my-paper/bib/bib_index.yaml
pwa bib validate my-paper/bib/bib_index.yaml --bib my-paper/bib/refs.bib --strict

# 5. Track section completion and find exemplars to imitate.
pwa sections sync my-paper/main.tex
pwa sections exemplars introduction

# 6. Check define-once discipline in reading order.
pwa defs check my-paper/abstract.tex my-paper/introduction.tex
```

### Design philosophy (why it works this way)

The full statement is in [docs/DESIGN_PHILOSOPHY.md](docs/DESIGN_PHILOSOPHY.md).
It is the generic, public form of a writing discipline built while writing
high-impact papers, and every feature and default is judged against it. Eight
pillars:

1. **Evidence grounding.** Every claim resolves to a source: a number in the
   statistics store, a figure's provenance chain, a citation key with recorded
   context, or a symbol in the definitions registry. Nothing is asserted from
   memory.
2. **Anti-AI-slop.** AI prose has fingerprints (inflated significance, copula
   avoidance, participle padding, synonym cycling, forced rules of three, em
   dashes, a fixed vocabulary). The linter finds them and proposes precise
   academic replacements.
3. **Statistical honesty.** "Significant" is earned, not asserted: it needs a
   test, a P-value below threshold, and an explicit verdict. A bare P-value is a
   defect.
4. **Single source of truth.** Each rule and each piece of state has exactly one
   owner. No value is duplicated.
5. **Plan, confirm, execute, verify.** The agent states its plan, waits for your
   approval, executes only that, then verifies. Decision authority is yours.
6. **Reproducibility.** Statistics are re-runnable, never transcribed from an
   image; completion changes are timestamped and justified.
7. **Configurable, not rigid.** The original agent was tuned to one author and one
   venue. Here, venue, citation style, spelling, notation, structure, strictness,
   and operating language are settings with friendly defaults, not assumptions.
8. **Dogfooding.** The project lints its own prose with its own linter, in
   pre-commit and CI. This README passes `pwa lint`.

Three convictions shape the defaults:

- **Source code and artifacts are the primary truth**, ahead of memory or an
  earlier draft. Technical claims are grounded in files the agent has read;
  whatever it cannot trace, it flags rather than asserts.
- **What to leave out is a decision, made before drafting.** For each figure,
  paragraph, and caption, the plan states what it will not contain, so the result
  stays focused and a non-specialist can still follow it.
- **A headline sentence is catchy and accurate.** A punchline stays only
  if a measurement backs it; a metaphor the data does not support is cut.

Objective: maximize the probability of acceptance at a high-impact venue. Quality
hierarchy: **Accuracy > Clarity > Conciseness > Professionalism.** When two goals
conflict, the earlier one wins; accuracy is never traded for brevity.

### Commands

| Command | What it does |
| --- | --- |
| `pwa init <dir>` | Create a config and scaffold a manuscript workspace. |
| `pwa lint <paths>` | Find AI-writing fingerprints; suggest replacements. |
| `pwa stats <paths>` | Check P-value verdicts, test naming, and number/unit style. |
| `pwa defs check <files>` | Flag forward references and redefinitions in reading order. |
| `pwa bib build/validate/ground` | Build, validate, and ground a citation context index. |
| `pwa sections status/sync/set/exemplars` | Track completion; pick exemplars. |
| `pwa check <paths>` | Run all linters at once. |

Each linter exits non-zero on errors, accepts `--exit-zero` for warn-only use, and
supports `--format json`.

### Configuration

`pwa init` writes `paper-writing-agent.toml` from a preset
(`strict-high-IF` / `balanced` / `lenient`) and a short wizard. Every value is
editable by hand. Configurable knobs include target field and venue tier, citation
style, spelling (US/UK), P-value notation, significant figures, section structure,
figure-reference style, hedging strictness, operating language, and project-local
forbidden-word extensions. Invariant by design: significance needs a test and a
verdict, citations are never fabricated, and the user decides.

### Repository layout

```
paper-writing-agent/
├── src/paper_writing_agent/   # deterministic core (editor-agnostic)
│   ├── cli.py                 #   entry point: pwa init|lint|bib|stats|sections|defs|check
│   ├── config/                #   config model + presets + init wizard + TOML I/O
│   ├── slop/                  #   anti-AI-slop linter (rules, masking, engine, report)
│   ├── bibindex/              #   BibTeX parser, context index, schema validator, grounding
│   ├── stats/                 #   statistical-honesty linter
│   ├── sections/              #   completion tracker + exemplars
│   ├── definitions/           #   abbreviation registry + no-forward-reference linter
│   ├── scaffold.py            #   workspace scaffolder used by `pwa init`
│   └── templates/workspace/   #   manuscript-workspace templates (package data)
├── plugin/                    # Claude Code plugin (agentic layer)
│   ├── skills/ commands/ agents/ knowledge/
│   └── README.md
├── examples/                  # synthetic CS/software worked examples
├── tests/                     # pytest tests for every module
└── docs/                      # design philosophy, architecture, requirements, slides
```

A manuscript workspace created by `pwa init` holds your `PROJECT_PROFILE.md`,
`paper_outline.md`, `DEFINITIONS.md`, `citation_policy.md`, `provenance_map.md`,
`section_status.yaml`, `bib/`, `stats/`, and the resolved
`paper-writing-agent.toml`. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

### Two layers, one core

The Python core is pure, deterministic, and unit-tested; it owns the rules and the
checks and has no editor dependency. The Claude Code plugin supplies the workflow,
prompts, and templates, and calls the core for every check. The rules stay
verifiable; the agent stays free to orchestrate.

### Slides

A nine-slide deck on the motivation and technical core lives in
[docs/slides/](docs/slides/):
[PDF](docs/slides/design-philosophy.pdf) ·
[PPTX](docs/slides/design-philosophy.pptx) (native, editable).

### Privacy

This is a generic, domain-agnostic tool. It contains no project-specific,
unpublished, or author-private material. All worked examples are synthetic and
drawn from the computer-science and software domains. See [NOTICE](NOTICE).

### Disclaimer

This tool assists with writing; it does not guarantee correctness. Verifying every
claim, number, citation, and statement, and accountability for the submitted
manuscript, rest with the author, not with the AI or this tool.

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The project holds its own development to
the same discipline it enforces on manuscripts.

### License

MIT (see [LICENSE](LICENSE)). Attribution for adapted content is in
[NOTICE](NOTICE).

---

## 简体中文

> 写出你的实验本就值得的论文。paper-writing-agent 从你自己的代码、日志与数值出发，
> 起草与修订计算机科学与软件工程论文，使行文精确、统计诚实、引用真实、文本不带
> AI 指纹。为最大化高影响力场所的录用概率而构建。

### 它解决的问题

论文是对实验的一次有损压缩，而大部分损失发生在转写之间。一个数字从图中重新键入，
却悄然出错。一种方法在运行一个月后只被记住一半。一处引用说了被引文献并未表达的意思。
行文读起来像语言模型，于是在评审中被标记。每一处缺口，要么让你损失准确性，要么让你
损失评审人的信任。

paper-writing-agent 弥合这些缺口。你把它指向那些已经定义了结果的产物：源代码、运行
脚本、配置文件、日志、环境配方，以及全精度统计数据。它据此写作，而非凭记忆。它不会
臆造引用，也不会在没有检验与结论判定的情况下称某结果显著。它还会移除那些让一份本来
扎实的草稿显得像机器所写的 AI 行文模式。

### 适用人群

从事计算（干实验）研究的人员，涵盖生物信息学、机器学习、计算科学或软件工程，拥有其
结果背后的代码、日志与配置，并希望将它们转化为面向强场所的论文。只要你能指出某张图的
数值是在哪个目录里产生的，本工具就能让你的草稿接地于此。

### 这是什么

paper-writing-agent 是两层的混合体：

- 一个 **Claude Code 插件**（推荐的使用方式）：一个与你协作的智能体，遵循
  计划-确认-执行-核验的工作流进行规划、起草与修订，并附带一套与期刊无关的写作模板
  知识库；以及
- 一个确定性的 **Python 内核**（`pip install paper-writing-agent`，命令为 `pwa`）：
  底层引擎，用于检查行文、建立文献索引、跟踪完成度、校验术语定义，不依赖任何编辑器，
  且具备完整测试覆盖。

插件给你体验，内核给你可信赖的检查，因为它们是代码而非判断。开箱即用的合理默认值；
一切都可通过 `pwa init` 覆盖。

### 前置要求

- **[Claude Code](https://claude.com/claude-code)**（必需）：智能体以 Claude Code
  插件形式运行，这是主要界面。
- **Python 3.10 或更新版本**：供插件调用的 `pwa` 内核使用。
- 你的稿件，以及对其背后实验产物的读取权限。

你可以单独把 `pwa` 内核当作一组检查器来运行，但写作工作流以 Claude Code 为前提。

### 安装

```bash
pip install paper-writing-agent        # 提供 `pwa` 命令
# 或从克隆仓库安装：
pip install -e ".[dev]"
```

Claude Code 插件（技能、命令、智能体、知识库）请见 [plugin/README.md](plugin/README.md)。

### 设置：把你的实验告诉智能体

正是这一步让智能体在写作时不丢失信息。在 `pwa init` 之后，打开工作区中的
`PROJECT_PROFILE.md`，记录每一类证据所在的位置，并让智能体去读取：

| 来源 | 智能体用它做什么 |
| --- | --- |
| 结果与输出 | 每张图与每张表背后的数值 |
| 实验源代码 | 方法的真实描述 |
| 运行脚本与作业文件 | 每次运行如何被启动与配置 |
| 配置文件 | 超参数与实验条件 |
| 日志 | 一次运行中实际发生了什么 |
| 环境配方 | 版本信息，供可复现的方法部分使用 |
| 统计存储（`stats/`） | 全精度数值，仅在行文中才做四舍五入 |

智能体会把「图到代码」的链条记录在 `provenance_map.md` 中，因此稿件中的任何数值都能
追溯到产生它的脚本与数据。给定这些路径，方法部分随代码而定，数值取自存储而非你的记忆，
且不会断言来源并不支持的内容。

### 快速开始

```bash
# 1. 建立论文工作区（交互式；或加 --yes 使用默认值）。
pwa init my-paper/

# 2. 在 my-paper/PROJECT_PROFILE.md 中记录你的实验来源。然后在 Claude Code 中
#    让智能体据此起草某一节：
#    /pwa-draft introduction

# 3. 按全部规则检查行文。
pwa check my-paper/

# 4. 由参考文献建立引用上下文索引。
pwa bib build my-paper/bib/refs.bib --output my-paper/bib/bib_index.yaml
pwa bib validate my-paper/bib/bib_index.yaml --bib my-paper/bib/refs.bib --strict

# 5. 跟踪各节完成度并查找可借鉴的范例。
pwa sections sync my-paper/main.tex
pwa sections exemplars introduction

# 6. 按阅读顺序检查“术语先定义后使用”。
pwa defs check my-paper/abstract.tex my-paper/introduction.tex
```

### 设计理念（为什么这样做）

完整说明见 [docs/DESIGN_PHILOSOPHY.md](docs/DESIGN_PHILOSOPHY.md)。它是一套在撰写
高影响力论文过程中形成的写作纪律的通用、公开形式，每一项功能与默认值都以它为准绳。
八根支柱：

1. **证据为本。** 每个论断都可追溯到来源：统计存储中的数值、图的溯源链、带有既往
   用法的引用键，或术语表中的符号。绝不凭记忆断言。
2. **杜绝 AI 腔。** AI 行文有指纹（夸大的显著性、回避系动词、分词填充、同义词轮换、
   刻意的三段式、破折号、固定词汇）。检查器会发现它们并给出精确的学术替换。
3. **统计诚实。** “显著”需要争取而非断言：它需要检验、低于阈值的 P 值以及明确的结论
   判定。孤立的 P 值即为缺陷。
4. **唯一真实来源。** 每条规则与每份状态只有一个归属。任何取值都不重复。
5. **先计划、再确认、后执行、终核验。** 智能体先陈述计划，等待你的批准，只执行获批
   内容，然后核验。决定权在你。
6. **可复现。** 统计可重新运行，绝不从图像转录；完成度变更带有时间戳与理由。
7. **可配置而非僵化。** 原始智能体是为单一作者与单一场所调校的。这里，场所、引用风格、
   拼写、记法、结构、严格度与运行语言都是带有友好默认值的设置项，而非默认假设。
8. **自食其果（dogfooding）。** 本项目在 pre-commit 与 CI 中用自己的检查器检查自己的
   文字。本 README 通过 `pwa lint`。

三条信念塑造了这些默认值：

- **源代码与产物是首要真相**，先于记忆或早先的草稿。技术论断接地于智能体已读取的
  文件；凡不能追溯者，它标记而非断言。
- **不写什么，是一个先于起草的决定。** 对每张图、每个段落、每条图注，计划都会说明它
  将不包含什么，从而使成果保持聚焦，非专业读者也能跟上。
- **一句点题的话，既要抓人，也要准确。** 只有当某项测量支撑它时，点题句才保留；
  数据并不支持的比喻会被删去。

目标：最大化高影响力场所的录用概率。质量层级：
**准确 > 清晰 > 简洁 > 专业。** 当两个目标冲突时，靠前者胜出；绝不以简洁换取准确。

### 命令

| 命令 | 作用 |
| --- | --- |
| `pwa init <dir>` | 创建配置并生成论文工作区。 |
| `pwa lint <paths>` | 找出 AI 行文指纹并给出替换建议。 |
| `pwa stats <paths>` | 检查 P 值结论、检验命名、数字与单位格式。 |
| `pwa defs check <files>` | 按阅读顺序标记前向引用与重复定义。 |
| `pwa bib build/validate/ground` | 构建、校验并以既往用法锚定引用索引。 |
| `pwa sections status/sync/set/exemplars` | 跟踪完成度并挑选范例。 |
| `pwa check <paths>` | 一次运行全部检查器。 |

每个检查器在出现错误时返回非零码，支持 `--exit-zero`（仅告警）与 `--format json`。

### 配置

`pwa init` 会基于预设（`strict-high-IF` / `balanced` / `lenient`）与简短向导写出
`paper-writing-agent.toml`，所有取值均可手动编辑。可配置项包括目标领域与场所层级、
引用风格、拼写（美式/英式）、P 值记法、有效数字、章节结构、图表引用风格、对冲措辞
严格度、运行语言，以及项目本地的禁用词扩展。设计上的不变量：显著性需要检验与结论判定、
绝不臆造引用、决定权在用户。

### 仓库结构

```
paper-writing-agent/
├── src/paper_writing_agent/   # 确定性内核（与编辑器无关）
│   ├── cli.py                 #   入口：pwa init|lint|bib|stats|sections|defs|check
│   ├── config/                #   配置模型 + 预设 + 初始化向导 + TOML 读写
│   ├── slop/                  #   杜绝 AI 腔检查器（规则、掩码、引擎、报告）
│   ├── bibindex/              #   BibTeX 解析器、上下文索引、模式校验、锚定
│   ├── stats/                 #   统计诚实检查器
│   ├── sections/              #   完成度跟踪 + 范例
│   ├── definitions/           #   缩写表 + 禁止前向引用检查器
│   ├── scaffold.py            #   `pwa init` 使用的工作区生成器
│   └── templates/workspace/   #   论文工作区模板（打包数据）
├── plugin/                    # Claude Code 插件（智能体层）
│   ├── skills/ commands/ agents/ knowledge/
│   └── README.md
├── examples/                  # 合成的 CS/软件示例
├── tests/                     # 每个模块的 pytest 测试
└── docs/                      # 设计理念、架构、需求、幻灯片
```

由 `pwa init` 生成的论文工作区包含你的 `PROJECT_PROFILE.md`、`paper_outline.md`、
`DEFINITIONS.md`、`citation_policy.md`、`provenance_map.md`、`section_status.yaml`、
`bib/`、`stats/`，以及解析后的 `paper-writing-agent.toml`。见
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)。

### 两层一核

Python 内核纯粹、确定且经过单元测试，拥有规则与检查，且不依赖任何编辑器；Claude Code
插件提供工作流、提示词与模板，并调用内核执行每一项检查。规则保持可验证；智能体保持
自由编排。

### 幻灯片

关于动机与技术内核的九页幻灯片位于 [docs/slides/](docs/slides/)：
[PDF](docs/slides/design-philosophy.pdf) ·
[PPTX](docs/slides/design-philosophy.pptx)（原生、可编辑）。

### 隐私

这是一个通用、与领域无关的工具，不含任何项目专有、未发表或作者私有的材料。所有示例
均为合成内容，取自计算机科学与软件领域。见 [NOTICE](NOTICE)。

### 免责声明

本工具用于辅助写作，不保证正确性。论文中每一处主张、数字、引用与表述的核对，以及对
所提交稿件的责任，由作者本人承担，而非 AI 或本工具。

### 参与贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。本项目以其要求于论文的同等纪律来约束自身的开发。

### 许可证

MIT（见 [LICENSE](LICENSE)）。改编内容的署名见 [NOTICE](NOTICE)。

---

## 日本語

> あなたの実験にふさわしい論文を書く。paper-writing-agent は、あなた自身のコード・
> ログ・数値から計算機科学・ソフトウェア工学の論文を起草・改稿し、文章を精確に、
> 統計を誠実に、引用を実在に保ち、AI 指紋を残さない。高インパクトな発表先での採択
> 確率を最大化するために作られている。

### 解決する課題

論文とは実験の非可逆圧縮であり、損失の多くは「書き写し」の途中で起きる。数値が図から
打ち直され、いつのまにか誤る。手法が、実行から一か月後には半分しか思い出せない。引用が、
引かれた文献の言っていないことを述べる。文章が言語モデルのように読め、査読で目印を
付けられる。ひとつひとつの綻びが、正確さを損なうか、査読者の信頼を損なう。

paper-writing-agent はその綻びを埋める。結果をすでに定義している成果物、すなわち
ソースコード・実行スクリプト・設定ファイル・ログ・環境レシピ・full-precision の統計値に
エージェントを向ける。エージェントはそれらから書き、記憶からは書かない。引用を捏造せず、
検定と判定のないまま結果を有意とも言わない。そして、本来は堅実な草稿を機械が書いたように
見せる AI 文章のパターンを取り除く。

### 想定利用者

計算（ドライ）実験を行う研究者。バイオインフォマティクス、機械学習、計算科学、
ソフトウェア工学などで、結果の背後にあるコード・ログ・設定を自ら保有し、それらを
強い発表先に向けた論文に仕立てたい人。ある図の数値がどのディレクトリで生成されたかを
指し示せるなら、本ツールは草稿をそこに接地させ続ける。

### これは何か

paper-writing-agent は2層のハイブリッドである：

- **Claude Code プラグイン**（想定される使い方）。計画→確認→実行→検証のワークフロー
  の下で、あなたと共に計画・起草・改稿するエージェントであり、ジャーナル非依存の執筆
  テンプレート知識ベースを同梱する。
- 決定論的な **Python コア**（`pip install paper-writing-agent`、コマンドは `pwa`）。
  その下で動く engine であり、文章の検査、参考文献の索引化、完成度の追跡、用語定義の
  検査を担う。エディタに非依存で、テストを完全に備える。

プラグインが体験を、コアが信頼できる検査を与える。検査は判断ではなくコードだからだ。
既定値は実用的で、すべて `pwa init` で上書きできる。

### 必要環境

- **[Claude Code](https://claude.com/claude-code)**（必須）。エージェントは Claude
  Code プラグインとして動作し、これが主要インターフェースである。
- **Python 3.10 以降**。プラグインが呼び出す `pwa` コア用。
- あなたの原稿と、その背後にある実験成果物への読み取りアクセス。

`pwa` コアは検査器群として単体でも動くが、執筆ワークフローは Claude Code を前提とする。

### インストール

```bash
pip install paper-writing-agent        # `pwa` コマンドを提供
# またはクローンから：
pip install -e ".[dev]"
```

Claude Code プラグイン（スキル・コマンド・エージェント・知識ベース）は
[plugin/README.md](plugin/README.md) を参照。

### セットアップ：実験の在り処をエージェントに教える

この一手が、情報を失わずに書くことを可能にする。`pwa init` の後、ワークスペースの
`PROJECT_PROFILE.md` を開き、各種の証拠がどこにあるかを記録し、エージェントに読ませる：

| 在り処 | エージェントの用途 |
| --- | --- |
| 結果・出力 | 各図・各表の背後にある数値 |
| 実験ソースコード | 手法の真の記述 |
| 実行スクリプト・ジョブファイル | 各実行がどう起動され設定されたか |
| 設定ファイル | ハイパーパラメータと実験条件 |
| ログ | 実行中に実際に何が起きたか |
| 環境レシピ | 再現可能な Methods のためのバージョン情報 |
| 統計ストア（`stats/`） | full-precision の数値。丸めは本文でのみ |

エージェントは「図からコードへ」の連鎖を `provenance_map.md` に記録するので、原稿中の
どの数値も、それを生んだスクリプトとデータまで辿れる。これらのパスがあれば、Methods は
コードに従い、数値は記憶ではなくストアから来て、出典が支持しないことは何も断言されない。

### クイックスタート

```bash
# 1. 原稿ワークスペースを用意（対話式。--yes で既定値）。
pwa init my-paper/

# 2. my-paper/PROJECT_PROFILE.md に実験の在り処を記録する。そして Claude Code 上で、
#    それらから節を起草するようエージェントに頼む：
#    /pwa-draft introduction

# 3. 全規則で文章を検査。
pwa check my-paper/

# 4. 参考文献から引用文脈索引を構築。
pwa bib build my-paper/bib/refs.bib --output my-paper/bib/bib_index.yaml
pwa bib validate my-paper/bib/bib_index.yaml --bib my-paper/bib/refs.bib --strict

# 5. 各節の完成度を追跡し、模範とする節を探す。
pwa sections sync my-paper/main.tex
pwa sections exemplars introduction

# 6. 読む順序で「一度定義してから使う」を検査。
pwa defs check my-paper/abstract.tex my-paper/introduction.tex
```

### 設計思想（なぜこの形か）

完全版は [docs/DESIGN_PHILOSOPHY.md](docs/DESIGN_PHILOSOPHY.md) を参照。これは高インパクト
論文を書きながら培った執筆規律の、汎用かつ公開の形であり、あらゆる機能と既定値はこれに
照らして判断される。8本の柱：

1. **証拠接地。** すべての主張は出典に解決する：統計ストアの数値、図の来歴チェーン、
   既往用法を記録した引用キー、あるいは定義簿の記号。記憶からは何も断言しない。
2. **AI 臭の排除。** AI 文章には指紋がある（過大な有意性、コピュラ回避、分詞パディング、
   同義語の巡回、無理な三段構え、em ダッシュ、固定語彙）。検査器がそれらを検出し、精確な
   学術表現を提案する。
3. **統計的誠実。** 「有意」は主張ではなく獲得するもの：検定・閾値未満の P 値・明示的な
   判定が要る。裸の P 値は欠陥である。
4. **唯一の真実源。** 各規則と各状態の所有者は一つだけ。いかなる値も重複させない。
5. **計画→確認→実行→検証。** エージェントは計画を述べ、あなたの承認を待ち、承認済みの
   ものだけを実行し、検証する。決定権はあなたにある。
6. **再現性。** 統計は再実行可能で、画像から書き写さない。完成度の変更には日時と理由を
   付す。
7. **硬直ではなく設定可能。** 元のエージェントは単一の著者・単一の発表先に合わせて調整
   されていた。ここでは、発表先・引用形式・綴り・記法・構成・厳格度・運用言語はすべて、
   前提ではなく友好的な既定値を持つ設定項目である。
8. **ドッグフーディング。** 本プロジェクトは pre-commit と CI で、自らの文章を自らの
   検査器で検査する。この README も `pwa lint` を通過する。

3つの信念が既定値を形づくる：

- **ソースコードと成果物こそが一次の真実**であり、記憶や以前の草稿に優先する。技術的
   主張はエージェントが読んだファイルに接地し、辿れないものは断言せず指摘する。
- **何を書かないかは、起草より前に下す決定である。** 各図・各段落・各キャプションに
   ついて、計画は「そこに含めないもの」を述べ、成果を焦点の合ったものに保ち、非専門家
   でも追えるようにする。
- **見出しの一文は、キャッチーさと正確さを両立させる。** ある測定がそれを裏づける
   ときにのみパンチラインは残り、データが支持しない比喩は削られる。

目的：高インパクトな発表先での採択確率の最大化。品質階層：
**正確さ > 明確さ > 簡潔さ > 専門性。** 二つの目標が衝突するときは前者が勝ち、正確さを
簡潔さと引き換えにしない。

### コマンド

| コマンド | 役割 |
| --- | --- |
| `pwa init <dir>` | 設定を作成し原稿ワークスペースを生成。 |
| `pwa lint <paths>` | AI 文章の指紋を検出し置換を提案。 |
| `pwa stats <paths>` | P 値の判定・検定名・数値や単位の体裁を検査。 |
| `pwa defs check <files>` | 読む順序で前方参照と再定義を指摘。 |
| `pwa bib build/validate/ground` | 引用文脈索引の構築・検証・既往用法への接地。 |
| `pwa sections status/sync/set/exemplars` | 完成度の追跡と模範節の選定。 |
| `pwa check <paths>` | 全検査器を一括実行。 |

各検査器はエラー時に非ゼロを返し、`--exit-zero`（警告のみ）と `--format json` に対応する。

### 設定

`pwa init` はプリセット（`strict-high-IF` / `balanced` / `lenient`）と短いウィザードから
`paper-writing-agent.toml` を書き出す。全項目は手で編集できる。設定可能な項目：対象分野・
発表先ティア、引用形式、綴り（米国式/英国式）、P 値記法、有効数字、セクション構成、
図表参照の表記、ヘッジの厳格度、運用言語、プロジェクト固有の禁止語拡張。設計上の不変条件：
有意性には検定と判定が必要、引用は決して捏造しない、決定権はユーザーにある。

### リポジトリ構成

```
paper-writing-agent/
├── src/paper_writing_agent/   # 決定論的コア（エディタ非依存）
│   ├── cli.py                 #   入口：pwa init|lint|bib|stats|sections|defs|check
│   ├── config/                #   設定モデル + プリセット + init ウィザード + TOML 入出力
│   ├── slop/                  #   AI 臭排除リンター（規則・マスキング・エンジン・レポート）
│   ├── bibindex/              #   BibTeX パーサ・文脈索引・スキーマ検証・接地
│   ├── stats/                 #   統計的誠実リンター
│   ├── sections/              #   完成度トラッカー + 模範節
│   ├── definitions/           #   略語登録簿 + 前方参照禁止リンター
│   ├── scaffold.py            #   `pwa init` が使うワークスペース生成器
│   └── templates/workspace/   #   原稿ワークスペーステンプレート（パッケージデータ）
├── plugin/                    # Claude Code プラグイン（エージェント層）
│   ├── skills/ commands/ agents/ knowledge/
│   └── README.md
├── examples/                  # 合成の CS/ソフトウェア実例
├── tests/                     # 各モジュールの pytest テスト
└── docs/                      # 設計思想・アーキテクチャ・要件・スライド
```

`pwa init` が生成する原稿ワークスペースには、あなたの `PROJECT_PROFILE.md`、
`paper_outline.md`、`DEFINITIONS.md`、`citation_policy.md`、`provenance_map.md`、
`section_status.yaml`、`bib/`、`stats/`、および解決済みの `paper-writing-agent.toml` が
含まれる。[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) を参照。

### 2層・1コア

Python コアは純粋・決定論的で単体テスト済み、規則と検査を所有し、エディタに非依存。
Claude Code プラグインはワークフロー・プロンプト・テンプレートを提供し、各検査ではコアを
呼び出す。規則は検証可能なまま、エージェントは自由に編成する。

### スライド

動機と技術的な肝をまとめた9枚のスライドが [docs/slides/](docs/slides/) にある：
[PDF](docs/slides/design-philosophy.pdf) ·
[PPTX](docs/slides/design-philosophy.pptx)（ネイティブ・編集可能）。

### プライバシー

本ツールは汎用かつ領域非依存であり、プロジェクト固有・未公開・著者私有の素材を一切
含まない。すべての実例は合成であり、計算機科学・ソフトウェア領域から作成した。
[NOTICE](NOTICE) を参照。

### 免責事項

本ツールは執筆を支援するものであり、正確性を保証しない。論文中のあらゆる主張・数値・
引用・記述の確認、および提出する原稿に対する責任は、AI や本ツールではなく執筆者本人が負う。

### 貢献

[CONTRIBUTING.md](CONTRIBUTING.md) を参照。本プロジェクトは、原稿に課す規律と同じ規律で
自らの開発を律する。

### ライセンス

MIT（[LICENSE](LICENSE) を参照）。改変したコンテンツの帰属は [NOTICE](NOTICE) に記す。
