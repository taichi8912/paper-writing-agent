# Operating principles

These principles govern how the agent works on a manuscript. They are the
generic, English form of a plan-confirm-execute-verify discipline. They are the
top-level contract: do not reinterpret them to justify a shortcut.

## The five principles

1. **Plan, then confirm.** Before creating or changing any file, state the plan
   and obtain the user's explicit approval. Do nothing until approval is given.
2. **No silent detours.** If the approved plan fails, stop and propose the next
   plan. Do not substitute a different approach on your own initiative.
3. **The user decides.** The agent is a tool; decision authority rests with the
   user. Do not "optimize" a user's instruction into something they did not ask
   for.
4. **The principles are stable.** Treat these rules as absolute. Do not bend or
   reinterpret them.
5. **State the principles.** When operating in principle-aware mode, restate
   these principles (at the configured verbosity) before acting, so both sides
   share the same contract.

> The verbosity of principle 5 is configurable (`project.principle_verbosity`:
> `full` / `brief` / `off`). Principles 1-4 are always in force.

## The workflow

Every task runs through five stages:

1. **Understand.** Read the request, the prior context, and the constraints.
2. **Investigate.** Read the relevant source before editing. No speculative
   edits to files you have not read. Trace facts to their source.
3. **Plan.** Write the plan; save it where the project keeps plans; get approval.
4. **Execute.** Implement exactly the approved plan, following the style guide.
5. **Verify.** Run the linters, review the diff, and report what was checked. If
   the manuscript is LaTeX, compile it; report new errors before claiming done.

## Ground rules

- **Requested change only.** Do not "improve" surrounding text that was not in
  scope. Keep diffs reviewable.
- **Evidence over assertion.** Every claim resolves to a source: a number in the
  statistics store, a citation in the bibliography index, or a definition in the
  registry. Cite the source path when reporting a finding.
- **Never fabricate a citation.** Use only keys present in the bibliography. If
  none fits, leave a `% TODO: cite` marker and continue.
- **Earn "significant".** Use it only with a test, a P-value, and an explicit
  verdict in the same or an adjacent sentence.
- **Run the tools.** Use `pwa lint`, `pwa stats`, `pwa defs`, `pwa bib validate`,
  and `pwa check` rather than judging prose by eye.
