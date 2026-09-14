#!/usr/bin/env python3
"""Create stage-scoped adjudication tasks with prediction arms concealed.

Run only after that stage's predictions have been audited and frozen. This
script prepares evidence; it does not assign semantic verdicts or read a later
stage's discussion. The anonymous-to-arm key is kept out of reviewer tasks.
"""
import argparse
import hashlib
import json
from pathlib import Path


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def main(a):
    selected = [r for r in json.loads(a.manifest.read_text())['prs'] if r['split'] == a.stage]
    packets = {r['case_id']: r for r in json.loads((a.evaluation / 'packet_manifest.json').read_text())}
    predictions = [json.loads(line) for line in a.predictions.read_text().splitlines()]
    expected = {k for k, v in packets.items() if v['split'] == a.stage and v['status'] == 'prepared'}
    assert {(r['case_id'], r['arm']) for r in predictions} == {(k, arm) for k in expected for arm in ('baseline', 'skills')}
    assert len(predictions) == 2 * len(expected)
    key, cases = {}, []
    for meta in selected:
        opaque = 'case-' + hashlib.sha256(f"{meta['repo']}#{meta['number']}".encode()).hexdigest()[:12]
        packet = packets[opaque]
        findings = []
        for prediction in predictions:
            if prediction['case_id'] != opaque:
                continue
            for index, finding in enumerate(prediction['findings']):
                fid = 'finding-' + hashlib.sha256(f"phase3-judgment:{opaque}:{prediction['arm']}:{index}".encode()).hexdigest()[:16]
                key[fid] = {'case_id': opaque, 'arm': prediction['arm'], 'index': index}
                findings.append({'finding_id': fid, **{k: v for k, v in finding.items() if k != 'skills_help'}})
        findings.sort(key=lambda r: r['finding_id'])
        anonymous = a.output / 'anonymous' / (opaque + '.json')
        dump(anonymous, {'case_id': opaque, 'findings': findings})
        cases.append({'case_id': meta['case_id'], 'opaque_id': opaque, 'metadata': meta,
                      'raw': str(a.cache / (meta['case_id'] + '.json')),
                      'packet': packet.get('packet'), 'packet_scope': packet.get('scope'),
                      'exclusion_reason': packet.get('reason'), 'anonymous_predictions': str(anonymous)})
    cases.sort(key=lambda r: (r['packet'] is None, r['opaque_id']))
    dump(a.output / 'private' / 'arm_key.json', key)
    for group in range(a.groups):
        rows = cases[group::a.groups]
        path = a.output / f'task-{group + 1:02d}.json'
        dump(path, {'stage': a.stage, 'cases': rows,
                    'results': str(a.output / f'results-{group + 1:02d}.jsonl')})
    print(json.dumps({'stage': a.stage, 'cases': len(cases), 'prepared': len(expected),
                      'predictions_sha256': hashlib.sha256(a.predictions.read_bytes()).hexdigest(),
                      'groups': a.groups, 'output': str(a.output)}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest', type=Path, required=True)
    p.add_argument('--evaluation', type=Path, required=True)
    p.add_argument('--cache', type=Path, required=True)
    p.add_argument('--predictions', type=Path, required=True)
    p.add_argument('--stage', choices=['initial_evaluation', 'confirmation'], required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--groups', type=int, default=2)
    args = p.parse_args()
    assert args.groups > 0
    main(args)
