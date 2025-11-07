import argparse
import yaml
import os

from src .scraper import scrape_project

def main():
    parser = argparse.ArgumentParser(description="Apache Jira scraper -> JSONL pipeline")
    parser.add_argument("--config", default="config.yaml", help="Path to YAML config")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    projects = cfg.get("projects", [])
    output_dir = cfg.get("output_dir", "data")
    page_size = int(cfg.get("page_size", 100))
    retry_conf = cfg.get("retry", {})

    os.makedirs(output_dir, exist_ok=True)

    for pj in projects:
        scrape_project(pj, output_dir=output_dir, page_size=page_size, retry_conf=retry_conf)

if __name__ == "__main__":
    main()
