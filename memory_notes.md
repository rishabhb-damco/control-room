# Control Room — Shared Conventions

> Folded in from Claude Code's local memory store on 10 July 2026 so these carry over across machines. These apply across all clients, not just one — client-specific notes live in each client's own `memory_notes.md`.

---

## Report password gate pattern (all clients)

Every HTML report published to GitHub Pages, for any client, must include a full-screen password gate before content loads (uses `sessionStorage` so it's entered once per browser session; Enter key submits).

**Password pattern:** `{ClientName}123`, capital first letter:
- Wellspring → `Wellspring123`
- eSprinto → `ESprinto123`
- Kodacars → `Kodacars123`
- Garuda Aviation → `GarudaAviation123`

**Why:** Prevents data leaks if a report URL is shared or indexed — client data (leads, scheduling rates, spend) is confidential.

**How to apply:** Copy the `#pw-gate` block from an existing reference report exactly (for Wellspring: `wellspring-report-may-10-2026-may-15-2026.html`) — CSS in the main `<style>` block, gate HTML + JS immediately after `<body>`.
