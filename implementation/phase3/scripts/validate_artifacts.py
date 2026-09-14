#!/usr/bin/env python3
"""Check phase3 corpus accounting and skill structure; no network or writes."""
import argparse
import collections
import json
from pathlib import Path

import yaml


def validate(root, expected):
    phase = root / 'implementation/phase3'
    manifest = json.loads((phase / 'survey_manifest.json').read_text())
    selected = {row['case_id']: row for row in manifest['prs']}
    assert len(selected) == len(manifest['prs']) == 500
    cases = [json.loads(line) for line in (phase / 'review_cases.jsonl').read_text().splitlines()]
    assert len(cases) == len({row['case_id'] for row in cases}) == expected
    for row in cases:
        meta = selected[row['case_id']]
        assert type(row['merged']) is bool
        assert row['merged'] == meta['merged']
        assert row['outcome'] == meta['merge_outcome']
        assert row['merged_at'] == meta['mergedAt']
        assert row['closed_at'] == meta['closedAt']
        assert row['split'] == meta['split']
        assert bool(row['merged_at']) == row['merged']
        assert row['url'] == meta['url']
        assert row['retrieved_at'] and row['head_sha']
        assert not row.get('collection_errors')
        for source in row['evidence']:
            assert source['url'].startswith('https://github.com/')
            assert source['author'] and source['authorship']
    if expected == 500:
        assert {row['case_id'] for row in cases} == set(selected)
    names = []
    for file in sorted((root / 'skills').glob('*/SKILL.md')):
        text = file.read_text()
        assert text.startswith('---\n')
        front = yaml.safe_load(text.split('---', 2)[1])
        assert front['name'] == file.parent.name
        assert front['description']
        names.append(front['name'])
    assert set(names) == {
        'prismarine-review',
        'prismarine-architecture-review',
        'prismarine-protocol-data-review',
        'prismarine-lifecycle-action-review',
        'prismarine-item-inventory-review',
        'prismarine-geometry-movement-review',
        'prismarine-world-render-review',
    }
    print(json.dumps({'cases': len(cases), 'outcomes': dict(collections.Counter(r['outcome'] for r in cases)),
                      'skills': names, 'result': 'passed'}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument('--expected-cases', type=int, default=500)
    args = parser.parse_args()
    validate(args.root, args.expected_cases)
