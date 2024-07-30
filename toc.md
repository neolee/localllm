# 基于本地 LLM 的应用示例代码

- *Garfield* 聊天机器人框架升级
  - `bot.py`：聊天机器人（*bot*）的公共父类
  - `builtin_bots.py`：内置的示例 *bots*
  - `garfield.py`：聊天系统整合类
- 本地 LLM 通用 *helper*
  - `api.py`：基于 `openai` 标准 API 接口的通用 *helper*
  - `system_message.txt`：系统提示词的可编辑文本
- 基于本地 LLM 的聊天机器人
  - `llm_chat.py`：基于本地 LLM 的简单聊天命令行程序
  - `llm_bot.py`：整合进 *Garfield* 系统的、基于本地 LLM 的聊天机器人，包括简单和流式输出两个版本
- 基于本地 LLM 的 RAG 简单示例
  - `rag_db_create.py`：基于文档生成 RAG 所需向量数据库的示例
  - `rag_qa_only.py`：基于生成好的向量数据库进行简单问答的示例
  - `rag_chat.py`：基于生成好的向量数据库进行问答的聊天命令行程序
