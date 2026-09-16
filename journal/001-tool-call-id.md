# 001 - Tool observation 缺少 tool_call_id

## 场景

这是 Personal Agent 第一次真实尝试完整的 ReAct Tool Call 闭环：

```text
User → LLM → read tool call → tool observation → LLM → Final
```

真实 API 调用通过 `src/main.py` 正常入口发起。

## 现象

第一轮 LLM 成功返回了 `read` 工具调用请求。工具结果写回模型后，第二轮 API 请求失败：

```text
400 BadRequestError:
messages[3]: missing field `tool_call_id`
```

本次没有泄露 API Key，也没有读取 `secret/`。

## 原因

当前 `react.py` 在写回 tool observation 时，没有携带 OpenAI-compatible Tool Calling protocol 所要求的 `tool_call_id`。

因此第二轮请求中，API 无法判断当前 tool result 对应前面哪一次 tool call。

## 关键理解

Tool Calling 不只是：

```text
tool name
arguments
result
```

而是存在一次工具调用的身份关联：

```text
assistant tool call
├── id
├── name
└── arguments

tool result
├── tool_call_id
└── content
```

返回 tool result 时，`tool_call_id` 必须对应前面 assistant tool call 的 `id`。

## 下一步

需要检查并最小修改：

```text
src/llm/client.py
src/agent/react.py
```

确保：

1. LLM client 在统一 `tool_call` response 中保留 `tool_call_id`。
2. ReAct 在执行工具后，将同一个 ID 写入 `role="tool"` message。
3. 再把完整 messages 发回模型。
