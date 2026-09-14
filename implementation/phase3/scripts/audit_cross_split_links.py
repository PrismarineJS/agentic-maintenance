#!/usr/bin/env python3
"""Conservative cross-split link screening; answer-bearing contexts stay private.

Direct links do not prove shared answers, and absent links do not prove independence.
This screening is intentionally conservative; semantic adjudication comes only
after the relevant skills and predictions are frozen.
"""
import argparse
import collections
import json
import pathlib
import re


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--cache', required=True)
    parser.add_argument('--evaluation', required=True)
    args = parser.parse_args()
    root, evaluation = pathlib.Path(args.cache), pathlib.Path(args.evaluation)
    rows = json.loads(pathlib.Path(args.manifest).read_text())['prs']
    by_id = {(r['repo'].lower(), r['number']): r for r in rows}
    edges = []
    for row in rows:
        path = root / ('discovery' if row['split'] == 'discovery' else 'heldout') / (row['case_id'] + '.json')
        data = json.loads(path.read_text())
        texts = [('body', data.get('pr', {}).get('body') or '')]
        for key in ('issue_comments', 'reviews', 'inline_comments'):
            texts.extend((str(c.get('id')), c.get('body') or '') for c in data.get(key, []))
        for source, body in texts:
            matches = [(m, (m[1] + '/' + m[2]).lower(), int(m[3])) for m in
                       re.finditer(r'https://github\.com/([^/\s<>]+)/([^/\s<>]+)/(?:pull|issues)/(\d+)', body)]
            matches.extend((m, row['repo'].lower(), int(m[1])) for m in
                           re.finditer(r'(?<![/\w])#(\d+)\b', body))
            for match, repo, number in matches:
                target = by_id.get((repo, number))
                if not target or target['split'] == row['split']:
                    continue
                context = body[max(0, match.start() - 160):match.end() + 160]
                signal = bool(re.search(r'block(?:ed|ing)?|depend|after|before|fix(?:es|ed)?|clos(?:es|ed)|continu|supersed|rebas|merge|same|related|implement|cherry|version|ported', context, re.I))
                edges.append({'source_case': row['case_id'], 'target_case': target['case_id'],
                              'source_split': row['split'], 'target_split': target['split'],
                              'source_id': source, 'relation_signal': signal,
                              'private_context': context})
    identity_map = {}
    for path in (evaluation / 'private' / 'answers').glob('*.json'):
        case = json.loads(path.read_text())['case']
        identity_map[case.get('case_id', case.get('metadata', {}).get('case_id'))] = path.stem
    linked = collections.defaultdict(list)
    for edge in edges:
        for key in ('source_case', 'target_case'):
            if edge[key] in identity_map:
                linked[identity_map[edge[key]]].append(edge)
    public = []
    for packet in json.loads((evaluation / 'packet_manifest.json').read_text()):
        if packet['status'] != 'prepared':
            continue
        links = linked.get(packet['case_id'], [])
        discovery_links = [e for e in links if 'discovery' in (e['source_split'], e['target_split'])]
        public.append({'case_id': packet['case_id'],
                       'cross_discovery_link_count': len(discovery_links),
                       'cross_evaluation_stage_link_count': len(links) - len(discovery_links),
                       'relation_signal_count': sum(e['relation_signal'] for e in links),
                       'risk': 'potential_same_change' if any(e['relation_signal'] for e in links)
                       else ('generic_or_uncertain_reference' if links else 'no_direct_link_found')})
    (evaluation / 'private' / 'cross_split_links.json').write_text(json.dumps({'edges': edges, 'packet_links': dict(linked)}, indent=2) + '\n')
    (evaluation / 'cross_split_link_summary.json').write_text(json.dumps(public, indent=2) + '\n')
    print(json.dumps(dict(collections.Counter(x['risk'] for x in public))))


if __name__ == '__main__':
    main()
