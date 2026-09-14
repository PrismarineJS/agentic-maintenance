#!/usr/bin/env python3
"""Unblind independently adjudicated findings and report exact denominators."""
import argparse
import collections
import json
from pathlib import Path


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def score(a):
    predictions = rows(a.predictions)
    judgments = [r for path in sorted(a.adjudication.glob('results-*.jsonl')) for r in rows(path)]
    by_case = {r['opaque_id']: r for r in judgments}
    assert len(by_case) == len(judgments)
    arm_key = json.loads((a.adjudication / 'private/arm_key.json').read_text())
    finding_judgments = {r['finding_id']: r for case in judgments for r in case['finding_judgments']}
    assert len(finding_judgments) == sum(len(c['finding_judgments']) for c in judgments)
    assert set(finding_judgments) == set(arm_key)
    finding_lookup = {(r['case_id'], r['arm'], r['index']): fid for fid, r in arm_key.items()}
    packets = {r['case_id']: r for r in json.loads((a.evaluation / 'packet_manifest.json').read_text())}
    risks = {r['case_id']: r['risk'] for r in json.loads((a.evaluation / 'cross_split_link_summary.json').read_text())}
    groups = {'all': lambda k: True,
              'strict': lambda k: risks[k] == 'no_direct_link_found',
              'strict_cumulative': lambda k: risks[k] == 'no_direct_link_found' and packets[k]['scope'] == 'cumulative_review_revision',
              'strict_hunk_only': lambda k: risks[k] == 'no_direct_link_found' and packets[k]['scope'] != 'cumulative_review_revision',
              'overlap_sensitive': lambda k: risks[k] != 'no_direct_link_found'}
    if a.exclude_cases:
        excluded = set(json.loads(a.exclude_cases.read_text()))
        assert excluded <= set(packets)
        groups.update({
            'clean_sensitivity': lambda k: risks[k] == 'no_direct_link_found' and k not in excluded,
            'clean_cumulative_sensitivity': lambda k: risks[k] == 'no_direct_link_found' and k not in excluded and packets[k]['scope'] == 'cumulative_review_revision',
            'clean_hunk_sensitivity': lambda k: risks[k] == 'no_direct_link_found' and k not in excluded and packets[k]['scope'] != 'cumulative_review_revision',
        })
    result = {}
    for group, include in groups.items():
        result[group] = {}
        for arm in ('baseline', 'skills'):
            selected = [r for r in predictions if r['arm'] == arm and include(r['case_id'])]
            counts = collections.Counter(cases=len(selected))
            eligible, recovered, elapsed = set(), set(), []
            for p in selected:
                key = p['case_id']
                case = by_case[key]
                refs = {r['reference_id'] for r in case['reference_issues'] if r['actionable_in_snapshot']}
                eligible.update((key, rid) for rid in refs)
                counts['no_comment_cases'] += not p['findings']
                if isinstance(p.get('elapsed_seconds'), (int, float)):
                    elapsed.append(p['elapsed_seconds'])
                    counts['cases_exceeding_declared_cap'] += p['elapsed_seconds'] > p['budget']['seconds_per_case']
                for index, f in enumerate(p['findings']):
                    verdict = finding_judgments[finding_lookup[(key, arm, index)]]
                    assert verdict['verdict'] in ('supported_actionable', 'supported_optional', 'unsupported', 'uncertain')
                    counts['findings'] += 1
                    counts[verdict['verdict']] += 1
                    counts[f['kind'] + '_proposed'] += 1
                    counts[f['kind'] + '_' + verdict['verdict']] += 1
                    assert set(verdict['matched_reference_ids']) <= refs, (key, verdict)
                    if f['kind'] == 'actionable' and verdict['verdict'] == 'supported_actionable':
                        recovered.update((key, rid) for rid in verdict['matched_reference_ids'])
            counts['eligible_reference_issues'] = len(eligible)
            counts['recovered_actionable_references'] = len(recovered)
            result[group][arm] = {**dict(counts), 'reported_case_seconds_total': sum(elapsed),
                                  'cases_with_elapsed_measurement': len(elapsed)}
    a.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'adjudicated_cases': len(judgments), 'predictions': len(predictions), 'output': str(a.output)}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--predictions', type=Path, required=True)
    parser.add_argument('--adjudication', type=Path, required=True)
    parser.add_argument('--evaluation', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--exclude-cases', type=Path, help='Post-hoc exposure exclusion IDs; adds sensitivity groups without replacing original groups.')
    score(parser.parse_args())
