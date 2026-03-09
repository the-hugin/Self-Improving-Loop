#!/usr/bin/env python3
"""Search the internet using a local SearXNG instance."""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import urllib.error


DEFAULT_URL = "http://localhost:8888"


def fetch_results(query, category, language, base_url):
    params = {
        "q": query,
        "format": "json",
        "categories": category,
        "language": language,
    }
    url = f"{base_url}/search?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Claude-Code-SearXNG-Skill/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(
            f"ERROR: Cannot connect to SearXNG at {base_url}: {e}",
            file=sys.stderr,
        )
        print(
            "Make sure SearXNG is running:\n"
            "  cd D:/Projects/searxng && docker compose up -d\n"
            "SearXNG runs on http://localhost:8888",
            file=sys.stderr,
        )
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON response from SearXNG: {e}", file=sys.stderr)
        print(
            "Make sure JSON format is enabled in settings.yml (search.formats: [html, json])",
            file=sys.stderr,
        )
        sys.exit(1)


def print_results(data, query, category, max_results):
    results = data.get("results", [])[:max_results]
    infoboxes = data.get("infoboxes", [])

    if not results and not infoboxes:
        print("No results found.")
        return

    print(f"## SearXNG — {query}")
    print(f"Category: {category} | Results: {len(results)}\n")

    # Print infobox if present (Wikipedia-style quick answer)
    if infoboxes:
        box = infoboxes[0]
        print(f"### Quick answer: {box.get('infobox', '')}")
        content = box.get("content", "").strip()
        if content:
            print(f"{content}\n")

    for i, result in enumerate(results, 1):
        title = result.get("title", "No title")
        url = result.get("url", "")
        content = result.get("content", "").strip()
        engines = ", ".join(result.get("engines", []))
        published_date = result.get("publishedDate", "")

        print(f"### {i}. {title}")
        print(f"URL: {url}")
        if published_date:
            print(f"Published: {published_date}")
        if engines:
            print(f"Sources: {engines}")
        if content:
            print(f"\n{content}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Search the internet using a local SearXNG instance"
    )
    parser.add_argument("query", help="Search query")
    parser.add_argument(
        "--category",
        choices=[
            "general",
            "news",
            "images",
            "videos",
            "science",
            "files",
            "it",
            "map",
            "music",
            "social media",
        ],
        default="general",
        help="Search category (default: general)",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=10,
        help="Maximum number of results (default: 10)",
    )
    parser.add_argument(
        "--language",
        default="all",
        help="Language code, e.g. en, ru, de (default: all)",
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help=f"SearXNG base URL (default: {DEFAULT_URL})",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output raw JSON instead of formatted text",
    )

    args = parser.parse_args()

    data = fetch_results(args.query, args.category, args.language, args.url)

    if args.json_output:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print_results(data, args.query, args.category, args.max_results)


if __name__ == "__main__":
    main()
