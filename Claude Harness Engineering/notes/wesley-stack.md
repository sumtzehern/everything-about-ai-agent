When a parent agent spawns a subagent via the Task tool, the subagent starts with a clean message history containing only the system prompt and the delegated task description. It does NOT inherit the parent's conversation. This is context isolation: the subagent can focus entirely on its specific subtask without being distracted by hundreds of messages from the parent's broader conversation. The result is returned to the parent as a single tool_result, collapsing potentially dozens of subagent turns into one concise answer.

When spawning a subagent with the 'Explore' type, it receives only read-only tools: bash (with restrictions), read_file, and search tools. It cannot call write_file or edit_file. This implements the principle of least privilege: an agent tasked with 'find all usages of function X' doesn't need write access. Removing write tools eliminates the risk of accidental file modification during exploration, and it also narrows the tool space so the model makes better decisions with fewer options.

The Task tool is not included in the subagent's tool set. A subagent must complete its work directly -- it cannot delegate further. This prevents infinite delegation loops: without this constraint, an agent could spawn a subagent that spawns another subagent, each one re-delegating the same task in slightly different words, consuming tokens without making progress. One level of delegation handles the vast majority of use cases. If a task is too complex for a single subagent, the parent should decompose it differently.

Skills wise:
- /commit: create git commis following repo conventions
- /review-pr - Review pull requet for bugs and style
- /test - Run and analyze test suites
- /deploy - Deploy application to target env


/commit:
1. Run git status + git diff to see changes
2. Analyze all staged changes and draft message
3. Create commit with Co-Authored-By trailer
4. Run git status after commit to verify

/review-pr:
1. Fetch PR diff via gh pr view
2. Analyze changes file by file for issues
3. Check for bugs, security, and style problems
4. Post review comments with gh pr review


How to build an agent:
## 🤖 Agent Builder — Key Takeaways

### The Core Philosophy
> **The model already knows how to be an agent. Your job is to get out of the way.**

An agent is a simple loop:
```
LOOP:
  Model sees: context + available capabilities
  Model decides: act or respond
  If act: execute capability, add result, continue
  If respond: return to user
```

---

### The Three Elements
1. **Capabilities** — What it can *do* (search, read, create, send, query). Start with **3–5 only**.
2. **Knowledge** — Domain expertise loaded *on-demand*, not upfront.
3. **Context** — The conversation history. Keep it clean and protect its clarity.

---

### Progressive Complexity
| Level | What to Add | When |
|-------|-------------|------|
| Basic | 3–5 capabilities | Always start here |
| Planning | Progress tracking | Multi-step tasks lose coherence |
| Subagents | Isolated child agents | Exploration pollutes context |
| Skills | On-demand knowledge | Domain expertise needed |

> **Most agents never need to go beyond Level 2.**

---

### Key Anti-Patterns to Avoid
- ❌ Over-engineering before there's a need
- ❌ Too many capabilities (causes model confusion)
- ❌ Rigid pre-specified workflows
- ❌ Front-loading knowledge (bloats context)
- ❌ Micromanaging the model

---

### Available References
- `references/agent-philosophy.md` — Deep dive into why agents work
- `references/minimal-agent.py` — Complete working agent (~80 lines)
- `references/tool-templates.py` — Capability definitions
- `references/subagent-pattern.py` — Context isolation
- `scripts/init_agent.py` — Generate new agent projects

---

Would you like to **build an agent**? If so, tell me:
1. **What's its purpose?**
2. **What domain does it operate in?**
3. **What 3–5 actions should it be able to perform?**


compress strategy:
Context management uses three distinct layers, each with different cost/benefit profiles. (1) Microcompact runs every turn and is nearly free: it truncates tool_result blocks from older messages, stripping verbose command output that's no longer needed. (2) Auto_compact triggers when token count exceeds a threshold: it calls the LLM to generate a conversation summary, which is expensive but dramatically reduces context size. (3) Manual compact is user-triggered for explicit 'start fresh' moments. Layering these means the cheap operation runs constantly (keeping context tidy) while the expensive operation runs rarely (only when actually needed).

Auto_compact only triggers when the estimated savings (current tokens minus estimated summary size) exceed 20,000 tokens. Compression is not free: the summary itself consumes tokens, plus there's the API call cost to generate it. If the conversation is only 25,000 tokens, compressing might save 5,000 tokens but cost an API call and produce a summary that's less coherent than the original. The 20K threshold ensures compression only happens when the savings meaningfully exceed the overhead.


When auto_compact fires, it generates a summary and replaces the ENTIRE message history with that summary. It does not keep the last N messages alongside the summary. This avoids a subtle coherence problem: if you keep recent messages plus a summary of older ones, the model sees two representations of overlapping content. The summary might say 'we decided to use approach X' while a recent message still shows the deliberation process, creating contradictory signals. A clean summary is a single coherent narrative.

