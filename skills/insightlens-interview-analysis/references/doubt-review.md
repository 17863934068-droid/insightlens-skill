# 疑点审阅规则

## 检查的边界

审阅的对象是“结论与所提供材料之间的关系”，不是用模型知识判定受访者是否说了事实。受访者猜测本身可以被忠实引用，但分析不能将猜测升级为事实。

先声明材料与结论是否完整可读。缺少原稿、只给节选或引用定位缺失时，记录检查限制；不能因为没有看到证据就断言它在完整原稿中不存在。

缺少来源或指定段落时，在 `scopeNotices` 单列 `unverifiable` 提示并关联受影响的结论；不为凑齐四类而标成“推断越界”或“已核实引用失配”。若同一结论另有可核验的语义问题，可另列疑点；资料补齐后再更新检查结果。

## 四类疑点

| category | 标签 | 标记依据 | 不应标记的情况 |
| --- | --- | --- | --- |
| citation_mismatch | 引用失配 | 指定原文段落已提供且可读，但所引文本未出现在该段；应展示查找结果 | 指定来源/段落未提供时仅提示无法核验；引文存在但观点有争议，或不同文稿恰有同句，不因此断言错引 |
| overgeneralization | 概括过度 | “所有/共同/普遍”超出实际支持者范围，将未表态当支持，错误合并不同诉求 | “所提供两份访谈均提到”的确有两份支持；不能看到“都”就标记 |
| omitted_condition | 限制遗漏 | 省去原文中的时间、对象、前提或例外后改变了含义 | 主题标题可以简短；应连同完整条目阅读，条件已在正文中清楚保留时不重复报警 |
| unsupported_inference | 推断越界 | 将猜测写成原因事实，凭空补人物属性，或未比较就断言产品首要级 | 明确写为有依据的待验证假设/候选机会并保留边界；不因出现产品建议就标记 |

同一结论可有多项不同疑点；同一片段同一问题不重复标记。明确的相反原文比“材料没提到”更有力。证据少不等于错误，但应限制结论范围。

逐字引文匹配后仍须检查说话人、转述对象、否定和情态。例如“系统把‘可能周五’写成‘周五必须交’”不能作为受访者承诺周五交付的证据。区分访谈员的引导问题与受访者自己的表态；对同一人的追访按稳定 participantId 去重，不按文件数计算支持人数。

## 两种判断性质

- `verified_mismatch`：通过指定的可读原文逐字核查，确认引用或定位失配。只针对引用关系；不等于整条洞察已被证伪。
- `needs_review`：语义判断有争议、证据范围不足、遗漏限制、推断尚无依据。具体说明疑点，不写成已确认错误。

材料缺失导致无法核验时，不使用 `verified_mismatch`。不提供未经校准的准确率或置信度百分比。

## 输出字段

默认可读清单；用户需要程序接入时输出相同含义的 JSON。保留 target 原文，不能悄悄润色再作为审阅对象。

```json
{
  "reviewScope": {"sourceIds": ["T01"], "limitations": []},
  "scopeNotices": [],
  "issues": [{
    "id": "D01-Q01",
    "targetId": "D01",
    "targetText": "原结论全文",
    "span": "原结论中逐字存在的具体存疑片段",
    "category": "overgeneralization",
    "assessment": "needs_review",
    "reason": "说明原结论超出哪些具体证据",
    "relatedEvidence": [{"sourceId": "T01", "paragraphId": "T01-P001", "quote": "对应原文的直接引文", "relation": "limits"}],
    "missingEvidence": [],
    "suggestedRevision": "供研究者考虑的修订；证据不足时也可为空",
    "status": "pending"
  }],
  "reviewedTargets": [{"targetId":"D01", "targetText":"原结论全文", "issueIds":["D01-Q01"], "scopeNoticeIds":[], "reviewOutcome":"flagged_for_review"}]
}
```

`relation` 使用 `supports`、`contradicts`、`limits`、`no_position`。不是每项都要填四种关系，未表态不能作为相反意见。引用失配时，不将错误引文放进 relatedEvidence 伪装成有效证据；在原因中保留原始错误引用，相关证据只收录核验过的原文。

若某处缺少依据，在 missingEvidence 说明需要什么材料，不能编造“反对原文”。所有新疑点初始为 pending。没有疑点时 issues 为 []，仍保留范围和限制。

完整覆盖每个输入结论，`reviewedTargets` 保留原文、issueIds 和 scopeNoticeIds。`reviewOutcome` 使用 `flagged_for_review`、`unverifiable`、`no_issue_identified_in_provided_materials`；有可核验疑点时优先标待复核，单纯缺材料用 unverifiable。空疑点清单不能让人误以为所有输入都已检查。

缺材料提示格式：`{"id":"D02-N01","targetId":"D02","status":"unverifiable","sourceId":"T02","paragraphId":"T02-P001","reason":"所指原稿未提供，尚不能核验","neededMaterial":"T02 原稿及对应段落"}`。它是资料完整性提示，不算四类疑点之一，不计入已发现错误数量。

## 引用核验脚本

```text
python3 scripts/check_evidence.py input.json --output report.json
```

输入：

```json
{
  "sources": [{"sourceId":"T01", "paragraphs":[{"id":"T01-P001", "text":"原文内容"}]}],
  "citations": [{"id":"E01", "sourceId":"T01", "paragraphId":"T01-P001", "quote":"原文内容"}]
}
```

脚本核查：来源存在、段落属于指定来源、引用非空且逐字出现在该段。输出 `match`、`mismatch`、`unverifiable`：来源或段落未提供属于不可核验；在提供的段落中查不到引文属于指定定位失配，不证明全稿没有此句话。忽略空白后相同只提供可能的格式差异线索，不自动通过。

退出码 0 表示指定引用均匹配；1 表示发现失配或无法核验；2 表示输入格式错误。逐字匹配不能证明概括、因果或优先级正确，也不能区分两份原稿中完全相同的句子本来应指哪一位。
