import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

M3U_URLS = [
    "https://raw.githubusercontent.com/doms9/iptv/refs/heads/default/M3U8/events.m3u8",
    "https://raw.githubusercontent.com/IPTVFlixBD/Fancode-BD/refs/heads/main/playlist.m3u",
    "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/main/playlist.m3u",
    "https://raw.githubusercontent.com/a1xmedia/m3u/refs/heads/main/a1x.m3u"
]

def fetch_m3u_links(m3u_url):
    """Download and parse M3U file, returning streaming links."""
    print(f"Fetching playlist: {m3u_url}")
    try:
        resp = requests.get(m3u_url, timeout=15)
        resp.raise_for_status()
        lines = resp.text.splitlines()
        # filter non-empty lines that don't begin with '#'
        links = [line.strip() for line in lines if line.strip() and not line.startswith("#")]
        print(f"  Found {len(links)} possible streams.")
        return links
    except Exception as ex:
        print(f"  Error fetching {m3u_url}: {ex}")
        return []

def is_stream_working(url, timeout=10):
    """Try HEAD, fall back to a small GET. Returns True if stream responds."""
    try:
        resp = requests.head(url, allow_redirects=True, timeout=timeout)
        if resp.status_code == 200:
            return True
        # Fallback for servers that don't support HEAD
        resp = requests.get(url, headers={'Range': 'bytes=0-1023'}, timeout=timeout, stream=True)
        return resp.status_code in (200, 206)
    except Exception:
        return False

def check_streams(links):
    """Check all streams in parallel and return only working ones."""
    working = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(is_stream_working, url): url for url in links}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                if future.result():
                    working.append(url)
            except Exception:
                pass  # Ignore any unexpected error for individual streams
    return working

if __name__ == "__main__":
    for m3u_url in M3U_URLS:
        links = fetch_m3u_links(m3u_url)
        if not links:
            print(f"No streams found in {m3u_url}")
            continue
        print("  Checking which links are working. This may take a while...")
        working_links = check_streams(links)
        if working_links:
            print(f"\nWorking streams in {m3u_url}:")
            for link in working_links:
                print(link)
        else:
            print(f"No working streams found in {m3u_url}.")
        print("\n" + "-"*50 + "\n")