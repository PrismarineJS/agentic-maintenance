#!/usr/bin/env python3
"""Append individually adjudicated heldout context to the tracked survey.

Run after stage predictions and adjudication are complete. Does not synthesize
new policy or inspect another stage. Re-running a stage replaces only its rows.
"""
import argparse
import json
from pathlib import Path


def main(a):
    manifest = {r['case_id']: r for r in json.loads(a.manifest.read_text())['prs']}
    existing = {r['case_id']: r for r in (json.loads(line) for line in a.output.read_text().splitlines())}
    analyses = [json.loads(line) for p in sorted(a.adjudication.glob('results-*.jsonl')) for line in p.read_text().splitlines()]
    expected = {key for key, r in manifest.items() if r['split'] == a.stage}
    assert len(analyses) == len(expected) and {r['case_id'] for r in analyses} == expected
    for analysis in analyses:
        key = analysis['case_id']
        meta = manifest[key]
        raw = json.loads((a.cache / (key + '.json')).read_text())
        assert analysis['merged'] == meta['merged']
        assert analysis['outcome'] == meta['merge_outcome']
        assert not raw['errors']
        evidence = []
        for kind in ('reviews', 'inline_comments', 'issue_comments'):
            for c in raw[kind]:
                if (c.get('user') or {}).get('login', '').lower() not in ('rom1504', 'extremeheat', 'karang'):
                    continue
                attribution = next((r['authorship'] for r in raw['target_participation'] if r['kind'] == kind and r['id'] == c['id']), 'uncertain_or_undisclosed')
                evidence.append({'id': c['id'], 'kind': kind, 'url': c['html_url'], 'author': c['user']['login'],
                                 'account_id': c['user']['id'], 'authorship': attribution,
                                 'created_at': c.get('created_at') or c.get('submitted_at'),
                                 'review_commit': c.get('commit_id'), 'original_commit': c.get('original_commit_id'),
                                 'path': c.get('path'), 'original_line': c.get('original_line'), 'review_state': c.get('state')})
        existing[key] = {
            'schema_version': 1, 'case_id': key, 'repo': meta['repo'], 'number': meta['number'], 'url': meta['url'],
            'title': meta['title'], 'split': meta['split'], 'family_id': meta['family_id'], 'pilot': False,
            'merged': meta['merged'], 'merged_at': meta['mergedAt'], 'closed_at': meta['closedAt'],
            'created_at': meta['createdAt'], 'outcome': meta['merge_outcome'], 'retrieved_at': raw['retrieved_at'],
            'base_sha': raw['pr']['base']['sha'], 'head_sha': raw['pr']['head']['sha'],
            'summary': analysis['summary'], 'lessons': [{'text': analysis['lesson'], 'kind': 'heldout_context_not_discovery_policy'}],
            'evidence': evidence, 'analysis': analysis, 'analyst': 'independent_' + a.stage + '_adjudication',
            'collection_errors': raw['errors'], 'review_thread_metadata': raw.get('review_threads'),
        }
    a.output.write_text(''.join(json.dumps(existing[k], ensure_ascii=False) + '\n' for k in sorted(existing)))
    print(json.dumps({'stage': a.stage, 'added_or_replaced': len(analyses), 'total_cases': len(existing)}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest', type=Path, required=True)
    p.add_argument('--adjudication', type=Path, required=True)
    p.add_argument('--cache', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--stage', choices=['initial_evaluation', 'confirmation'], required=True)
    main(p.parse_args())
