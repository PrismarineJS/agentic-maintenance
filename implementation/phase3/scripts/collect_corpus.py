#!/usr/bin/env python3
"""Reproducible, read-only GitHub corpus collection. Raw responses stay outside git.

Usage: python3 collect_corpus.py discover|pilot|collect
Requires authenticated gh. No GitHub mutations are performed.
"""
import concurrent.futures
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
CACHE = pathlib.Path('/tmp/prismarine-phase3')
SEED = 'prismarine-phase3-2026-09-14-v1'
REVIEWERS = ['rom1504', 'extremeheat', 'Karang']
PRIMARY = ['PrismarineJS/mineflayer', 'PrismarineJS/minecraft-data',
           'PrismarineJS/node-minecraft-protocol', 'ProtoDef-io/node-protodef']
ADJACENT = ['PrismarineJS/' + x for x in ['prismarine-physics', 'prismarine-world',
    'prismarine-chunk', 'prismarine-entity', 'prismarine-registry', 'prismarine-item',
    'prismarine-chat', 'minecraft-data-generator', 'node-minecraft-data',
    'mineflayer-pathfinder', 'prismarine-viewer', 'flying-squid']] + ['ProtoDef-io/ProtoDef']

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(obj, indent=2) + '\n')
    tmp.replace(path)

def gh(args):
    for attempt in range(5):
        p = subprocess.run(['gh', 'api'] + args, text=True, capture_output=True)
        if p.returncode == 0:
            return json.loads(p.stdout)
        if attempt == 4:
            raise RuntimeError(p.stderr[:600])
        time.sleep(2 ** attempt)

def stable(value):
    return hashlib.sha256((SEED + value).encode()).hexdigest()

def authorship_label(body):
    """Disclosure hints only: mentions/accusations do not establish authorship."""
    import re
    agent = r'(?:Astra|Claude(?: Code)?|Gemini|Copilot|Cursor|Codex|ChatGPT|Jules)'
    disclosure = re.search(r'Astra agent review|(?:from|generated (?:by|with)|written by|review(?:ed)? by|analysis by)\s+(?:an?\s+)?' + agent, body, re.I)
    if disclosure:
        return 'explicitly_agent_generated' if disclosure.start() < 100 else 'explicit_agent_content_in_mixed_or_uncertain_comment'
    return 'uncertain_or_undisclosed'

def metadata_repo(repo):
    dest = CACHE / 'metadata' / (repo.replace('/', '--') + '.json')
    if dest.exists():
        return json.loads(dest.read_text())
    rows = {}
    searches = []
    for reviewer in REVIEWERS:
        for qualifier in ['commenter', 'reviewed-by']:
            cursor = None
            query = f'repo:{repo} is:pr created:2022-09-14..2026-09-14 {qualifier}:{reviewer}'
            total = None
            while True:
                after = ',after:' + json.dumps(cursor) if cursor else ''
                gql = 'query { search(query:' + json.dumps(query) + ',type:ISSUE,first:100' + after + ') {issueCount pageInfo{hasNextPage endCursor} nodes{... on PullRequest{number title url state merged mergedAt createdAt closedAt updatedAt headRefOid baseRefOid author{login} comments{totalCount} reviews{totalCount}}}}}'
                result = gh(['graphql', '-f', 'query=' + gql])
                if result.get('errors'):
                    raise RuntimeError(str(result['errors']))
                data = result['data']['search']
                total = data['issueCount']
                if total > 1000:
                    raise RuntimeError(f'Split date interval required: {query}: {total}')
                for node in data['nodes']:
                    key = str(node['number'])
                    row = rows.setdefault(key, dict(node, repo=repo, participation_search=[]))
                    row['participation_search'].append({'reviewer': reviewer, 'qualifier': qualifier})
                if not data['pageInfo']['hasNextPage']:
                    break
                cursor = data['pageInfo']['endCursor']
            searches.append({'query': query, 'count': total})
    result = {'repository': repo, 'retrieved_at': now(), 'searches': searches, 'prs': list(rows.values())}
    dump(dest, result)
    print(f'metadata {repo}: {len(rows)} candidates', flush=True)
    return result

