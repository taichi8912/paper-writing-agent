# paper-writing-agent

[English](#english) · [简体中文](#简体中文) · [日本語](#日本語)

## English

> An evidence-grounded, anti-AI-slop manuscript-writing agent for
> computer-science and software-engineering papers, engineered to maximize
> acceptance at high-impact venues.

### What it is

paper-writing-agent helps you draft and revise scientific papers so that the
prose is precise, the statistics are honest, the citations are real, and the text
carries no AI fingerprints. It is a **hybrid**:

- a deterministic **Python core** (`pip install paper-writing-agent`, command
  `pwa`) that lints prose, indexes a bibliography, tracks completion, and checks
  definitions; and
- a **Claude Code plugin** that drives the core agentically and ships a knowledge
  base of journal-agnostic writing templates.

Sensible defaults out of the box; everything is overridable through `pwa init`.

### Why it works this way (design philosophy)

The full statement is in [docs/DESIGN_PHILOSOPHY.md](docs/DESIGN_PHILOSOPHY.md).
In short, eight pillars:

1. **Evidence grounding.** Every claim resolves to a source: a number, a figure's
   provenance, a citation, or a definition.
2. **Anti-AI-slop.** AI prose has fingerprints; the linter finds them and
   proposes precise academic replacements.
3. **Statistical honesty.** "Significant" needs a test, a P-value, and an
   explicit verdict.
4. **Single source of truth.** Each rule and each piece of state has one owner.
5. **Plan, confirm, execute, verify.** The user holds decision authority.
6. **Reproducibility.** Statistics are re-runnable; changes are auditable.
7. **Configurable, not rigid.** Venue, citation style, spelling, and strictness
   are settings, not assumptions.
8. **Dogfooding.** The project lints its own prose with its own linter.

Objective: maximize acceptance at a high-impact venue. Quality hierarchy:
**Accuracy > Clarity > Conciseness > Professionalism.**

### Slides

A nine-slide deck on the motivation and technical core lives in
[docs/slides/](docs/slides/):
[PDF](docs/slides/design-philosophy.pdf) ·
[PPTX](docs/slides/design-philosophy.pptx) (native, editable).

### Install

```bash
pip install paper-writing-agent        # provides the `pwa` command
# or, from a clone:
pip install -e ".[dev]"
```

For the Claude Code plugin, see [plugin/README.md](plugin/README.md).

### Quickstart

```bash
# 1. Set up a manuscript workspace (interactive; or add --yes for defaults).
pwa init my-paper/

# 2. Write, then check your prose against every rule.
pwa check my-paper/

# 3. Build a citation context index from your bibliography.
pwa bib build my-paper/bib/refs.bib --output my-paper/bib/bib_index.yaml
pwa bib validate my-paper/bib/bib_index.yaml --bib my-paper/bib/refs.bib --strict

# 4. Track section completion and find exemplars to imitate.
pwa sections sync my-paper/main.tex
pwa sections exemplars introduction

# 5. Check define-once discipline in reading order.
pwa defs check my-paper/abstract.tex my-paper/introduction.tex
```

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

Each linter exits non-zero on errors, accepts `--exit-zero` for warn-only use,
and supports `--format json`.

### Configuration

`pwa init` writes `paper-writing-agent.toml` from a preset
(`strict-high-IF` / `balanced` / `lenient`) and a short wizard. Every value is
editable by hand. Configurable knobs include target field and venue tier,
citation style, spelling (US/UK), P-value notation, significant figures, section
structure, figure-reference style, hedging strictness, operating language, and
project-local forbidden-word extensions. Invariant by design: significance needs
a test and a verdict, citations are never fabricated, and the user decides.

### Two layers, one core

The Python core is pure, deterministic, and unit-tested; it owns the rules and
the checks and has no editor dependency. The Claude Code plugin supplies the
workflow, prompts, and templates, and calls the core for every check. See
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

### Privacy

This is a generic, domain-agnostic tool. It contains no project-specific,
unpublished, or author-private material. All worked examples are synthetic and
drawn from the computer-science and software domains. See [NOTICE](NOTICE).

### Disclaimer

This tool assists with writing; it does not guarantee correctness. Verifying
every claim, number, citation, and statement, and accountability for the
submitted manuscript, rest with the author, not with the AI or this tool.

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The project holds its own development to
the same discipline it enforces on manuscripts.

### License

MIT (see [LICENSE](LICENSE)). Attribution for adapted content is in
[NOTICE](NOTICE).

---

## 简体中文

> 一个以证据为本、杜绝 AI 腔的科研论文写作智能体，面向计算机科学与软件工程论文，
> 目标是最大化高影响力期刊或会议的录用概率。

### 这是什么

paper-writing-agent 帮助你起草与修订科研论文，使行文精确、统计诚实、引用真实、
文本不带 AI 指纹。它是一个**混合体**：

- 一个确定性的 **Python 内核**（`pip install paper-writing-agent`，命令为 `pwa`），
  用于检查行文、建立文献索引、跟踪完成度、校验术语定义；以及
- 一个 **Claude Code 插件**，以智能体方式驱动内核，并附带一套与期刊无关的写作模板
  知识库。

开箱即用的合理默认值；一切都可通过 `pwa init` 覆盖。

### 设计理念（为什么这样做）

完整说明见 [DESIGN_PHILOSOPHY.md](docs/DESIGN_PHILOSOPHY.md)。简要而言，八根支柱：

1. **证据为本。** 每个论断都可追溯到来源：数值、图的溯源、引用或定义。
2. **杜绝 AI 腔。** AI 行文有指纹；检查器会发现它们并给出精确的学术替换。
3. **统计诚实。** “显著”需要检验、P 值以及明确的结论判定。
4. **唯一真实来源。** 每条规则与每份状态只有一个归属。
5. **先计划、再确认、后执行、终核验。** 决定权属于用户。
6. **可复现。** 统计可重新运行；变更可审计。
7. **可配置而非僵化。** 期刊、引用风格、拼写、严格度都是设置项，而非默认假设。
8. **自食其果（dogfooding）。** 本项目用自己的检查器检查自己的文字。

目标：最大化高影响力场所的录用概率。质量层级：
**准确 > 清晰 > 简洁 > 专业。**

### 幻灯片

关于动机与技术内核的九页幻灯片位于 [docs/slides/](docs/slides/)：
[PDF](docs/slides/design-philosophy.pdf) ·
[PPTX](docs/slides/design-philosophy.pptx)（原生、可编辑）。

### 安装

```bash
pip install paper-writing-agent        # 提供 `pwa` 命令
# 或从克隆仓库安装：
pip install -e ".[dev]"
```

Claude Code 插件请见 [plugin/README.md](plugin/README.md)。

### 快速开始

```bash
# 1. 建立论文工作区（交互式；或加 --yes 使用默认值）。
pwa init my-paper/

# 2. 写作后，按全部规则检查行文。
pwa check my-paper/

# 3. 由参考文献建立引用上下文索引。
pwa bib build my-paper/bib/refs.bib --output my-paper/bib/bib_index.yaml
pwa bib validate my-paper/bib/bib_index.yaml --bib my-paper/bib/refs.bib --strict

# 4. 跟踪各节完成度并查找可借鉴的范例。
pwa sections sync my-paper/main.tex
pwa sections exemplars introduction

# 5. 按阅读顺序检查“术语先定义后使用”。
pwa defs check my-paper/abstract.tex my-paper/introduction.tex
```

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

### 两层一核

Python 内核纯粹、确定且经过单元测试，拥有规则与检查，且不依赖任何编辑器；Claude Code
插件提供工作流、提示词与模板，并调用内核执行每一项检查。见
[ARCHITECTURE.md](docs/ARCHITECTURE.md)。

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

> 証拠に接地し、AI 臭を排した科学論文執筆エージェント。計算機科学・ソフトウェア
> 工学の論文を対象に、高インパクトな発表先での採択確率を最大化することを目的とする。

### これは何か

paper-writing-agent は、文章が精確で、統計が誠実で、引用が実在し、AI 指紋を含まない
論文の起草・改稿を支援する。本ツールは**ハイブリッド**である：

- 決定論的な **Python コア**（`pip install paper-writing-agent`、コマンドは `pwa`）。
  文章の検査、参考文献の索引化、完成度の追跡、用語定義の検査を担う。
- **Claude Code プラグイン**。コアをエージェント的に駆動し、ジャーナル非依存の
  執筆テンプレート知識ベースを同梱する。

既定値は実用的で、すべて `pwa init` で上書きできる。

### 設計思想（なぜこの形か）

完全版は [DESIGN_PHILOSOPHY.md](docs/DESIGN_PHILOSOPHY.md) を参照。要点は8本の柱：

1. **証拠接地。** すべての主張は出典（数値・図の来歴・引用・定義）に解決する。
2. **AI 臭の排除。** AI 文章には指紋がある。検査器がそれを検出し、精確な学術表現を提案する。
3. **統計的誠実。** 「有意」には検定・P 値・明示的な判定が必要。
4. **唯一の真実源。** 各規則と各状態の所有者は一つだけ。
5. **計画→確認→実行→検証。** 決定権はユーザーにある。
6. **再現性。** 統計は再実行可能で、変更は監査可能。
7. **硬直ではなく設定可能。** 発表先・引用形式・綴り・厳格度は前提ではなく設定項目。
8. **ドッグフーディング。** 本プロジェクトは自らの文章を自らの検査器で検査する。

目的：高インパクトな発表先での採択確率の最大化。品質階層：
**正確さ > 明確さ > 簡潔さ > 専門性。**

### スライド

動機と技術的な肝をまとめた9枚のスライドが [docs/slides/](docs/slides/) にある：
[PDF](docs/slides/design-philosophy.pdf) ·
[PPTX](docs/slides/design-philosophy.pptx)（ネイティブ・編集可能）。

### インストール

```bash
pip install paper-writing-agent        # `pwa` コマンドを提供
# またはクローンから：
pip install -e ".[dev]"
```

Claude Code プラグインは [plugin/README.md](plugin/README.md) を参照。

### クイックスタート

```bash
# 1. 原稿ワークスペースを用意（対話式。--yes で既定値）。
pwa init my-paper/

# 2. 執筆後、全規則で文章を検査。
pwa check my-paper/

# 3. 参考文献から引用文脈索引を構築。
pwa bib build my-paper/bib/refs.bib --output my-paper/bib/bib_index.yaml
pwa bib validate my-paper/bib/bib_index.yaml --bib my-paper/bib/refs.bib --strict

# 4. 各節の完成度を追跡し、模範とする節を探す。
pwa sections sync my-paper/main.tex
pwa sections exemplars introduction

# 5. 読む順序で「一度定義してから使う」を検査。
pwa defs check my-paper/abstract.tex my-paper/introduction.tex
```

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

`pwa init` はプリセット（`strict-high-IF` / `balanced` / `lenient`）と短い
ウィザードから `paper-writing-agent.toml` を書き出す。全項目は手で編集できる。
設定可能な項目：対象分野・発表先ティア、引用形式、綴り（米国式/英国式）、P 値記法、
有効数字、セクション構成、図表参照の表記、ヘッジの厳格度、運用言語、プロジェクト
固有の禁止語拡張。設計上の不変条件：有意性には検定と判定が必要、引用は決して捏造しない、
決定権はユーザーにある。

### 2層・1コア

Python コアは純粋・決定論的で単体テスト済み、規則と検査を所有し、エディタに非依存。
Claude Code プラグインはワークフロー・プロンプト・テンプレートを提供し、各検査では
コアを呼び出す。[ARCHITECTURE.md](docs/ARCHITECTURE.md) を参照。

### プライバシー

本ツールは汎用かつ領域非依存であり、プロジェクト固有・未公開・著者私有の素材を
一切含まない。すべての実例は合成であり、計算機科学・ソフトウェア領域から作成した。
[NOTICE](NOTICE) を参照。

### 免責事項

本ツールは執筆を支援するものであり、正確性を保証しない。論文中のあらゆる主張・数値・
引用・記述の確認、および提出する原稿に対する責任は、AI や本ツールではなく執筆者本人が負う。

### 貢献

[CONTRIBUTING.md](CONTRIBUTING.md) を参照。本プロジェクトは、原稿に課す規律と
同じ規律で自らの開発を律する。

### ライセンス

MIT（[LICENSE](LICENSE) を参照）。改変したコンテンツの帰属は [NOTICE](NOTICE) に記す。
