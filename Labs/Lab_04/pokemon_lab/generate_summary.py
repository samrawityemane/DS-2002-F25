import os, sys
import pandas as pd

def generate_summary(portfolio_file):
    if not os.path.exists(portfolio_file):
        print(f"[ERROR] Missing portfolio file: {portfolio_file}", file=sys.stderr)
        sys.exit(1)
    df = pd.read_csv(portfolio_file)
    if df.empty:
        print("[INFO] Portfolio is empty. Nothing to summarize.")
        return
    total_portfolio_value = df["card_market_value"].sum()
    idx = df["card_market_value"].idxmax()
    most_valuable_card = df.loc[idx]
    print(f"Total Portfolio Value: ${total_portfolio_value:,.2f}")
    print("Most Valuable Card:")
    print(f"  Name: {most_valuable_card.get('card_name','UNKNOWN')}")
    print(f"  ID:   {most_valuable_card.get('card_id','UNKNOWN')}")
    print(f"  Value: ${most_valuable_card.get('card_market_value',0.0):,.2f}")

def main():
    generate_summary("card_portfolio.csv")

def test():
    generate_summary("test_card_portfolio.csv")

if __name__ == "__main__":
    test()