def pick_balanced(rows, count):
    # Round-robin repository, survey-year and observed outcome. Stable order within strata.
    groups = {}
    for row in rows:
        y = min(3, max(0, (datetime.date.fromisoformat(row['createdAt'][:10]) - datetime.date(2022, 9, 14)).days // 365))
        row['survey_year'] = y + 1
        key = (row['repo'], y, row['state'])
        groups.setdefault(key, []).append(row)
    for key, values in groups.items():
        values.sort(key=lambda x: stable(x['url']))
    chosen = []
    keys = sorted(groups, key=lambda x: stable(str(x)))
    while len(chosen) < count:
        advanced = False
        for key in keys:
            if groups[key] and len(chosen) < count:
                chosen.append(groups[key].pop(0))
                advanced = True
        if not advanced:
            break
    return chosen

def discover():
    if (ROOT / 'survey_manifest.json').exists():
        raise SystemExit('Frozen manifest already exists. Preserve it; run in a separate artifact directory to reproduce or explicitly document an amendment before replacing it.')
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        sources = list(pool.map(metadata_repo, PRIMARY + ADJACENT))
    all_rows = [r for s in sources for r in s['prs']]
    selected = pick_balanced([r for r in all_rows if r['repo'] in PRIMARY], 400)
    selected += pick_balanced([r for r in all_rows if r['repo'] in ADJACENT], 500 - len(selected))
    if len(selected) < 500:
        keys = {r['url'] for r in selected}
        selected += pick_balanced([r for r in all_rows if r['url'] not in keys], 500 - len(selected))
    # Search metadata cannot reliably resolve dependent families. Conservatively group
    # normalized near-identical titles; detailed relationship discoveries are recorded
    # later and excluded from paired evaluation when they cross the split.
    import re
    families = {}
    for row in selected:
        family = re.sub(r'\b(v?\d+(?:\.\d+)*)\b', '<version>', row['title'].lower())
        family = re.sub(r'[^a-z<>]+', ' ', family).strip()
        row['family_id'] = stable(row['repo'] + ':' + family)[:16]
        families.setdefault(row['family_id'], []).append(row)
    held = []
    for family in sorted(families, key=stable):
        members = families[family]
        if len(held) + len(members) <= 100:
            held += members
        if len(held) == 100:
            break
    held_urls = {r['url'] for r in held}
    initial, confirmation = [], []
    for family in sorted({r['family_id'] for r in held}, key=lambda x: stable('confirmation' + x)):
        members = families[family]
        if len(confirmation) + len(members) <= 20:
            confirmation += members
        else:
            initial += members
    confirm_urls = {r['url'] for r in confirmation}
    for r in selected:
        r['split'] = 'confirmation' if r['url'] in confirm_urls else 'initial_evaluation' if r['url'] in held_urls else 'discovery'
        r['case_id'] = r['repo'].replace('/', '--') + '--' + str(r['number'])
        r['inclusion_reason'] = 'Deterministic repository/year/outcome round-robin from target commenter/reviewed-by search union; participation subject to detail verification.'
        r['merged'] = bool(r['merged'])
        r['merge_outcome'] = 'merged' if r['merged'] else 'open' if r['state'] == 'OPEN' else 'closed_unmerged'
    pilot = pick_balanced([r for r in selected if r['split'] == 'discovery'], 20)
    pilot_ids = {r['case_id'] for r in pilot}
    for r in selected:
        r['pilot'] = r['case_id'] in pilot_ids
    from collections import Counter
    manifest = {'schema_version': 1, 'frozen_at': now(), 'seed': SEED,
        'window': {'created_from': '2022-09-14', 'created_through': '2026-09-14'},
        'selection': '500 total; first400 primary (or available), balance remainder adjacent; deterministic round-robin repo/survey-year/state, stable SHA256 ordering. Not latest500.',
        'state_semantics': 'Observed at metadata retrieval; merged boolean and mergedAt explicit. Merge is not correctness evidence.',
        'family_method': 'Conservative normalized-title grouping before detailed interpretation. Additional discovered relationships must be recorded and cross-split cases excluded from evaluation.',
        'candidate_count': len(all_rows), 'candidate_counts_by_repo': {s['repository']: len(s['prs']) for s in sources},
        'counts_by_repo': dict(Counter(r['repo'] for r in selected)),
        'counts_by_split': dict(Counter(r['split'] for r in selected)),
        'counts_by_outcome': dict(Counter(r['merge_outcome'] for r in selected)),
        'counts_by_year': dict(Counter(r['survey_year'] for r in selected)),
        'reviewer_search_counts': {u: sum(any(p['reviewer'] == u for p in r['participation_search']) for r in selected) for u in REVIEWERS},
        'limitations': ['Search participation is a candidate signal until actual discussions are verified.', 'Family detection from metadata is incomplete; detailed relationship checks required.', 'Authorship is uncertain unless explicitly disclosed; account identity alone does not establish human authorship.'],
        'reserves': [{'repo': r['repo'], 'number': r['number'], 'url': r['url'], 'headRefOid': r['headRefOid'], 'baseRefOid': r['baseRefOid']} for r in sorted([x for x in all_rows if x['url'] not in {s['url'] for s in selected}], key=lambda x: stable('reserve' + x['url']))],
        'reserve_policy': 'Ordered metadata-only reserves. Any substitution must be a declared manifest amendment with reason; do not replace poor evaluation results or silently include reserve cases in the500.',
        'prs': sorted(selected, key=lambda r: (r['repo'], r['number']))}
    dump(ROOT / 'survey_manifest.json', manifest)
    print(json.dumps({k: v for k, v in manifest.items() if k != 'prs'}, indent=2), flush=True)

def paginate(endpoint):
    rows = []
    page = 1
    while True:
        data = gh([endpoint + ('&' if '?' in endpoint else '?') + f'per_page=100&page={page}'])
        if not isinstance(data, list):
            raise RuntimeError('Expected list from ' + endpoint)
        rows.extend(data)
        if len(data) < 100:
            return rows
        page += 1

def collect_case(row):
    folder = 'discovery' if row['split'] == 'discovery' else 'heldout'
    dest = CACHE / folder / (row['case_id'] + '.json')
    cached = json.loads(dest.read_text()) if dest.exists() else None
    if cached and cached.get('collector_version') == 2 and not cached.get('errors'):
        return row['case_id']
    prefix = 'repos/' + row['repo']
    pr = prefix + '/pulls/' + str(row['number'])
    result = cached or {'metadata': row, 'retrieved_at': now(), 'errors': {}, 'completeness': {}}
    result['collector_version'] = 2
    for key, endpoint, multiple in [
        ('pr', pr, False), ('reviews', pr + '/reviews', True),
        ('inline_comments', pr + '/comments', True),
        ('issue_comments', prefix + '/issues/' + str(row['number']) + '/comments', True),
        ('commits', pr + '/commits', True), ('files', pr + '/files', True)]:
        if key in result:
            continue
        try:
            result[key] = paginate(endpoint) if multiple else gh([endpoint])
            result['completeness'][key] = 'complete_paginated' if multiple else 'retrieved'
            if key in result['errors']:
                result.setdefault('recovered_errors', {})[key] = result['errors'].pop(key)
        except Exception as exc:
            result['errors'][key] = str(exc)
            result['completeness'][key] = 'unavailable'
    # Checks and status at the captured head, not a claim of historical CI reconstruction.
    head = row['headRefOid']
    for key, endpoint in [('checks', prefix + '/commits/' + head + '/check-runs?per_page=100'),
                          ('status', prefix + '/commits/' + head + '/status?per_page=100')]:
        if key in result:
            continue
        try:
            result[key] = gh([endpoint])
            if key in result['errors']:
                result.setdefault('recovered_errors', {})[key] = result['errors'].pop(key)
            total = result[key].get('total_count', 0)
            result['completeness'][key] = 'first_100_truncated' if total > 100 else 'retrieved'
        except Exception as exc:
            result['errors'][key] = str(exc)
    # REST preserves inline replies and original hunks, but not thread resolution.
    # Store GraphQL thread metadata separately without duplicating comment bodies.
    try:
        owner, name = row['repo'].split('/')
        cursor = None
        threads = []
        while True:
            after = ',after:' + json.dumps(cursor) if cursor else ''
            gql = 'query {repository(owner:' + json.dumps(owner) + ',name:' + json.dumps(name) + '){pullRequest(number:' + str(row['number']) + '){reviewThreads(first:100' + after + '){pageInfo{hasNextPage endCursor} nodes{id isResolved isOutdated path line originalLine startLine originalStartLine diffSide resolvedBy{login} comments(first:100){totalCount nodes{databaseId url replyTo{databaseId}}}}}}}}'
            data = gh(['graphql', '-f', 'query=' + gql])
            if data.get('errors'):
                raise RuntimeError(str(data['errors']))
            page = data['data']['repository']['pullRequest']['reviewThreads']
            threads.extend(page['nodes'])
            if not page['pageInfo']['hasNextPage']:
                break
            cursor = page['pageInfo']['endCursor']
        result['review_threads'] = threads
        result['completeness']['review_threads'] = 'thread_metadata_complete; comment_ids_first100_perthread; full_bodies_in_paginated_REST_inline_comments'
    except Exception as exc:
        result['errors']['review_threads'] = str(exc)
    records = []
    for kind in ['reviews', 'inline_comments', 'issue_comments']:
        for c in result.get(kind, []):
            login = (c.get('user') or {}).get('login', '')
            if login.lower() in [x.lower() for x in REVIEWERS]:
                text = c.get('body') or ''
                records.append({'kind': kind, 'id': c['id'], 'url': c.get('html_url'), 'login': login,
                    'account_id': c['user']['id'], 'authorship': authorship_label(text),
                    'substantive_body': bool(text.strip()), 'commit_id': c.get('commit_id'),
                    'original_commit_id': c.get('original_commit_id')})
    result['target_participation'] = records
    result['verified_target_participation'] = bool(records)
    result['snapshot_notes'] = 'Current PR head/base are metadata, not guaranteed review-time snapshots. Review commit_id and inline original_commit_id/diff_hunk retained. Conversational concerns require reconstruction. REST commits cap250 and files cap3000 may apply; checked below.'
    if len(result.get('commits', [])) >= 250:
        result['completeness']['commits'] = 'possible_rest_250_cap'
    if len(result.get('files', [])) >= 3000:
        result['completeness']['files'] = 'possible_rest_3000_cap'
    result['completeness']['file_patches'] = 'some_missing_or_binary' if any('patch' not in f for f in result.get('files', [])) else 'all_present_but_api_may_truncate_large_patches'
    dump(dest, result)
    print('collected ' + row['case_id'] + ' ' + row['split'], flush=True)
    return row['case_id']

def collect(pilot_only=False):
    manifest = json.loads((ROOT / 'survey_manifest.json').read_text())
    rows = [r for r in manifest['prs'] if not pilot_only or r['pilot']]
    rows.sort(key=lambda r: (r['split'] == 'discovery', r['repo'] != 'PrismarineJS/minecraft-data', r['case_id']))
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        list(pool.map(collect_case, rows))

if __name__ == '__main__':
    {'discover': discover, 'pilot': lambda: collect(True), 'collect': collect}[sys.argv[1]]()
