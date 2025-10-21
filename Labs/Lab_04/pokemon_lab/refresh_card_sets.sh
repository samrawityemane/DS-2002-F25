#!/usr/bin/env bash
echo "Refreshing all card sets in card_set_lookup/..."
for FILE in card_set_lookup/*.json; do
  SET_ID=$(basename "$FILE" .json)
  echo "Updating set: $SET_ID ..."
  URL="https://api.pokemontcg.io/v2/cards?q=set.id:${SET_ID}&pageSize=250"
  if [ -n "${POKEMON_TCG_API_KEY:-}" ]; then
    curl -sS -H "X-Api-Key: ${POKEMON_TCG_API_KEY}" "$URL" -o "$FILE"
  else
    curl -sS "$URL" -o "$FILE"
  fi
  echo "Data updated for: $FILE"
done
echo "All card sets have been refreshed."
