"""Check exact citation membership in supplied transcript paragraphs; no model call."""
import argparse
import json
from pathlib import Path
import sys


def build_sources(rows):
    if not isinstance(rows, list):
        raise ValueError('sources must be an array')
    result = {}
    for source in rows:
        sid = source.get('sourceId')
        paragraphs = source.get('paragraphs')
        if not isinstance(sid, str) or not sid.strip() or sid in result:
            raise ValueError('sourceId must be a unique nonempty string')
        if not isinstance(paragraphs, list):
            raise ValueError('paragraphs must be an array')
        result[sid] = {}
        for paragraph in paragraphs:
            pid, text = paragraph.get('id'), paragraph.get('text')
            if not isinstance(pid, str) or not pid.strip() or pid in result[sid]:
                raise ValueError('paragraph id must be unique within source')
            if not isinstance(text, str):
                raise ValueError('paragraph text must be a string')
            result[sid][pid] = text
    return result


def check(data):
    sources = build_sources(data.get('sources'))
    citations = data.get('citations')
    if not isinstance(citations, list):
        raise ValueError('citations must be an array')
    results, ids = [], set()
    for citation in citations:
        cid = citation.get('id')
        sid, pid, quote = (citation.get(k) for k in ('sourceId', 'paragraphId', 'quote'))
        if not isinstance(cid, str) or not cid.strip() or cid in ids:
            raise ValueError('citation id must be a unique nonempty string')
        if not all(isinstance(v, str) for v in (sid, pid, quote)):
            raise ValueError('citation sourceId, paragraphId and quote must be strings')
        ids.add(cid)
        row = {'id': cid, 'sourceId': sid, 'paragraphId': pid}
        if not quote.strip():
            row.update(status='unverifiable', reason='Empty quote provides no evidence.')
        elif sid not in sources:
            row.update(status='unverifiable', reason='The specified source was not supplied.')
        elif pid not in sources[sid]:
            row.update(status='unverifiable', reason='The specified paragraph was not supplied for this source.')
        elif quote in sources[sid][pid]:
            row.update(status='match', reason='Exact quote found in specified source paragraph.')
        else:
            text = sources[sid][pid]
            row.update(status='mismatch', reason='Exact quote absent from specified paragraph; this does not establish absence from the full transcript.')
            if ''.join(quote.split()) in ''.join(text.split()):
                row['formattingHint'] = 'Matches only after whitespace removal; verify manually.'
        results.append(row)
    counts = {status: sum(r['status'] == status for r in results)
              for status in ('match', 'mismatch', 'unverifiable')}
    return {'scope': 'Exact citation membership only; no semantic correctness assessment.',
            'counts': counts, 'results': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding='utf-8'))
        report = check(data)
        encoded = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
        if args.output:
            if args.output.resolve() == args.input.resolve():
                raise ValueError('output must differ from input')
            args.output.write_text(encoded, encoding='utf-8')
        else:
            sys.stdout.write(encoded)
    except (ValueError, OSError, TypeError, AttributeError) as exc:
        print(f'Input/output error: {exc}', file=sys.stderr)
        return 2
    return 1 if report['counts']['mismatch'] or report['counts']['unverifiable'] else 0


if __name__ == '__main__':
    sys.exit(main())
