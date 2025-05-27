import json

with open('seluruh_hasil.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(f'Total artikel dalam gabungan.json: {len(data)}')
