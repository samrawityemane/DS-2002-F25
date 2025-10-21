
import os, sys, json, glob
import pandas as pd

def _load_lookup_data(lookup_dir: str) -> pd.DataFrame:
    all_lookup_df = []
    for path in glob.glob(os.path.join(lookup_dir, "*.json")):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "data" not in data or not isinstance(data["data"], list):
            continue
        df = pd.json_normalize(data["data"])
        df["card_market_value"] = (
            df.get("tcgplayer.prices.holofoil.market")
              .fillna(df.get("tcgplayer.prices.normal.market"))
              .fillna(0.0)
              .astype(float)
        )
        df = df.rename(columns={
            "id":"card_id",
            "name":"card_name",
            "number":"card_number",
            "set.id":"set_id",
            "set.name":"set_name",
        })
        required_cols = ["card_id","card_name","card_number","set_id","set_name","card_market_value"]
        df = df.reindex(columns=required_cols)
        all_lookup_df.append(df)

    if not all_lookup_df:
        return pd.DataFrame(columns=["card_id","card_name","card_number","set_id","set_name","card_market_value"])

    lookup_df = pd.concat(all_lookup_df, ignore_index=True)
    lookup_df = lookup_df.sort_values(by=["card_id","card_market_value"], ascending=[True, False])
    lookup_df = lookup_df.drop_duplicates(subset=["card_id"], keep="first").reset_index(drop=True)
    return lookup_df


def _load_inventory_data(inventory_dir: str) -> pd.DataFrame:
    parts = [pd.read_csv(p) for p in glob.glob(os.path.join(inventory_dir, "*.csv"))]
    if not parts:
        return pd.DataFrame(columns=[
            "card_name","set_id","card_number","binder_name","page_number","slot_number","card_id"
        ])
    inventory_df = pd.concat(parts, ignore_index=True)
    inventory_df["set_id"] = inventory_df["set_id"].astype(str)
    inventory_df["card_number"] = inventory_df["card_number"].astype(str)
    inventory_df["card_id"] = inventory_df["set_id"] + "-" + inventory_df["card_number"]
    return inventory_df


def update_portfolio(inventory_dir: str, lookup_dir: str, output_file: str) -> None:
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)

    if inventory_df.empty:
        print("[ERROR] Inventory is empty; writing empty portfolio with headers.", file=sys.stderr)
        cols = ["index","binder_name","page_number","slot_number","card_name","card_id","set_id","set_name","card_number","card_market_value"]
        pd.DataFrame(columns=cols).to_csv(output_file, index=False)
        return

    join_cols = ["card_id","card_name","set_id","set_name","card_number","card_market_value"]
    merged = pd.merge(inventory_df, lookup_df[join_cols], on="card_id", how="left", suffixes=("_inv",""))
    merged["card_market_value"] = merged["card_market_value"].fillna(0.0).astype(float)
    merged["set_name"] = merged["set_name"].fillna("NOT_FOUND")

    merged["index"] = (
        merged["binder_name"].astype(str) + "-" +
        merged["page_number"].astype(str) + "-" +
        merged["slot_number"].astype(str)
    )

    final_cols = ["index","binder_name","page_number","slot_number","card_name","card_id","set_id","set_name","card_number","card_market_value"]
    merged[final_cols].to_csv(output_file, index=False)
    print(f"[OK] Wrote portfolio -> {output_file}")


def main():
    update_portfolio("./card_inventory", "./card_set_lookup", "card_portfolio.csv")


def test():
    update_portfolio("./card_inventory_test", "./card_set_lookup_test", "test_card_portfolio.csv")


if __name__ == "__main__":
    print("[INFO] update_portfolio.py starting in Test Mode", file=sys.stderr)
    test() 
