# paper-writing-agent

> 証拠に接地し、AI 臭を排した科学論文執筆エージェント。計算機科学・ソフトウェア
> 工学の論文を対象に、高インパクトな発表先での採択確率を最大化することを目的とする。

**言語：** [English](../README.md) · [中文](README.zh.md) · 日本語（本文）

## これは何か

paper-writing-agent は、文章が精確で、統計が誠実で、引用が実在し、AI 指紋を含まない
論文の起草・改稿を支援する。本ツールは**ハイブリッド**である：

- 決定論的な **Python コア**（`pip install paper-writing-agent`、コマンドは `pwa`）。
  文章の検査、参考文献の索引化、完成度の追跡、用語定義の検査を担う。
- **Claude Code プラグイン**。コアをエージェント的に駆動し、ジャーナル非依存の
  執筆テンプレート知識ベースを同梱する。

既定値は実用的で、すべて `pwa init` で上書きできる。

## 設計思想（なぜこの形か）

完全版は [DESIGN_PHILOSOPHY.md](DESIGN_PHILOSOPHY.md) を参照。要点は8本の柱：

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

## インストール

```bash
pip install paper-writing-agent        # `pwa` コマンドを提供
# またはクローンから：
pip install -e ".[dev]"
```

Claude Code プラグインは [plugin/README.md](../plugin/README.md) を参照。

## クイックスタート

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

## コマンド

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

## 設定

`pwa init` はプリセット（`strict-high-IF` / `balanced` / `lenient`）と短い
ウィザードから `paper-writing-agent.toml` を書き出す。全項目は手で編集できる。
設定可能な項目：対象分野・発表先ティア、引用形式、綴り（米国式/英国式）、P 値記法、
有効数字、セクション構成、図表参照の表記、ヘッジの厳格度、運用言語、プロジェクト
固有の禁止語拡張。設計上の不変条件：有意性には検定と判定が必要、引用は決して捏造しない、
決定権はユーザーにある。

## 2層・1コア

Python コアは純粋・決定論的で単体テスト済み、規則と検査を所有し、エディタに非依存。
Claude Code プラグインはワークフロー・プロンプト・テンプレートを提供し、各検査では
コアを呼び出す。[ARCHITECTURE.md](ARCHITECTURE.md) を参照。

## プライバシー

本ツールは汎用かつ領域非依存であり、プロジェクト固有・未公開・著者私有の素材を
一切含まない。すべての実例は合成であり、計算機科学・ソフトウェア領域から作成した。
[NOTICE](../NOTICE) を参照。

## 貢献

[CONTRIBUTING.md](../CONTRIBUTING.md) を参照。本プロジェクトは、原稿に課す規律と
同じ規律で自らの開発を律する。

## ライセンス

MIT（[LICENSE](../LICENSE) を参照）。改変したコンテンツの帰属は [NOTICE](../NOTICE) に記す。
