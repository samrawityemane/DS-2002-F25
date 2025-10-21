#!/usr/bin/env bash
read -rp "Enter TCG Card Set ID (e.g., base1, base4): " SET_ID
if [ -z "$SET_ID" ]; then echo "Error: Set ID cannot be empty." >&2; exit 1; fi
echo "Fetching cards for set: $SET_ID ..."
URL="https://api.pokemontcg.io/v2/cards?q=set.id:${SET_ID}&pageSize=250"
if [ -n "${POKEMON_TCG_API_KEY:-}" ]; then
  curl -sS -H "X-Api-Key: ${POKEMON_TCG_API_KEY}" "$URL" -o "card_set_lookup/${SET_ID}.json"
else
  curl -sS "$URL" -o "card_set_lookup/${SET_ID}.json"
fi
echo "Data for set '$SET_ID' has been saved to card_set_lookup/${SET_ID}.json"
