# InsightLens · 访谈分析与疑点审阅 Skill

将访谈转录稿整理为结构统一、可回溯的分析草稿，并标出需要研究者核对的具体表述。

**状态：v0.1.0-preview · 预览版。** 当前包含合成示例和引用检查测试；尚无真实用户测试、效率提升或语义准确率验证。采用 MIT 许可证。

[GitHub 仓库](https://github.com/17863934068-droid/insightlens-skill) · [预览版与下载](https://github.com/17863934068-droid/insightlens-skill/releases/tag/v0.1.0-preview)

## 它帮助你做什么

面向需要整理多份访谈材料的产品经理、UX 设计师和研究者，减少反复交代分析要求、输出难以比较和查找原文的工作。

| 使用方式 | 你提供 | 你得到 |
| --- | --- | --- |
| 分析访谈 | 研究问题、转录稿、受访者编号 | 单份分析、跨访谈综合、洞察草稿、产品机会、原文证据与待核对项 |
| 审阅已有洞察 | 原稿和带编号的已有结论 | 存疑片段、具体原因、相关原文、候选修订及材料缺失提示 |
| 核验引用 | 指定来源、段落和直接引文的 JSON | 逐字匹配、指定定位失配或无法核验的检查结果 |

分析时区分受访者表述、解释、假设和产品机会。审阅时关注引用失配、概括过度、限制遗漏和推断越界。没有被标疑点，不等于结论已确认正确。

## 使用条件

- 需要能加载 Skill 指令并读取相关文件的 AI 工具。本包以 Codex 的 Skill 使用方式编写，尚未完成其他工具的兼容性测试。
- 语义分析由你使用的模型完成；本包不包含模型服务、API 密钥或模型调用额度。
- 输入以可读取的转录文本为主。录音转写、扫描 PDF 识别和 Word 解析依赖运行环境，本包不提供这些解析器。
- 引用核验脚本使用 Python 3，仅依赖标准库；模型所在环境无法执行脚本时，应说明未完成脚本核验，不能声称已经运行。
- 本包没有网络调用代码，但 AI 工具如何处理材料取决于你所使用的平台。请按所在团队要求处理真实访谈资料。

## 下载与安装

可在 GitHub 的 **Code → Download ZIP** 下载源码，或从上方预览版页面下载压缩包并解压。在解压后的根目录开始操作。

### Codex：先在一个项目中试用

把 `skills/insightlens-interview-analysis` 整个文件夹复制到目标项目的 `.agents/skills/` 中，形成：

```text
你的项目/
└── .agents/skills/insightlens-interview-analysis/
    ├── SKILL.md
    ├── references/
    └── scripts/
```

在该项目中打开 Codex，选择此 Skill，或在支持 `$` 调用的界面输入 `$insightlens-interview-analysis`。没有出现时重启后检查。若已经存在同名 Skill，请先比较版本，避免直接覆盖自己的修改。

个人范围安装可将同一文件夹放到 `~/.agents/skills/`。以上为官方文档所述加载方式；本候选包还未完成全新环境的安装验收。安装依据：[OpenAI 官方 Build skills 文档](https://learn.chatgpt.com/docs/build-skills)（核对日期：2026-10-29）。该文档也建议通过插件进行更完整的分发；本阶段先提供可手动安装的 Skill 文件夹。

### 第一次运行：使用合成示例

在本候选包目录中让 AI 读取以下指令。若已安装，可用 Skill 名调用；未安装时，可明确指定 `skills/insightlens-interview-analysis/SKILL.md`，并要求读取其中相关引用文件。后者是文件式试用，不算安装验收。

```text
使用 $insightlens-interview-analysis。
请读取 examples/meeting-review/input.json，审阅其中全部 claims。
只以其中 sources 为证据，保留结论原文与编号。
标出具体疑点，附原因、原文定位和候选修订；材料缺失单独说明。
所有结果保持待审阅，不替我确认。
```

完成后再看 [示例说明](examples/meeting-review/README.md) 和 `sample-review.json`。示例输出来自先前的合成材料试运行，是供理解结构和边界的记录，不是唯一标准措辞，也不是运行时默认答案。

## 用于自己的材料

### 从转录稿开始

```text
使用 $insightlens-interview-analysis。
研究问题：用户为什么在预约过程中放弃？
材料：我提供的 T01.txt、T02.txt、T03.txt。
受访者：分别为 U01、U02、U03。
先分别分析，再综合共同点、差异和反例。
为洞察保留原文定位，区分事实、解释、假设与产品机会。
请将结果整理为 Markdown 草稿，并标出需要我核对的部分。
```

### 检查已有分析

```text
使用 $insightlens-interview-analysis。
原稿是我提供的 transcripts/，已有结论是 insights.md。
请保留原结论及编号，检查结论与原稿之间的关系。
标记存疑片段并解释原因，缺材料时说明需要补什么。
先给审阅清单，不直接覆盖原稿或替我确认结论。
```

按实际文件位置修改示例路径。跨访谈统计请提供受访者编号；同一人的追访使用同一编号。

## 输出与人工判断

完整分析的结构见 [统一输出结构](skills/insightlens-interview-analysis/references/output-schema.md)。审阅字段和引用检查输入见 [疑点审阅规则](skills/insightlens-interview-analysis/references/doubt-review.md)。

- **待审阅**：分析生成，或已有内容尚未确认。
- **已编辑待核对**：结论发生修改，需要重新检查。
- **已确认**：只有使用者明确确认后才记录。
- **已排除**：保留原因，可恢复。

这是 AI 应遵循的记录约定；Skill 文件本身不提供数据库或独立网页，也不会自动跨会话保存状态。需要持续追踪时，请把结果和修改记录保存为文件。

## 独立运行引用检查

在本候选包根目录执行：

```sh
python3 skills/insightlens-interview-analysis/scripts/check_evidence.py tests/fixtures/citation-input.json
python3 -m unittest discover -s tests -v
```

第一条使用故意包含问题的合成样本，预期为 **4 条匹配、3 条失配、3 条无法核验，退出码 1**；这不是脚本运行失败。全部引用匹配时退出码 0，输入格式错误时为 2。脚本只查指定段落中的逐字引用，不能判断洞察语义是否正确。

## 文件结构

```text
skills/insightlens-interview-analysis/  可安装的核心 Skill
examples/meeting-review/              合成输入、调用指令与审阅输出
tests/                               引用脚本测试及合成夹具
evaluation/                          已完成检查及其局限
docs/                                发布准备记录
```

本目录是独立的 Skill 仓库。原网页工程中的同名 Skill 是本次整理前的来源；后续公开版修改在此维护，并在需要时同步回网页工程。

## 当前边界与许可证

不同模型、上下文长度和材料质量会影响结果；长访谈可能需要分批处理并检查覆盖范围。合成样本检查不能替代真实研究验证。详见 [验证说明](evaluation/README.md)。

候选包附有 [MIT 许可证](LICENSE)，版权署名为 `InsightLens contributors`。允许使用、修改和分发（包括商业使用），分发时需保留版权与许可声明。全文依据 [Open Source Initiative 的 MIT 许可证文本](https://opensource.org/license/mit)。正式发布准备见 [发布准备](docs/release-preparation.md)。
