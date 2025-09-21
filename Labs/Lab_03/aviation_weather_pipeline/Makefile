
.PHONY: all fetch analyze clean
.DEFAULT_GOAL := analyze

fetch:
	@echo "[fetch] Starting…"
	./fetch_metars.sh
	@echo "[fetch] Raw JSON saved to ./raw_metars"

analyze: fetch
	@echo "[analyze] Starting…"
	./analyze_data.sh
	@echo "[analyze] CSV written to ./weather_report.csv"
	@echo "[pipeline] Done ✔"

clean:
	@echo "[clean] Removing outputs…"
	rm -rf raw_metars weather_report.csv
	@echo "[clean] Done."
