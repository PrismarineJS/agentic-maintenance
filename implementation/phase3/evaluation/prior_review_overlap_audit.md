# Post-hoc audit of prior phase2 exposure

Date: 2026-09-14. The audit reconstructs every one of the 45 prepared phase3 packet identities from the frozen survey's `repo#number` using the preparation script's SHA-256 prefix. It compares them against all 53 phase2 inline-review records, all 69 phase2 classifications, and the separately excluded mineflayer #4104 pilot. This is an additional, post-hoc screen; original discovery-link flags and scores remain unchanged.

Two prepared packets have exact prior-exposure matches. Both are confirmation cumulative packets originally labelled `no_direct_link_found` and included in the predeclared strict group. Both also use the exact revision previously inspected in phase2.

| Packet | Prior phase2 status | Same historical revision |
| --- | --- | --- |
| Mineflayer #4087, `case-d03f269e7db8` | Classified category 2; reviewed and validated, publication skipped because no distinct new finding was justified | `dc290378d252dda9026c5183e2dd2431a58e1ae5` |
| Mineflayer #4093, `case-ffb4575ce459` | Classified category 2; Astra review posted concerning dismount physics timing and held-sneak restoration | `9eb574f3849981d1dfa784258cbaa88411911ecb` |

No initial prepared packet overlaps these registries. The #4104 pilot does not overlap any prepared packet. There are no additional classification-only or inline-only matches among the 45 packets.

A skipped publication is still prior review exposure: the #4087 record documents reading the diff/discussion and validating resource-pack packet sequences. The #4093 record includes an explicitly Astra-authored review and concrete reproductions. These artifacts establish prior project exposure, while they do not prove that either fresh confirmation reviewer accessed or recalled phase2 material.

Preserve the originally declared results and add a separately labelled **post-hoc exclusion of prior phase2 exposure**. This leaves the initial strict group unchanged at 27 cumulative plus one hunk-only packet; confirmation changes from eight cumulative plus one hunk-only packet to six cumulative plus one hunk-only packet. The original eight discovery-link-sensitive packets remain a separate initial stratum. Ground-truth judgments need not change for this sensitivity analysis; the limitation concerns independence.

This exact-identity check cannot establish freedom from related-PR, shared-code or unrecorded exposure. No quality or adoption conclusion follows from the overlap counts alone.

[All 45 identity checks, exact overlap statuses, revisions and input hashes](prior_review_overlap_audit.json) preserve the evidence. Sources are [phase2 review records](../../phase2/u9g_inline_reviews.json), [phase2 classifications](../../../design/phase2/u9g_pr_classification.json), and the [pilot exclusion record](../../phase2/u9g_inline_reviews.md).

[Machine-readable case IDs for the post-hoc exclusion](prior_exposure_excluded_case_ids.json) contain only the two exact prior-exposure matches.
