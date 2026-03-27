# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

An educational framework (`learn-claude-code/`) teaching harness engineering for AI agents through 12 progressive sessions. The central thesis: **the model IS the agent; the code is the harness** (tools + knowledge + observation + action interfaces + permissions).

Supporting projects:
- `ai-agent-skills-migration/` — skill migration work (git repo)
- `outlook-api-1.0.3/` — standalone Outlook skill module
- `notes/` — personal research notes

---

## learn-claude-code

### Setup

```bash
cd learn-claude-code
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add ANTHROPIC_API_KEY
```

### Running Agents

```bash
python agents/s01_agent_loop.py       # minimal loop (~100 lines)
python agents/s12_worktree_task_isolation.py  # full multi-agent system
python agents/s_full.py               # capstone: all mechanisms combined
```

### Web Platform

```bash
cd web
npm install
npm run extract   # pre-build content extraction from agents/
npm run dev       # http://localhost:3000
npm run build     # production build (runs tsc --noEmit then next build)
```

CI runs `npm ci && npx tsc --noEmit && npm run build`.

---

## Agent Architecture

### The Core Loop (all sessions build on this)

```python
def agent_loop(messages):
    while True:
        response = client.messages.create(
            model=MODEL, system=SYSTEM,
            messages=messages, tools=TOOLS,
        )
        messages.append({"role": "assistant", "content": response.content})
        if response.stop_reason != "tool_use":
            return
        results = []
        for block in response.content:
            if block.type == "tool_use":
                output = TOOL_HANDLERS[block.name](**block.input)
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": output})
        messages.append({"role": "user", "content": results})
```

### Session Progression

| Session | Key Mechanism |
|---------|--------------|
| s01 | Agent loop — one loop & Bash is all you need |
| s02 | Tool dispatch — adding a tool means adding one handler |
| s03 | TodoWrite — agents without plans drift |
| s04 | Subagents — child agents with clean context |
| s05 | Skill loading — load knowledge on demand, not upfront |
| s06 | Context compaction — 3-layer memory compression |
| s07 | Task system — persistent task DAG on disk |
| s08 | Background tasks — daemon threads + notifications |
| s09 | Agent teams — persistent teammates + async mailboxes |
| s10 | Team protocols — structured request-response handshakes |
| s11 | Autonomous agents — idle cycle + auto-claiming tasks |
| s12 | Worktree isolation — each agent works in its own directory |

### Runtime Artifacts (generated, not committed)

- `.tasks/task_*.json` — persistent task state with dependency graphs
- `.teams/` — teammate config, inbox JSONL, status tracking
- `.transcripts/` — compressed conversation histories
- `.task_outputs/` — task execution outputs

---

## Web Platform Architecture

**Stack**: Next.js + React 19 + TypeScript + Tailwind CSS 4

**Routing**: `web/src/app/[locale]/(learn)/`
- `[version]/page.tsx` — agent source viewer
- `[version]/diff/` — diff viewer between sessions
- `compare/page.tsx` — cross-session comparison
- `timeline/page.tsx` — learning timeline
- `layers/page.tsx` — architecture layer diagrams

**Content pipeline**: `web/scripts/extract-content.ts` runs at build time to extract agent source content into static data consumed by the Next.js pages. Run `npm run extract` before `npm run dev` if agent files have changed.

Supports three locales: `en`, `zh`, `ja`.

---

## Environment Variables

| Variable | Required | Notes |
|----------|----------|-------|
| `ANTHROPIC_API_KEY` | Yes | `sk-ant-xxx` |
| `MODEL_ID` | No | Default: `claude-sonnet-4-6` |
| `ANTHROPIC_BASE_URL` | No | For compatible providers (MiniMax, DeepSeek, etc.) |
| `MATON_API_KEY` | For Outlook skill | Used by `outlook-api-1.0.3/` |
