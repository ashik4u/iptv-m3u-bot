import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def load_m3u_urls(feed_file="feed.txt"):
    """Load M3U URLs from feed.txt file."""
    try:
        with open(feed_file, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        return urls
    except Exception as ex:
        print(f"Error reading {feed_file}: {ex}")
        return []

def extract_channel_name(extinf_line):
    """Extract channel name from EXTINF line."""
    if not extinf_line:
        return ""
    # Extract text after the last comma
    parts = extinf_line.split(',', 1)
    if len(parts) > 1:
        return parts[1].strip()
    return ""

def fetch_m3u_links(m3u_url):
    try:
        resp = requests.get(m3u_url, timeout=15)
        resp.raise_for_status()
        lines = resp.text.splitlines()
        entries = []
        current_extinf = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#EXTINF"):
                current_extinf = line
            elif not line.startswith("#"):
                entries.append((current_extinf, line))
                current_extinf = None
        return entries
    except Exception as ex:
        print(f"  Error fetching {m3u_url}: {ex}")
        return []

def is_stream_working(url, timeout=10):
    try:
        resp = requests.head(url, allow_redirects=True, timeout=timeout)
        if resp.status_code == 200:
            return True
        resp = requests.get(url, headers={'Range': 'bytes=0-1023'}, timeout=timeout, stream=True)
        return resp.status_code in (200, 206)
    except Exception:
        return False

def check_streams(entries):
    working_entries = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_entry = {executor.submit(is_stream_working, url): (extinf, url) for extinf, url in entries}
        for future in as_completed(future_to_entry):
            extinf, url = future_to_entry[future]
            try:
                if future.result():
                    working_entries.append((extinf, url))
            except Exception:
                pass
    return working_entries

if __name__ == "__main__":
    M3U_URLS = load_m3u_urls()
    if not M3U_URLS:
        print("No URLs found in feed.txt")
        exit(1)
    
    combined_entries = []
    for m3u_url in M3U_URLS:
        print(f"\n----- Checking {m3u_url} -----")
        entries = fetch_m3u_links(m3u_url)
        if not entries:
            print(f"No streams found in {m3u_url}")
            continue
        print(f"  Found {len(entries)} possible streams. Checking working links...")
        working = check_streams(entries)
        print(f"  {len(working)} working links found.")
        combined_entries.extend(working)

    # Remove duplicates based on URL
    seen_urls = set()
    unique_entries = []
    for extinf, url in combined_entries:
        if url not in seen_urls:
            seen_urls.add(url)
            channel_name = extract_channel_name(extinf) or url
            unique_entries.append((extinf, url, channel_name))
    
    # Sort entries alphabetically by channel name
    unique_entries.sort(key=lambda x: x[2].lower())
    
    print(f"\nTotal unique working streams: {len(unique_entries)} (removed {len(combined_entries) - len(unique_entries)} duplicates)")

    # Combine and write to output M3U with single group
    output_file = "combined_working_streams.m3u"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for extinf, url, channel_name in unique_entries:
            if extinf:
                # Add group-title to existing EXTINF line
                if 'group-title=' not in extinf:
                    extinf = extinf.replace('#EXTINF:', '#EXTINF:').replace(',', ' group-title="All Channels",', 1)
                f.write(f"{extinf}\n")
            else:
                f.write(f'#EXTINF:-1 group-title="All Channels",{channel_name}\n')
            f.write(f"{url}\n")
    print(f"Combined working streams saved to {output_file}")