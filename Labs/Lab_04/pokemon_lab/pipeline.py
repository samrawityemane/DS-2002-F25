import sys
import update_portfolio
import generate_summary

def run_production_pipeline():
    print("[START] Production pipeline", file=sys.stderr)
    print("[STEP] Update portfolio", file=sys.stderr)
    update_portfolio.main()
    print("[STEP] Generate summary", file=sys.stderr)
    generate_summary.main()
    print("[DONE] Production pipeline", file=sys.stderr)

if __name__ == "__main__":
    run_production_pipeline()
