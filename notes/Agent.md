 # The Agent Loop:

Undertstand the mentor model, exit condition controls the entire flow. Loop will continue runs untill the model stops calling tools.

So how does agent work,
1. Your prompt become the first message.
2. Prompt + Tool is instruction sets to LLM what to do in which step, the workflow being enable.
3. When do we stop, when model stop reason is done with using tool
4. Exe each tool call and save the result, after saving those result, append as user to steps 2


Code example in one function:

```
def agent_loop(query):
    messages = [{"role": "user", "content": query}]
    while True:
        response = client.messages.create(
            model=MODEL, system=SYSTEM, messages=messages,
            tools=TOOLS, max_tokens=8000,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            return

        results = []
        for block in response.content:
            if block.type == "tool_use":
                output = run_bash(block.input["command"])
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                })
        messages.append({"role": "user", "content": results})
```

# Tools

Loop always stay the same, new tools register in to the dispatch map

for example: 
I want a agent that could exe bash commands, read_file, write_files, edit_file

Problem: only  ```bash```, the agent can do anything. That's why we need read_file and write_file
Key note: ***Adding tool does not require any change to the loop we mention prompt --> prompt + tool as an input for workflow --> stop when no more tool is being used --> save result and repeat steps 2***

So what changed now:
1. we now have 4 tools (bash, read, write, edit)
2. Tool heandle dict to handle tool
3. path_safe sandbox
4. agent-loop remain the same

# Sub-Agents:
essentially think of subagents as someone who doesn't share full context but instead Parent would assign insturction that only provids required information to complete it's task. Once the task is done, it will only return the summarised task and result to the parent.

# Skills:

quote: Load knowledge when you need it, not upfront
 only inject via tool_result, not the system prompt

 What is the problem:
 You want agent that follow domain-specific workflows: git, testing, code review. Putting everything in one system prompt is a waste of token. 
 Simple example: 20,000 token each = 20,000 tokens, which not always be used in a given task

 System prompt (Layer 1 -- always present):
+--------------------------------------+
| You are a coding agent.              |
| Skills available:                    |
|   - git: Git workflow helpers        |  ~100 tokens/skill
|   - test: Testing best practices     |
+--------------------------------------+

When model calls load_skill("git"):
+--------------------------------------+
| tool_result (Layer 2 -- on demand):  |
| <skill name="git">                   |
|   Full git workflow instructions...  |  ~2000 tokens
|   Step 1: ...                        |
| </skill>                             |
+--------------------------------------+

# Memory Management:

3 layer context compression

Problem: The context window is limited, you might realise when you are using the same window for gpt for a long time it will stack up a lot of memory or in some way work on large codebase without compression

Every turn:
+------------------+
| Tool call result |
+------------------+
        |
        v
[Layer 1: micro_compact]        (silent, every turn)
  Replace tool_result > 3 turns old
  with "[Previous: used {tool_name}]"
        |
        v
[Check: tokens > 50000?]
   |               |
   no              yes
   |               |
   v               v
continue    [Layer 2: auto_compact]
              Save transcript to .transcripts/
              LLM summarizes conversation.
              Replace all messages with [summary].
                    |
                    v
            [Layer 3: compact tool]
              Model calls compact explicitly.
              Same summarization as auto_compact.

So the solution:
1. Micro_compact: before each LLM, replace old tool results with placeholder

# Tasks
.tasks/
  task_1.json  {"id":1, "status":"completed"}
  task_2.json  {"id":2, "blockedBy":[1], "status":"pending"}
  task_3.json  {"id":3, "blockedBy":[1], "status":"pending"}
  task_4.json  {"id":4, "blockedBy":[2,3], "status":"pending"}

Task graph (DAG):
                 +----------+
            +--> | task 2   | --+
            |    | pending  |   |
+----------+     +----------+    +--> +----------+
| task 1   |                          | task 4   |
| completed| --> +----------+    +--> | blocked  |
+----------+     | task 3   | --+     +----------+
                 | pending  |
                 +----------+

Ordering:     task 1 must finish before 2 and 3
Parallelism:  tasks 2 and 3 can run at the same time
Dependencies: task 4 waits for both 2 and 3
Status:       pending -> in_progress -> completed