# Claude Agents & Skills Orchestration Guide

## Overview

This directory contains **agents** (specialized AI assistants) and **skills** (reusable capabilities) that work together to scrape, analyze, and report on web content using Playwright automation.

## Directory Structure

read the directory structure,

Agents define WHO does the work (specialized agents with specific permissions)
Skills define HOW to do the work (portable expertise any agent can use)


## How to Use Agents

### 1. Understanding Agents

Agents are specialized AI assistants defined in `.claude/agents/*.md` files. Each agent:
- Has a specific purpose (e.g., scraping business news)
- Uses Playwright MCP servers for browser automation
- Follows a structured workflow
- Outputs to organized directories

### 2. Invoking an Agent

To use an agent, reference it with `@` prefix:

```
@business_news_scraper.md - Scrape WSJ, Business Insider, Forbes
```

### 3. Agent Workflow Pattern

Most scraping agents follow this pattern:

1. **Navigate** to target URLs using Playwright MCP
2. **Screenshot** pages using `webpage-screenshotter` skill
3. **Analyze** screenshots visually using Read tool
4. **Extract** data from what's visible
5. **Save** outputs to organized directories

## How to Use Skills

### 1. Understanding Skills

Skills are reusable capabilities defined in `.claude/skills/*/SKILL.md`. They provide:
- Code implementations
- Best practices
- Usage examples
- Configuration guidelines


## Output Organization

All outputs follow this structure:

```
outputs/
└── <agent_name>/
    └── <customer_name>/
        ├── reports/        # Final markdown reports
        ├── scripts/         # Generated scraping code
        ├── raw/            # JSON/CSV data files
        └── screenshots/    # PNG screenshots
```

