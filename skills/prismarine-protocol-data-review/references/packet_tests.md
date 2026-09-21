# Select a fixture that exercises the claimed behavior

For a packet-driven Mineflayer plugin change, start with the existing internal fixture: a real bot backed by node-minecraft-protocol's client and local server. Use `test/internalTest.js` or its `test/internalTests` successor at the candidate revision; reuse its setup rather than inventing another version runner. Read the actual test command and version selection so a green job cannot silently exclude the added test.

Drive the server packet through the connection, let the bot initialize normally, and observe its model/event or the server's received reply. This covers packet schema selection, native types, plugin injection and connection lifecycle that a fake bot with `_client.write = () => {}` bypasses. Register the relevant listener before triggering the action. A barrier is valid only when that protocol order guarantees the event of interest has completed; sending chat or waiting an arbitrary interval is not a universal synchronization mechanism.

| Claim under review | Useful evidence | What that evidence does not establish |
|---|---|---|
| Pure attribute arithmetic, geometry or model conversion | Actual model/helper with registry/chunk data and distinguishing inputs | Packet decoding, initialization or server acceptance |
| Plugin reacts to packets or emits versioned replies | Existing NMP server/client fixture with the actual bot/plugin | Vanilla gameplay acceptance or compatibility with a different server implementation |
| NMP acknowledgements, signing or handshake behavior | Exercise both production client and server paths affected by the change; include the next message/session and negative controls | Independent wire correctness if both ends share the same incorrect assumption |
| A shared codec's wire layout | Production codec plus authoritative bytes/source; read/write/size and appropriate interpreter/compiler controls | End-to-end action success |
| Placement succeeds, inventory reconciles, live authentication completes | Relevant external-server action and authoritative resulting state, or live service trace when that is the claim | Untested versions, transports or authentication modes |

Controlled EventEmitters, providers and clocks remain useful for isolated algorithms, fault injection and reproducing an ordering failure. Distinguish such supplementary evidence from a replacement for the shipping packet path. A failing isolated probe may establish a bug; passing it alone does not answer an explicit maintainer request for a real client/server regression.

When adding or reviewing tests, compare fixture complexity with the behavior being checked. Duplicating bot construction, emulating core plugins or implementing a local packet writer often means the existing fixture should be reused. Prefer a small reusable setup only when real repeated callers justify it; do not create a universal testing module as a prerequisite for a bounded fix.

Sources: extremeheat's [Mineflayer #4118 fake-bot objection](https://github.com/PrismarineJS/mineflayer/pull/4118#discussion_r3998183658), [#4116 fixture request](https://github.com/PrismarineJS/mineflayer/pull/4116#discussion_r3998186145), and [NMP #1521 client/server review](https://github.com/PrismarineJS/node-minecraft-protocol/pull/1521#pullrequestreview-5124257368). The accepted missing-test limitation in [data #747](https://github.com/PrismarineJS/minecraft-data/pull/747#pullrequestreview-1564292284) prevents applying this as an indiscriminate new-test requirement.
