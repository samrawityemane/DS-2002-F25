
import sys, json, csv

try:
    raw = sys.stdin.read().strip()
    if not raw:
        print("Error: No JSON received on stdin. Did you forget the pipe from curl?", file=sys.stderr)
        sys.exit(1)
    data = json.loads(raw)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON received from the pipe. Detail: {e}", file=sys.stderr)
    sys.exit(1)

fieldnames = ['card_id','card_name','set_name','rarity','market_price']
writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, restval="N/A")
writer.writeheader()


cards = data.get('data', [])
if not isinstance(cards, list):
    print("Error: JSON structure not as expected (missing 'data' list).", file=sys.stderr)
    sys.exit(1)

def get_market_price(card):
    prices = card.get('tcgplayer', {}).get('prices', {})
    for key in ('holofoil','normal','reverseHolofoil'):
        v = prices.get(key, {}).get('market')
        if v is not None:
            return v
    return 'N/A'

for c in cards:
    writer.writerow({
        'card_id': c.get('id','N/A'),
        'card_name': c.get('name','N/A'),
        'set_name': c.get('set',{}).get('name','N/A'),
        'rarity': c.get('rarity','N/A'),
        'market_price': get_market_price(c),
    })
