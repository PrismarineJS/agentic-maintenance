#!/usr/bin/env python3
"""Normalize manually curated discovery records, enriching metadata from the cache.

Does not read heldout cases or generate lessons. Raw discussions stay outside git.
"""
import argparse
import json
from pathlib import Path


def combine(manifest_path, analysis, cache, output):
    manifest = json.loads(manifest_path.read_text())
    selected = {r['case_id']: r for r in manifest['prs'] if r['split'] == 'discovery'}
    rows = {}
    for worker in ('root', 'principles', 'corpus', 'eval_setup'):
        for line in (analysis / (worker + '-cases.jsonl')).read_text().splitlines():
            record = json.loads(line)
            key = record['case_id']
            assert key in selected and key not in rows, key
            meta = selected[key]
            raw = json.loads((cache / (key + '.json')).read_text())
            assert not raw['errors'], (key, raw['errors'])
            assert record['merged'] == meta['merged'], key
            evidence = []
            for kind in ('reviews', 'inline_comments', 'issue_comments'):
                for item in raw[kind]:
                    if (item.get('user') or {}).get('login', '').lower() not in ('rom1504', 'extremeheat', 'karang'):
                        continue
                    attribution = next((p for p in raw['target_participation'] if p['kind'] == kind and p['id'] == item['id']), {})
                    evidence.append({
                        'id': item['id'], 'kind': kind, 'url': item.get('html_url'),
                        'author': item['user']['login'], 'account_id': item['user']['id'],
                        'authorship': attribution.get('authorship', 'uncertain_or_undisclosed'),
                        'created_at': item.get('created_at') or item.get('submitted_at'),
                        'review_commit': item.get('commit_id'), 'original_commit': item.get('original_commit_id'),
                        'path': item.get('path'), 'original_line': item.get('original_line'),
                        'review_state': item.get('state'),
                    })
            rows[key] = {
                'schema_version': 1, 'case_id': key, 'repo': meta['repo'], 'number': meta['number'],
                'url': meta['url'], 'title': meta['title'], 'split': meta['split'],
                'family_id': meta['family_id'], 'pilot': meta['pilot'],
                'merged': meta['merged'], 'merged_at': meta['mergedAt'],
                'closed_at': meta['closedAt'], 'created_at': meta['createdAt'],
                'outcome': meta['merge_outcome'], 'retrieved_at': raw['retrieved_at'],
                'base_sha': raw['pr']['base']['sha'], 'head_sha': raw['pr']['head']['sha'],
                'summary': record.get('summary') or record.get('behavior') or record.get('requested_behavior'),
                'lessons': record.get('lessons') or [{'text': record['scoped_lesson'], 'kind': record.get('lesson_kind') or record.get('lesson_status')}],
                'tags': record.get('tags') or record.get('classes', []),
                'evidence': evidence, 'analysis': record, 'analyst': worker,
                'collection_errors': raw['errors'],
                'review_thread_metadata': raw.get('review_threads'),
            }
    assert set(rows) == set(selected), set(selected) - set(rows)
    output.write_text(''.join(json.dumps(rows[k], ensure_ascii=False) + '\n' for k in sorted(rows)))
    print(json.dumps({'discovery_cases': len(rows), 'output': str(output)}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest', type=Path, required=True)
    p.add_argument('--analysis', type=Path, required=True)
    p.add_argument('--cache', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    combine(a.manifest, a.analysis, a.cache, a.output)
