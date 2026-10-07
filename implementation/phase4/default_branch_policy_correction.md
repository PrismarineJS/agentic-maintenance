# CI merge-policy correction

Date: 2026-10-07. Prepared and applied by the Astra agent following rom1504's
"Ok fix it" instruction. [Machine-readable receipts and remaining diff](default_branch_policy_correction.json).

## Applied scope

Removed `strict_required_status_checks_policy` from the active CI rulesets in
**node-nethernet** and **bedrock-protocol** by setting it to `false`. Readback
confirmed that this was the only ruleset field changed. Required `ci` remains
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
| [node-nethernet #32](https://github.com/PrismarineJS/node-nethernet/pull/32) | `77a0b38e92e140a75d96ad540794380dfef1af85` | `c46db7da4f0e97ec04487648f5759e3f23ff8e9c` | Linux/macOS passed; Windows failed with a timeout in `preserves optional discovery metadata and empty responses` (75 passing, 1 failing). The new gate correctly failed. One failed-job retry requested. |
| [bedrock-protocol #831](https://github.com/PrismarineJS/bedrock-protocol/pull/831) | `d2973e71bc9c0130450035d1f19919f619d4fd86` | `b4160368b7e5272ccdd435f75459220c167fe4e4` | New pull-request CI running on Linux and Windows. |

[Nethernet run](https://github.com/PrismarineJS/node-nethernet/actions/runs/37599215778).
[Bedrock run](https://github.com/PrismarineJS/bedrock-protocol/actions/runs/37599222323).

## Remaining scope and exact proposed diff

Automatic approval review rejected applying this setting across all 94 public,
unarchived repositories: it judged the broad persistent relaxation insufficiently
explicitly authorized by "Ok fix it". The two directly affected repositories were
subsequently accepted as a narrower fix. The other **92 were not modified**.
Their complete proposed per-repository diff is included in the JSON receipts.

For each remaining managed `pjs-ci-and-history` ruleset, change only:

```diff
- "strict_required_status_checks_policy": true
+ "strict_required_status_checks_policy": false
```

Preserve each ruleset's active/disabled state (33 active, 59 disabled among those
92), all other parameters, and unrelated/classic protections. The intended
policy file is not a claim of uniform live deployment. Applying the remaining
diff requires explicit user confirmation. This allows passing CI to predate
newer base changes, with the corresponding interaction risk.

## Verification

All 16 offline policy/audit/gate tests passed. Before mutation, the organization
inventory contained 94 included, 3 archived, and 1 private repository. One
classic-protection read on bedrock-protocol failed in that inventory; no classic
protection was changed. Each changed ruleset was fetched immediately before the
write, backed up, and read back afterward. Effective rules and the admin PR-only
review bypass were also fetched for the two changed repositories.

The previous rollout and after-snapshot files remain historical evidence.
Existing unrelated local phase2 drafts were not included in this change.
