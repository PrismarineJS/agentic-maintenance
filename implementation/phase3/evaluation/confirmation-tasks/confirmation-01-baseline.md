You are a blinded historical code reviewer. Run this task in a fresh agent with no inherited conversation, using the coordinator's identical model and reasoning configuration for both arms.

Read task JSON: /tmp/prismarine-phase3/evaluation/confirmation-batches/confirmation-01-baseline.json
Do not begin if its ready field is false. The coordinator must additionally freeze the initial skill version before starting EITHER initial arm, and freeze any revised skill version before starting EITHER confirmation arm.

Do not read project review skills or discovery/survey material. Apply your ordinary code-review judgment.

Review each listed packet independently, one at a time, using only its supplied exact-revision patch and source. Do not inspect other files, repository history, PR discussion, present-day code, outcomes, other agents' predictions, private evaluation files, or the discovery corpus. Do not access network tools. Do not post comments or modify repositories. Tool reads may access only this task, its packet paths, your output, the clock, and (skills arm only) its frozen skill folder and freeze metadata.

Both arms have the same declared per-case elapsed-time cap and source context. Check the clock at each case start and finish; report observable elapsed time and limitations honestly. There is no required finding count. Analyze correctness, maintainability, modular responsibility, and practical validation where supported by the shown code. A missing file or missing test in this bounded packet alone does not establish a bug. Avoid speculative architecture requests and generic style objections. This is a bounded review, not an exhaustive runtime audit.

Append one JSON object per case to the task's predictions JSONL immediately after reviewing it. Preserve case_id, arm, model, budget, packet_sha256 and skill_set_sha256 exactly from the task/packet. Include findings (array), no_comment_reason (when empty), validation_limits (array), elapsed_seconds (number or null), and skills_used (array). Each finding contains kind (actionable or optional), path, line (integer or null), side (RIGHT or LEFT), scenario, evidence, requested_change, validation, and skills_help (skills arm only; otherwise empty). Evidence should be your reasoning with a short code reference, not long copied source. Maximum three actionable and one optional finding per case are caps, not targets. Unsupported suspicions belong in validation_limits rather than findings. Do not suggest a finding merely because historical code is being evaluated.

Stop after the assigned cases and summarize only completion count and output path to the coordinator. Never read adjudication evidence. Other review agents must not see your predictions before their own predictions are frozen.
