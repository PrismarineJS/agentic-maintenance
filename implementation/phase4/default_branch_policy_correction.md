# CI merge-policy correction

Date: 2026-10-07. Prepared and applied by the Astra agent following rom1504's
"Ok fix it" instruction, followed by explicit "Yes go" approval for the remaining
92 repositories. [Machine-readable receipts](default_branch_policy_correction.json).

## Applied scope

Set `strict_required_status_checks_policy: false` in **all 94 managed CI
rulesets**: first node-nethernet and bedrock-protocol, then the remaining 92
following explicit approval. Per-write readback confirmed that this was the only
ruleset field changed. **35 remain active and 59 remain disabled**. Required `ci` remains
bound to GitHub Actions (app 15368), with no bypass. The PR requirement, admin
approval exception, and history protections remain intact.

The default policy now specifies this loose required-check behavior. A passing
required check is still necessary, but newer base commits do not alone require
a branch update and another test run. Maintainers should request integration
updates when changes overlap or need testing together.

## Existing PR transition

Updated the two affected PR branches through GitHub's update-branch API, guarded
by their expected head SHAs. These merge updates bring in the newly added CI
aggregate workflow. No default branch was pushed directly and neither PR was
merged. Existing runs using the old workflow could not produce `ci`.

| PR | Previous head | Updated head | Validation |
|---|---|---|---|
| [node-nethernet #32](https://github.com/PrismarineJS/node-nethernet/pull/32) | `77a0b38e92e140a75d96ad540794380dfef1af85` | `c46db7da4f0e97ec04487648f5759e3f23ff8e9c` | All three OS jobs and `ci` passed. Windows initially timed out in `preserves optional discovery metadata and empty responses` (75 passing, 1 failing); one failed-job retry passed. The gate correctly failed the first attempt. |
| [bedrock-protocol #831](https://github.com/PrismarineJS/bedrock-protocol/pull/831) | `d2973e71bc9c0130450035d1f19919f619d4fd86` | `b4160368b7e5272ccdd435f75459220c167fe4e4` | Linux, Windows, and the required `ci` gate all passed. |

[Nethernet run](https://github.com/PrismarineJS/node-nethernet/actions/runs/37599215778).
[Bedrock run](https://github.com/PrismarineJS/bedrock-protocol/actions/runs/37599222323).

## Completed scope and exact applied diff

Automatic approval review initially rejected applying this setting across all
94 public, unarchived repositories because it judged "Ok fix it" insufficiently
explicit for that scope. After the two directly affected repositories were
fixed, rom1504 explicitly approved the remaining 92 with "Yes go". All 92 changes
were then applied with fresh backups and individual readback verification.

The only change to each managed `pjs-ci-and-history` ruleset was:

```diff
- "strict_required_status_checks_policy": true
+ "strict_required_status_checks_policy": false
```

Each ruleset's active/disabled state, required GitHub Actions check, bypass
configuration, and history rules were preserved. The separate review rulesets
and all unrelated/classic protections were left unchanged. This allows passing
CI to predate newer base changes, with the corresponding interaction risk.

Three pre-existing classic protections still require up-to-date branches:
**prismarinejs.github.io**, **flying-squid**, and **prismarine-web-client**. They
were deliberately preserved under the approved scope. Their managed CI rulesets
remain disabled; removing these classic requirements would be a separate change.

## Verification

All 16 offline policy/audit/gate tests passed again after the completed rollout. The final live audit
and per-repository receipt comparison verify all 94 managed CI rulesets have
strictness disabled, with 35 active and 59 disabled. The 94 PR/review rulesets
still match the policy, including the admin PR-only approval exception.
Before/after comparison also verifies unchanged classic protections and all
other ruleset parameters.

The inventory contains 94 included, 3 archived, and 1 private repository.
The auditor reports one classic-protection read as unknown on bedrock-protocol:
GitHub returned HTTP 404 with "Branch protection has been disabled on this
repository." This same response occurred before and after; the audit conservatively
retains it as a read error. Its rulesets and effective branch rules were read
successfully. No classic protection was changed.

[Final settings snapshot](default_branch_policy_correction_after.json) and
[readable audit](default_branch_policy_correction_after.md) record this state.
The previous rollout and after-snapshot files remain historical evidence.
Existing unrelated local phase2 drafts were not included in this change.
