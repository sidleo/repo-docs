# repo-docs：中文项目文档 Skill

为不同 Agent 提供一套可复用的项目文档工作流：先检查项目实际文件，再生成或更新 **AGENTS.md 协作规则**与 **README.md 项目说明**。

适用于代码仓库、脚本工具、数据分析项目、文档项目和尚在初始化的目录。它是文本指令型 skill，使用时无需构建，没有运行服务或第三方依赖。

## 两份文档的分工

| 文件 | 读者需要了解的内容 |
| --- | --- |
| `AGENTS.md` | 应怎样修改项目、遵循什么约定、执行什么验证、怎样提交和交付。 |
| `README.md` | 项目是什么、能做什么、如何开始使用、目录结构与配置在哪里。 |

默认中文输出；文件名、命令与代码标识保留原文。支持只生成其中一份，已有内容按事实合并更新。

## 文件结构

```text
repo-docs/
├── SKILL.md                      # skill 入口、探查与交付流程
├── references/
│   ├── agents-guide.md           # AGENTS.md 写作规范
│   └── readme-guide.md           # README.md 写作规范
└── agents/
    └── openai.yaml               # 可选界面元数据，其他宿主可忽略
```

跨 Agent 使用时保留完整 `repo-docs/` 目录。[SKILL.md](repo-docs/SKILL.md) 中的相对链接会按需读取两份规范。仓库的 `scripts/package.py` 用于打包，`dist/` 存放分发文件。

## 下载与安装

- [repo-docs.skill](dist/repo-docs.skill)：完整 skill 安装包，供支持 `.skill` 格式的宿主导入。
- [repo-docs.zip](dist/repo-docs.zip)：完整 skill 目录与本使用说明，供手动解压安装。

`.skill` 使用 ZIP 封装，包内入口为 `repo-docs/SKILL.md`。手动安装时将完整 `repo-docs/` 目录放入目标 Agent 的 skill 目录。安装位置和加载方式遵循宿主配置。

## 使用方式

将 `repo-docs/` 放入目标 Agent 已确认支持的 skill 目录，按该宿主的方式发现并调用。不同 Agent 的目录与快捷命令可能不同；不能仅凭放入文件就断言已加载。

支持 `$skill-name` 的宿主可这样调用：

```text
使用 $repo-docs，为当前项目生成中文 AGENTS.md 和 README.md。
```

也可以指定范围：

```text
使用 repo-docs，只更新 README.md，保留现有的人工维护章节。
```

```text
使用 repo-docs，为指定项目更新两份中文文档，保留仍有效的项目约定。
```

没有 skill 加载功能，但能读取文件的 Agent，也可以直接执行：

```text
请读取 repo-docs/SKILL.md，并按其中指引读取本次需要的 references 文档，
为当前项目生成或更新中文 AGENTS.md 和 README.md。
```

路径应相对于该 Agent 的实际工作目录调整。若宿主不能读写文件，提供完整 skill 与相关规范内容，让它输出两份带文件名的正文，再保存到项目。

本 skill 只负责 AGENTS.md 和 README.md 的内容。其他 Agent 的入口文件、软链接与环境配置由使用者的环境管理，不属于本 skill 的工作范围。

## 相比原提示词的改进

- 以中文表达和篇幅习惯编写；章节按项目裁剪。
- 先读项目再写，命令、路径、测试、配置和提交约定都需要依据。
- README.md 补全项目用途、能力边界与最短使用路径，AGENTS.md 聚焦协作规则。
- 更新前检查已有内容，保留有效规则与人工章节。
- 空项目、无 Git 历史、无测试或仅有文档时照实描述。
- 交付时区分实际执行与配置核对；无变化时保持文件不变。

## 验证与维护

本项目没有自动化测试框架。修改 skill 后检查 YAML 元数据、相对链接和 Markdown 格式，再用实际项目检查生成结果的事实依据、两份文档的分工及旧内容保留情况。新增宿主专用适配时，保持核心 SKILL.md 不依赖该宿主。

维护者使用 Python 3.9 或更新版本，在仓库根目录重新生成两个分发包：

```bash
python3 scripts/package.py
```

打包只写入 `dist/repo-docs.skill` 和 `dist/repo-docs.zip`，不改变任何 Agent 的环境配置；源文件未变时保持包内容和修改时间不变。
