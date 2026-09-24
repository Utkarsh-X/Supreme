---
name: supreme
description: The complete five-document engineering framework for coding agents. Use when implementing, debugging, reviewing, refactoring, or auditing software repositories; load and apply every Supreme guidance document before acting.
license: MIT
compatibility: Any coding agent that supports the Agent Skills format and can read bundled Markdown reference files.
---

# Supreme — Agent Skill Entry Point

This file is the required entry point to the complete Supreme framework. It is a loader, not a replacement for the five guidance documents. Do not summarize, omit, or substitute their contents.

## Mandatory load protocol

On every invocation of Supreme, and **before taking task action**, open and read the complete contents of all five files below. Read every file even when the task appears to concern only one area. Apply the documents together as one framework.

1. [Engineering constitution](references/constitution.md)
2. [Operating protocol](references/operating-protocol.md)
3. [Specialist sub-agent profiles](references/sub-agent-profiles.md)
4. [Environment profile](references/environment-profile.md)
5. [Persistent state](references/persistent-state.md)

Read each file once in the listed order. This is the complete load sequence; do not follow navigation links during loading or loop back to previously read files. If a file is missing, inaccessible, or truncated, stop and identify the exact problem instead of proceeding with a partial version. Reopen a document during the task only if new evidence creates a specific need.

The framework is guidance, not a runtime enforcement mechanism. Follow the host's actual tool and permission model while applying all five documents.