# paper-writing-agent

> 一个以证据为本、杜绝 AI 腔的科研论文写作智能体，面向计算机科学与软件工程论文，
> 目标是最大化高影响力期刊或会议的录用概率。

**语言：** [English](README.md) · 简体中文 · [日本語](README.ja.md)

## 这是什么

paper-writing-agent 帮助你起草与修订科研论文，使行文精确、统计诚实、引用真实、
文本不带 AI 指纹。它是一个**混合体**：

- 一个确定性的 **Python 内核**（`pip install paper-writing-agent`，命令为 `pwa`），
  用于检查行文、建立文献索引、跟踪完成度、校验术语定义；以及
- 一个 **Claude Code 插件**，以智能体方式驱动内核，并附带一套与期刊无关的写作模板
  知识库。

开箱即用的合理默认值；一切都可通过 `pwa init` 覆盖。

## 设计理念（为什么这样做）

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

## 幻灯片

关于动机与技术内核的九页幻灯片位于 [docs/slides/](docs/slides/)：
[PDF](docs/slides/design-philosophy.pdf) ·
[PPTX](docs/slides/design-philosophy.pptx)（原生、可编辑）。

## 安装

```bash
pip install paper-writing-agent        # 提供 `pwa` 命令
# 或从克隆仓库安装：
pip install -e ".[dev]"
```

Claude Code 插件请见 [plugin/README.md](plugin/README.md)。

## 快速开始

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

## 命令

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

## 配置

`pwa init` 会基于预设（`strict-high-IF` / `balanced` / `lenient`）与简短向导写出
`paper-writing-agent.toml`，所有取值均可手动编辑。可配置项包括目标领域与场所层级、
引用风格、拼写（美式/英式）、P 值记法、有效数字、章节结构、图表引用风格、对冲措辞
严格度、运行语言，以及项目本地的禁用词扩展。设计上的不变量：显著性需要检验与结论判定、
绝不臆造引用、决定权在用户。

## 两层一核

Python 内核纯粹、确定且经过单元测试，拥有规则与检查，且不依赖任何编辑器；Claude Code
插件提供工作流、提示词与模板，并调用内核执行每一项检查。见
[ARCHITECTURE.md](docs/ARCHITECTURE.md)。

## 隐私

这是一个通用、与领域无关的工具，不含任何项目专有、未发表或作者私有的材料。所有示例
均为合成内容，取自计算机科学与软件领域。见 [NOTICE](NOTICE)。

## 参与贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。本项目以其要求于论文的同等纪律来约束自身的开发。

## 许可证

MIT（见 [LICENSE](LICENSE)）。改编内容的署名见 [NOTICE](NOTICE)。
