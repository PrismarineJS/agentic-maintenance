#!/usr/bin/env python3
"""Read-only verification of recorded phase3 GitHub inline reviews.

Accept an array of agent result rows. Fetch remote evidence for posted reviews;
never create, edit, approve or dismiss a review. Semantic deduplication and the
correctness of findings still require human/agent judgment.
"""
import argparse
import datetime
import json
import re
from pathlib import Path

from snapshot_u9g import api

HEADER = '**Astra agent review — AI-generated, not manually written by the maintainer.**'


def locations(patch):
    """Map visible RIGHT/LEFT diff lines to whether that side changed."""
    found = {}
    left = right = None
    for line in (patch or '').splitlines():
        match = re.match(r'^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@', line)
        if match:
            left, right = map(int, match.groups())
        elif left is not None:
            if line.startswith('+'):
                found[('RIGHT', right)] = True
                right += 1
            elif line.startswith('-'):
                found[('LEFT', left)] = True
                left += 1
            elif line.startswith(' '):
                found[('RIGHT', right)] = found[('LEFT', left)] = False
                left += 1
                right += 1
    return found


def audit(row):
    base = f"repos/{row['repo']}/pulls/{row['number']}"
    pr = api(base)
    review = api(base + f"/reviews/{row['review_id']}")
    comments = [c for c in api(base + '/comments?per_page=100', True)
                if c['pull_request_review_id'] == row['review_id']]
    files = {f['filename']: f for f in api(base + '/files?per_page=100', True)}
    errors, notes = [], []

    def require(condition, message):
        if not condition:
            errors.append(message)

    require(review['state'] == 'COMMENTED', 'review state is not COMMENTED')
    require(review['commit_id'] == row['head'], 'review commit differs from recorded head')
    require(review['body'].startswith(HEADER), 'review attribution header missing')
    require(any(s in review['body'] for s in row['skills_used']), 'review names no recorded skill')
    require(len(comments) == len(row['inline_comments']), 'remote inline count differs')
    same_head = pr['head']['sha'] == row['head']
    if not same_head:
        notes.append('Head changed after review; current-diff line checks are inapplicable.')
    if pr['state'] != 'open':
        notes.append('PR is no longer open at verification.')
    verified = []
    for expected in row['inline_comments']:
        url = expected.get('url') or expected.get('URL')
        comment = next((c for c in comments if c['html_url'] == url), None)
        require(comment is not None, 'recorded inline URL absent from review: ' + str(url))
        if comment is None:
            continue
        require(comment['body'] == expected['body'], 'inline body differs: ' + url)
        require(comment['body'].startswith(HEADER), 'inline attribution header missing: ' + url)
        require(any(s in comment['body'] for s in row['skills_used']), 'inline names no recorded skill: ' + url)
        require(comment['path'] == expected['path'], 'inline path differs: ' + url)
        require(comment['commit_id'] == row['head'], 'inline commit differs: ' + url)
        require(comment['side'] == expected.get('side', 'RIGHT'), 'inline side differs: ' + url)
        require((comment['line'] if same_head else comment['original_line']) == expected['line'], 'inline line differs: ' + url)
        changed = None
        if same_head:
            file = files.get(comment['path'])
            require(file is not None, 'inline path absent from current diff: ' + url)
            if file and file.get('patch'):
                changed = locations(file['patch']).get((comment['side'], comment['line']))
                require(changed is not None, 'inline line absent from returned diff: ' + url)
                if changed is False:
                    notes.append('Inline is on diff context; manually assess placement: ' + url)
            elif file:
                notes.append('API omitted patch; line visibility needs separate check: ' + url)
        verified.append({'id': comment['id'], 'url': url, 'path': comment['path'],
                         'line': comment['line'], 'original_line': comment['original_line'],
                         'side': comment['side'], 'changed_line': changed,
                         'author': comment['user']['login'], 'created_at': comment['created_at']})
    return {'repo': row['repo'], 'number': row['number'], 'review_id': review['id'],
            'review_url': review['html_url'], 'review_state': review['state'],
            'review_body': review['body'], 'review_head': review['commit_id'],
            'current_head': pr['head']['sha'], 'state': pr['state'], 'merged': pr['merged'],
            'verified_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'inline_comments': verified, 'errors': errors, 'notes': notes}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('results', type=Path)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    rows = json.loads(args.results.read_text())
    audited = []
    for row in rows:
        if row['status'] != 'posted':
            continue
        audited.append(audit(row))
        args.output.write_text(json.dumps(audited, indent=2) + '\n')
        print(row['repo'], row['number'], 'errors:', len(audited[-1]['errors']), flush=True)
    if not audited:
        args.output.write_text('[]\n')
    if any(r['errors'] for r in audited):
        raise SystemExit('Publication verification found errors; inspect output.')


if __name__ == '__main__':
    main()
