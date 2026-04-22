# disciplina

A Claude Code skill containing behavioral guidelines for disciplined LLM coding, derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on common LLM coding pitfalls.

The four principles:

1. **Think before coding** — surface assumptions, ask when unclear
2. **Simplicity first** — minimum code that solves the problem
3. **Surgical changes** — every changed line traces to the user's request
4. **Goal-driven execution** — turn vague asks into verifiable goals

See `SKILL.md` for the full text, worked examples, and rationale.

## Install

Using the [`skills` CLI](https://skills.sh) (recommended):

```bash
npx skills add naiplawan/disciplina
```

Or install manually by copying into your Claude Code skills path:

```bash
# User-level (applies across all projects)
cp -r disciplina ~/.claude/skills/

# Or project-level
cp -r disciplina /path/to/project/.claude/skills/
```

Claude Code will pick up the skill on next session start.

## Invoking

You can ask Claude to use it explicitly:

```
/disciplina review this refactor
```

## Important caveat — behavioral skills don't reliably auto-trigger

This skill was empirically tested against 20 realistic trigger queries (10 should-trigger + 10 should-not-trigger), each fired 3× through Claude Code.

Result: **0 out of 30 should-trigger runs actually activated the skill.**

This is not a description-quality issue — it's how Claude's skill-consult heuristic works. Claude only consults skills for tasks it perceives itself as unable to handle (specialized APIs, specific frameworks, exotic formats). It sees "fix this bug" or "refactor this function" and concludes *"I know how to code, I don't need a skill for that"* — missing the point that this skill is about *how* to code, not *whether* it can.

### Recommended pattern: route behavioral guidance through CLAUDE.md

Instead of relying on auto-trigger, put the compressed version of these principles into your always-loaded `CLAUDE.md` (global at `~/.claude/CLAUDE.md`, or per-project at `<repo>/CLAUDE.md`). Example section — copy into your CLAUDE.md:

```markdown
## Writing and Editing Code

- Before implementing, state assumptions explicitly; if the request has multiple reasonable interpretations, list them and ask rather than pick silently
- Write the minimum code that solves the stated problem — no abstractions for single-use code, no options the user didn't request, no error handling for scenarios that can't actually happen
- Keep changes surgical: every changed line should trace directly to the user's request. If you notice adjacent dead code, style inconsistency, or drive-by improvements, mention them in your reply — don't clean them up uninvited
- Turn vague goals into verifiable ones before touching code: "fix the bug" → "write a test that reproduces it, then make it pass"; "refactor X" → "ensure tests pass before and after". State a reproduce/verify step for each subtask before starting
```

Keep `SKILL.md` installed as a fallback for explicit invocation (when you want the worked example for §3 or the full framing).

## Evaluation methodology

The `evals/evals.json` file contains four behavioral test cases used during skill development (iteration 1):

1. **Ambiguous validation** — targets §1 "Think before coding"
2. **Overengineer date formatter** — targets §2 "Simplicity first"
3. **Surgical bugfix** — targets §3 "Surgical changes" (the clearest-win scenario)
4. **Vague flaky tests** — targets §4 "Goal-driven execution"

Each test was run with and without the skill. Eval 3 showed the clearest behavioral difference: with-skill made exactly a 1-character fix and flagged unrelated smells as "noted but not changed"; baseline snuck in an unrequested variable rename.

See the original project workspace for side-by-side output comparisons.

## License

MIT — see `LICENSE`.

## Credit

Principles derived from [Andrej Karpathy](https://x.com/karpathy/status/2015883857489522876). Packaged by [@rachaphol](https://github.com/rachaphol).
