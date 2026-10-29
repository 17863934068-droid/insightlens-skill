# GitHub 首次发布文案

以下为首发配置与文案。实际发布状态请查看 [GitHub Release 页面](https://github.com/17863934068-droid/insightlens-skill/releases/tag/v0.1.0-preview)。

## 仓库

- 名称：`insightlens-skill`
- 可见性：公开。
- 简介：将用户访谈转录稿整理为可回溯的分析草稿，并标出需要核对的疑点。A skill for evidence-linked interview analysis and review.
- Topics：`agent-skills`、`user-research`、`ux-research`、`interview-analysis`。
- 首页：使用根目录的 `README.md`，不将网页地址作为使用依赖。
- 许可证：MIT。

## 首次 Release

标签：`v0.1.0-preview`

标题：`InsightLens v0.1.0-preview · 访谈分析与疑点审阅`

类型：Pre-release。尚无真实用户验证，避免以稳定版发布。

可直接使用的正文：

```markdown
InsightLens 的首个预览版本，面向需要整理用户访谈的产品经理、设计师和研究者。

提供的能力：

- 按统一结构逐份分析转录稿，再综合共同点、差异和反例。
- 为关键发现保留直接引文与原文定位。
- 审阅已有结论中的引用失配、概括过度、限制遗漏和推断越界。
- 将资料不足单列提示，保留研究者的最终判断。
- 附带只依赖 Python 标准库的引用逐字核验脚本。

开始使用：按 README 将 `skills/insightlens-interview-analysis` 安装到目标工具支持的 Skill 目录，先运行 `examples/meeting-review` 中的合成示例。

当前验证：6 项引用脚本测试通过，并完成干净目录中的显式文件加载试运行。尚未验证全新工具环境的自动发现、跨工具兼容性或真实用户效果。示例结果不代表准确率或效率提升。

本包不包含模型服务、录音转写功能或网页服务。MIT 许可证适用于随包内容。

欢迎反馈：使用的工具和模型、问题描述、期望行为，以及可公开的合成或脱敏最小样本。请勿提交真实姓名、账号凭据或未经授权的访谈记录。
```

## 上传边界

以此独立目录为仓库根，只上传候选包文件。不要把原网页工程、安装检查项目、账号配置或个人访谈记录合并进来。发布成功后，应将 README 的“本地候选版”状态改为真实发布状态，并补上实际仓库与 Release 链接。
