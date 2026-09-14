# Numeric mapper review correction

`numeric_mapper_paths.cjs` reproduces the distinction behind the withdrawals on
[Mineflayer #4086](https://github.com/PrismarineJS/mineflayer/pull/4086#discussion_r4004019860)
and [#4089](https://github.com/PrismarineJS/mineflayer/pull/4089#discussion_r4004042201).
It selects an existing runtime by its absolute package.json path and uses its
actual node-minecraft-protocol serializer/deserializer. It opens no network
connection and changes no application files.

```sh
node numeric_mapper_paths.cjs /absolute/path/to/runtime/package.json
```

Executed with these released dependency combinations:

| minecraft-protocol | minecraft-data | protodef | Result |
| --- | --- | --- | --- |
| 1.67.0 | 3.114.0 | 1.19.0 | Five numeric/named packet comparisons pass. |
| 1.68.0 | 3.116.0 | 1.19.0 | Same result; captured in `numeric_mapper_paths-output.json`. |

Both combinations encode numeric respawn/statistics/gamerule actions and
main/off-hand values through the default compiled mapper. The isolated
interpreted mapper rejects the numeric hand. These are different code paths;
the interpreted error did not establish the claimed production failure.

This checks the disputed encoding behavior, not vanilla server acceptance or
the complete entity-interaction feature/data-release chain. The per-PR records
and independent cross-checks cover the actual event handlers separately.
