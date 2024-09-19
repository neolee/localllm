# 基于本地大语言模型（LLM）的应用示例

## 通用接口
- `api.py`: 基于 `openai` 标准的通用 API 接口 *helper*
- `system_message.txt`: 系统提示词的可编辑文本

> 下面的示例均会用到上面这些通用模块

## 常用场景示例

### 简单对话
- `llm_chat.py`: 基于本地 LLM 的简单对话机器人

### 基于本地文档的 RAG（*Retrieval Augmented Generation*）
- `rag_create_local_db.py`: 基于本地文档生成 RAG 所需的向量数据库
- `rag_qa.py`: 基于生成好的向量数据库进行问答
- `rag_chat.py`: 基于生成好的向量数据库的对话机器人

### 基于预训练集的 RAG 结合 CoT 与 Self-Reflection
*CoT（Chain-of-Thought prompting）* 及 *Self-Reflection* 都是流行的大模型/智能体方案，*CoT* 侧重引导模型通过一定流程实现更“逻辑性”的思考，这种逻辑流程本身可以借助强化学习（*Reinforcement Learning*）等方式来优化；而 *Reflection* 引导模型对自己生成的内容进行评估，这种评估可以借助 RAG 或其他经过调优（*fine-tuning*）的专用模型。在下面的示例中我们借助预训练的 Wikipedia 向量数据集，通过预先设计的提示词模板，实现最简单的 *CoT+Reflection* 机制。
- `cot_qa.py`: 基于预训练集的 *CoT+Reflection* 问答

## 全新的 Garfield 对话系统
*Garfield* 是计算机科学入门课程 [World of Programming](https://github.com/neolee/wop) 中引导学习者创建的一个可扩展的人机对话系统，现在借助本地大语言模型的力量，可以赋予其更高超的智能。
- `garfield.py`: Garfield 对话系统主程序入口 
- `/garfield`: Garfield 对话系统的对话机器人框架代码
  - `bot.py`：对话机器人（*bots*）的公共父类 `Bot`
  - `/bots`: 派生自 `Bot` 类的各种对话机器人
    - `builtin.py`：原课程中作为示例的一些简单 *bots*
    - `llm.py`：引入本地大语言模型的对话 *bots*，其中 `SimpleLLMBot` 仅提供最简单的交互；而 `LLMBot` 提供与 `openai` 标准 API 兼容的完整功能，可以选择一次性返回与流式返回数据的模式，并提供了对提交请求及返回数据做预处理、后处理的接口，可作为各种附加功能的父类
      - 与上面的 `llm_chat.py` 功能相当，但做了更好的泛化，利于重用
    - `rag.py`：继承自 `LLMBot`、添加了本地文档 *RAG* 的对话机器人
      - 与上面的 `rag_chat.py` 功能相当，但程序结构更优
    - `cot.py`: 继承自 `LLMBot`、添加了 *RAG with CoT+Reflection* 机制的对话机器人
      - 与上面的 `cot_qa.py` 原理类似
