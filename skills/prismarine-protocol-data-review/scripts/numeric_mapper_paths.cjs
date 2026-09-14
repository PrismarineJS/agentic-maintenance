// Reproduce the codec-path distinction behind the #4086/#4089 withdrawals.
// Usage: node numeric_mapper_paths.cjs /absolute/path/to/runtime/package.json
// The selected runtime must provide minecraft-protocol, minecraft-data and protodef.
// This performs encoding/decoding only; it opens no connection and writes no files.
const assert = require('node:assert/strict')
const { createRequire } = require('node:module')
const { resolve } = require('node:path')
const requireRuntime = createRequire(resolve(process.argv[2] || 'package.json'))
const mc = requireRuntime('minecraft-protocol')
const { ProtoDef } = requireRuntime('protodef')
const encoder = mc.createSerializer({ version: '26.1', state: 'play', isServer: false })
const decoder = mc.createDeserializer({ version: '26.1', state: 'play', isServer: true })
const results = []

for (const [numeric, named] of [[0, 'perform_respawn'], [1, 'request_stats'], [2, 'request_gamerule_values']]) {
  check('client_command', 'actionId', numeric, named, {})
}
for (const [numeric, named] of [[0, 'main_hand'], [1, 'off_hand']]) {
  check('use_entity', 'hand', numeric, named, { target: 1, location: { x: 0, y: 0, z: 0 }, sneaking: false })
}

function check (name, field, numeric, named, rest) {
  const packet = value => ({ name, params: { ...rest, [field]: value } })
  const bytes = encoder.createPacketBuffer(packet(numeric))
  assert.deepEqual(bytes, encoder.createPacketBuffer(packet(named)))
  const decoded = decoder.parsePacketBuffer(bytes).data
  assert.equal(decoded.params[field], named)
  results.push({ name, field, numeric, named, bytes: bytes.toString('hex'), decoded })
}

const interpreted = new ProtoDef(false)
interpreted.addType('hand', ['mapper', { type: 'varint', mappings: { 0: 'main_hand', 1: 'off_hand' } }])
let interpretedNumericError = null
try { interpreted.createPacketBuffer('hand', 0) } catch (error) { interpretedNumericError = error.message }
assert.equal(interpreted.createPacketBuffer('hand', 'main_hand').toString('hex'), '00')
console.log(JSON.stringify({
  versions: Object.fromEntries(['minecraft-protocol', 'minecraft-data', 'protodef'].map(name => [name, requireRuntime(name + '/package.json').version])),
  compiledProductionChecks: results,
  interpretedNumericError
}, null, 2))
