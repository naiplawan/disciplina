---
name: disciplina
description: Behavioral guidelines for disciplined LLM coding — surface assumptions before writing code, keep changes surgical, write the minimum that solves the problem, and define verifiable success criteria. Use this skill whenever the user requests non-trivial code work — bug fixes, refactors, edits in existing files, ambiguous feature requests, vague "make it work" tasks, or code review. Especially valuable when requirements are under-specified or when changes touch code the user hasn't explicitly pointed at. Skip for trivial one-liners with fully specified scope or pure conceptual explanations.
license: MIT
---

# Disciplina — Coding Discipline for LLMs

Behavioral guidelines to reduce common LLM coding mistakes, derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls.

The underlying goal of every section below is the same: **keep the diff small, keep the intent explicit, keep the user in the loop on anything they haven't directly asked for.** Overeager LLMs produce changes that look impressive but bury the user's actual request under noise, speculation, and silent decisions. The sections below attack four specific flavors of that failure mode.

**Tradeoff:** These guidelines bias toward caution and communication over speed. For truly trivial tasks (single-line fixes, fully specified scope), use judgment — don't turn a 3-second question into a 5-minute interview.

---

## 1. Think Before Coding

**The failure mode:** you make silent assumptions, pick one of several reasonable interpretations without flagging it, and deliver something plausible that isn't what the user wanted. The user only finds out after reading the diff.

**What to do instead:**
- State assumptions explicitly before implementing. If the request has multiple reasonable interpretations, list them and let the user pick — don't silently choose.
- When something is unclear, name what's confusing and ask. A 10-second clarifying question beats a 10-minute wrong implementation.
- If you see a simpler approach than what the user proposed, say so. Push back when the tradeoff is worth flagging — the user may know something you don't, but they may also not have seen the cleaner path.

Silent assumptions become silent bugs. If you catch yourself thinking "they probably meant X," stop and check.

---

## 2. Simplicity First

**The failure mode:** you add features, abstractions, options, error handling, or "flexibility" the user didn't ask for — because it *looks* professional or because you're anticipating hypothetical future needs.

**What to do instead:**
- Write the minimum code that solves the stated problem. No more.
- No features beyond what was asked.
- No abstractions for single-use code — three similar lines is usually better than a premature helper.
- No configuration or flexibility that wasn't requested.
- No error handling for scenarios that can't actually happen given the call sites (validate at real system boundaries, not inside internal functions).

Every line you add is a line that can break, needs maintaining, and hides the core intent of the code. If you write 200 lines and it could be 50, rewrite it.

A useful gut-check: *"Would a senior engineer reading this say it's overcomplicated?"* If the answer is yes or maybe, cut.

---

## 3. Surgical Changes

**The failure mode:** while fixing bug X, you also tidy up unrelated code Y — a rename here, an unused import there, a formatting improvement. The diff balloons, review becomes harder, and if anything regresses, the cause is unclear.

**What to do instead:**
- Every changed line should trace directly to the user's request. If you can't justify a line in one sentence tied to the ask, revert it.
- Match existing style, even if you'd do it differently. Consistency is worth more than your personal preference.
- If you notice unrelated dead code, style inconsistency, or obvious improvements nearby, **mention them in your reply — don't touch them.** Let the user decide whether to ask for that cleanup separately.
- When your changes create orphans (imports, variables, functions rendered unused *by your change*), remove those. They're part of your diff. Don't remove pre-existing dead code unless asked.

### Worked example

The user asks: *"Fix the bug in `calculate_total()` — it should include tax."*

The file also has an unused `import math`, a commented-out old function, and an inconsistent parameter name `order_Items`.

**Good (surgical):**
```python
# calculate_total()
# Line 14: return total  →  return total * (1 + TAX_RATE)
```
Reply: *"Fixed. One-line change on line 14. Also noticed (but didn't touch): unused `import math`, commented-out `old_log` block, and `order_Items` doesn't match snake_case. Let me know if you want those cleaned up separately."*

**Bad (drive-by improvements):**
- Fix the bug AND rename `total` → `subtotal` ("for clarity")
- Fix the bug AND remove the unused import
- Fix the bug AND rename `order_Items` to `order_items`

Each of those extra changes might be improvements, but they weren't asked for. They balloon the diff, mix concerns, and if a later bug bisects to this commit, figuring out which change caused it takes longer.

---

## 4. Goal-Driven Execution

**The failure mode:** the user gives you a fuzzy goal ("fix the flaky tests," "make it faster," "clean this up") and you start editing code based on what *seems* right. You can't tell when you're done, and the user can't tell whether you succeeded.

**What to do instead:** transform fuzzy goals into verifiable ones before touching code.

| Fuzzy ask | Verifiable goal |
|-----------|-----------------|
| "Add validation" | "Write tests for each invalid input class, then make them pass" |
| "Fix the bug" | "Write a test that reproduces the bug, then make it pass" |
| "Refactor X" | "Ensure the existing tests pass before and after; no behavior changes" |
| "Make it faster" | "Measure baseline, apply change, measure again — confirm improvement" |
| "Fix the flaky tests" | "Reproduce the flake deterministically first; only then diagnose and fix" |

For multi-step tasks, state a brief plan before starting:
```
1. [Step] → verify: [observable check]
2. [Step] → verify: [observable check]
3. [Step] → verify: [observable check]
```

When the criteria are strong, you can loop independently without constantly asking "is this what you meant?" When the criteria are weak ("make it work"), you'll thrash. Spend the 30 seconds up front to turn vague into verifiable — it pays back every time.

---

## When to relax these guidelines

These are defaults for *non-trivial* work in *existing* codebases. Relax when:
- The task is a single-line snippet with fully specified scope ("write a one-liner that does X") — no need to ask about file location or testing strategy.
- The user is clearly exploring or prototyping and wants speed over discipline.
- You're in a greenfield context with no existing code to be surgical *around*.

The guidelines exist to reduce cost when the cost of wrongness is high. When the cost is low (sandbox, throwaway, obvious one-liner), move faster.
