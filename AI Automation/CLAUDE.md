# AI Automation — Claude Code Workspace

> Lead: Rishabh B | Damco Digital
> Initiative started: 20 May 2026
> Last configured: 20 May 2026

---

## What This Is

Internal Damco Digital AI automation initiative. Working group: Rishabh, Gaurav, Edward, Ashish, Harshit.
Goal: identify and automate the most time-consuming repetitive tasks across departments using Claude Code + Claude Routines.

---

## Files in This Folder

| File | Purpose |
|---|---|
| `AI_Automation_Brief.md` | Living brief — initiative overview, members, skills built, roadmap |
| `action_tracker.md` | Open and completed actions + session log |
| `transcripts/` | Meeting transcripts |
| `task_lists/` | Task lists submitted by each team member |
| `skills/` | Notes and specs for skills being built |

---

## Workflow Commands

### "log new skill: [name]"
Add a row to the Weekly Log in `AI_Automation_Brief.md`:
`| [today's date] | [skill name] | [department] | [impact] |`

### "log meeting: [date]"
1. Read the transcript from `transcripts/`
2. Extract: decisions made, action items, next steps
3. Update `AI_Automation_Brief.md` Meeting Log
4. Add new open actions to `action_tracker.md`
5. Ask: "Shall I update the files now?"

### "what's pending?" or "open actions"
Read `action_tracker.md` and list all Open items by priority.

### "initiative status"
Read `AI_Automation_Brief.md` + `action_tracker.md` and return:
```
AI AUTOMATION — STATUS [date]

SKILLS BUILT: [count]
OPEN ACTIONS: [count + top 3]
NEXT DUE: [what + when]
NEXT TARGET: [next skill/automation to build]
```

---

## Session Behaviour

At session start, append to the Session Log in `action_tracker.md`:
`| [today's date] | [user's first request] | In Progress |`
Update to Completed when done.

### Git sync
This folder is its own git repo, synced to GitHub so it's accessible across machines. Only run `git push`/`git pull` when explicitly asked — never proactively sync in the background.
