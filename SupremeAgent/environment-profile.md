# Environment Profile

This file describes the host environment's capabilities and constraints. Update it when the environment changes.

The constitution and operating protocol are environment-independent. This file adapts their execution to the available tools and context.

---

## Agent Host

- **Platform**: [IDE name / agent framework / CLI — e.g., Antigravity, Cursor, Cline, custom harness,you]
- **Operating system**: [e.g., Windows, macOS, Linux]

## Capabilities

### File System
- Read files: [YES / NO]
- Write / create files: [YES / NO]
- Delete files: [YES / NO]
- Search / grep: [YES / NO]
- Directory listing: [YES / NO]

### Terminal
- Execute shell commands: [YES / NO]
- Interactive processes: [YES / NO]
- Background tasks: [YES / NO]
- Process management: [YES / NO]

### Version Control
- Git available: [YES / NO]
- Diff review: [YES / NO]
- Branch management: [YES / NO]
- Commit / push: [YES / NO]

### Language Tooling
- Compilers / interpreters: [list available — e.g., node, python, rustc, go]
- Package managers: [list — e.g., npm, pip, cargo]
- Linters / formatters: [list — e.g., eslint, prettier, ruff]
- Test runners: [list — e.g., jest, pytest, cargo test]

### Browser
- Browser automation: [YES / NO]
- Screenshots: [YES / NO]
- Network inspection: [YES / NO]
- Console access: [YES / NO]

### MCP Servers
- [Server name]: [brief capability description]

### External Services
- [Service name]: [access level — read-only / full / limited]

## Sub-Agent Support

- Can spawn sub-agents: [YES / NO]
- Available sub-agent types: [Researcher / Implementer / Debugger / Reviewer]
- Sub-agent model: [same as parent / configurable]

## Limitations

- [Any sandbox restrictions — e.g., no network access, no sudo]
- [Resource constraints — e.g., context window size, max file size]
- [Operational constraints — e.g., cannot install system packages]

---

## Failure Classification Guide

When something fails, classify before attempting a fix:

| Symptom | Likely Category | Correct Response |
|---|---|---|
| Compile / type error after your code change | **CODE** | Fix the code |
| Command not found or dependency missing | **ENVIRONMENT** | Install dependency or fix path |
| Agent tool returns error or timeout | **TOOL** | Retry, check tool status, or use alternative |
| External API returns error or is unreachable | **EXTERNAL** | Verify service status before changing code |
| Cause unclear | **UNKNOWN** | Investigate and classify before acting |

**Critical**: Do not modify working code to fix an environment problem. Do not endlessly retry a tool failure as if it were a code bug. Correctly classifying the failure category is the single most important step in debugging.
