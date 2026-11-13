import os, json, datetime, requests

def fetch_trending(tags='python'):
    endpoint = 'https://api.stackexchange.com/2.3/questions'
    params = {
        'order': 'desc',
        'sort': 'views',
        'tagged': tags,
        'site': 'stackoverflow',
        'pagesize': 20,
        'filter': '!*-f(6rc.lF)'
    }
    resp = requests.get(endpoint, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    results = [{
        'question_id': q['question_id'],
        'title': q['title'],
        'link': q['link'],
        'view_count': q['view_count'],
        'score': q['score'],
        'creation_date': datetime.datetime.utcfromtimestamp(q['creation_date']).isoformat() + 'Z'
    } for q in data.get('items', [])]
    payload = {
        'tags': tags,
        'generated_at': datetime.datetime.utcnow().isoformat() + 'Z',
        'questions': results
    }
    return payload

if __name__ == '__main__':
    tags = os.getenv('DEFAULT_TAGS', 'python')
    data = fetch_trending(tags)
    out_path = os.path.join('docs', 'trending.json')
    os.makedirs('docs', exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'Wrote {out_path}')
