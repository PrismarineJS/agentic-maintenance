# mineflayer — Open PR Status & Triage

- **Date:** 2026-05-23
- **Repo:** [PrismarineJS/mineflayer](https://github.com/PrismarineJS/mineflayer)
- **Source:** GitHub API via `gh pr list` (open PRs), including CI
  `statusCheckRollup`, mergeability, comments, changed files, and diff size.
- **Open PRs at snapshot:** 33

## Purpose

A categorized snapshot of every open mineflayer PR so we can decide where to
spend maintenance effort: what's ready to merge, what's a quick unblock, what
needs real work, and what's stale.

## How to read this

- **CI:** ✅ pass · ❌ fail · ⚪ no checks ran
- **🧪** = the PR adds/touches test files
- **💬N** = number of distinct people who commented
- **⚠️** = has a merge conflict
- **Size** = total lines changed (add + del): XS `<10` · S `<50` · M `<300` ·
  L `<800` · XL `800+`

> **Caveat on flaky tests:** mineflayer's `MinecraftServer` integration tests
> are known to be flaky. A trivial or docs-only PR that fails a *single* version
> job is almost certainly a flake, not a real regression — re-running CI will
> usually clear it.

---

## ✅ Green — CI passing, ready to review/merge (9)

| PR | Title | Size | Tests | Comments | Notes |
|----|-------|------|-------|----------|-------|
| [3902](https://github.com/PrismarineJS/mineflayer/pull/3902) | Update Mineflayer for Minecraft 26.1.2 | 283 (M) | 🧪 | 💬2 | The real MC version bump |
| [3852](https://github.com/PrismarineJS/mineflayer/pull/3852) | Auto-detect activateBlock face from bot pos | 160 (M) | 🧪 | — | |
| [3730](https://github.com/PrismarineJS/mineflayer/pull/3730) | Fix block visibility via canSeeBlock | 57 (M) | — | 💬1 | |
| [3890](https://github.com/PrismarineJS/mineflayer/pull/3890) | Add dynamic tick interval support | 46 (S) | — | — | |
| [3737](https://github.com/PrismarineJS/mineflayer/pull/3737) | Demonstrate prismarine-world entity storage | 34 (S) | — | 💬1 | by rom1504 |
| [3901](https://github.com/PrismarineJS/mineflayer/pull/3901) | Add look2 / getNotchYawPitch methods | 23 (S) | — | 💬2 | no tests added |
| [3900](https://github.com/PrismarineJS/mineflayer/pull/3900) | Add crafting util to readme | 50 (S) | 🧪 | — | mostly docs |
| [3842](https://github.com/PrismarineJS/mineflayer/pull/3842) | Fix resource pack UUID serialization | 127 (M) | 🧪 | 💬4 | ⚠️ conflict, but CI green |
| [3841](https://github.com/PrismarineJS/mineflayer/pull/3841) | Merge updates to current upstream | 1826 (XL) | 🧪 | 💬3 | **Draft** — large |

## 🟡 Lint-only failure — otherwise fine, trivial unblock (2)

| PR | Title | Size | Tests | Comments |
|----|-------|------|-------|----------|
| [3778](https://github.com/PrismarineJS/mineflayer/pull/3778) | Add cartography table use | 131 (M) | — | 💬1 |
| [3885](https://github.com/PrismarineJS/mineflayer/pull/3885) | Update Simplified Chinese docs translation | 2514 (XL) | — | 💬1 |

## ❌ Real test failures — needs work (10)

| PR | Title | Size | Tests | Comments | Failing |
|----|-------|------|-------|----------|---------|
| [3891](https://github.com/PrismarineJS/mineflayer/pull/3891) | Look sync fix | 43 (S) | 🧪 | 💬3 | 2 version groups |
| [3879](https://github.com/PrismarineJS/mineflayer/pull/3879) | Update Mineflayer for 26.1 | 359 (L) | 🧪 | — | all versions |
| [3786](https://github.com/PrismarineJS/mineflayer/pull/3786) | Velocity proxy support 1.20.2+ | 318 (L) | — | 💬3 | Lint + many |
| [3834](https://github.com/PrismarineJS/mineflayer/pull/3834) | Add Velocity proxy (config phase) | 290 (M) | — | 💬4 | 1 version |
| [3826](https://github.com/PrismarineJS/mineflayer/pull/3826) | Add cartography table plugin | 270 (M) | 🧪 | 💬2 | many versions |
| [3677](https://github.com/PrismarineJS/mineflayer/pull/3677) | Fix editBook invalid packet 1.13+ | 163 (M) | 🧪 | 💬1 | 3 version groups |
| [3881](https://github.com/PrismarineJS/mineflayer/pull/3881) | Fixed buckets (rebased #3740) | 128 (M) | 🧪 | — | 1 version group |
| [3794](https://github.com/PrismarineJS/mineflayer/pull/3794) | Send client brand in config state | 18 (S) | — | 💬2 | Lint + 1 |
| [3673](https://github.com/PrismarineJS/mineflayer/pull/3673) | Support placing item frames | 20 (S) | 🧪 | 💬1 | many versions |
| [3883](https://github.com/PrismarineJS/mineflayer/pull/3883) | Fix physics lock-up in 1.21.4 | 7 (XS) | — | 💬2 | Lint + 1 |

## ⚠️ Likely flaky — tiny/docs PRs failing 1–3 version jobs (5)

| PR | Title | Size | Failing | Notes |
|----|-------|------|---------|-------|
| [3853](https://github.com/PrismarineJS/mineflayer/pull/3853) | Add project to "Projects Using Mineflayer" | 1 (XS) | 1.19.4 only | ⚠️ pure readme |
| [3666](https://github.com/PrismarineJS/mineflayer/pull/3666) | Fix prismarine-windows to use registry | 2 (XS) | 1.19.3 only | |
| [3850](https://github.com/PrismarineJS/mineflayer/pull/3850) | Change headPitch to headYaw | 14 (XS) | 1.15.2 only | ⚠️ conflict |
| [3722](https://github.com/PrismarineJS/mineflayer/pull/3722) | Disable physics during config packet | 4 (XS) | 3 versions | |
| [3698](https://github.com/PrismarineJS/mineflayer/pull/3698) | createBot() documentation update | 7 (XS) | 3 versions | docs-only |

## 🤖 Bot release PRs — superseded version bumps (3)

Auto-generated `🎈` release PRs, all failing every version. The human-driven
equivalents (3902 / 3879) supersede these.

| PR | Title | Failing | Notes |
|----|-------|---------|-------|
| [3886](https://github.com/PrismarineJS/mineflayer/pull/3886) | 🎈 26.1.2 | all | superseded by 3902 |
| [3880](https://github.com/PrismarineJS/mineflayer/pull/3880) | 🎈 26.1.1 | all | ⚠️ conflict |
| [3854](https://github.com/PrismarineJS/mineflayer/pull/3854) | 🎈 26.1 | all | ⚠️ conflict |

## ⚪ Stale — no CI ran, all conflicting (from mid-2025) (3)

| PR | Title | Size | Tests | Comments |
|----|-------|------|-------|----------|
| [3539](https://github.com/PrismarineJS/mineflayer/pull/3539) | Bedrock connection & chat support | 313 (L) | 🧪 | 💬2 |
| [3548](https://github.com/PrismarineJS/mineflayer/pull/3548) | Implement skinUsesKeyedProperties 1.19.3+ | 42 (S) | — | 💬1 |
| [3588](https://github.com/PrismarineJS/mineflayer/pull/3588) | Fix rod/crossbow/bow always pointing | 11 (XS) | — | 💬2 |

---

## Duplicate / superseded clusters

- **MC version bump:** 3902 (green) supersedes bot PRs 3886/3880/3854 and the
  older 3879.
- **Buckets:** 3881 is a rebased version of 3740 (3740 ⚠️ conflicts, all
  versions failing) — 3740 is effectively replaced.
- **Cartography table:** 3778 (lint-only fail) and 3826 (lint-fixed plugin
  version) cover the same feature.
- **Velocity proxy:** 3786 and 3834 are competing implementations, both red.

## Recommended next actions

1. **Merge-ready:** review the 9 green PRs; prioritize **3902** (the actual
   26.1.2 update).
2. **Quick unblocks:** fix lint on **3778** and **3885**.
3. **Re-run CI** on the 5 suspected-flaky PRs before judging them.
4. **Decide between duplicates:** pick one of 3786/3834 (Velocity) and one of
   3778/3826 (cartography); close the other.
5. **Triage stale PRs** (3539/3548/3588): rebase-or-close.
