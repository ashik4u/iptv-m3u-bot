import requests

def fetch_m3u_links(m3u_url):
    """Download and parse M3U file, returning streaming links."""
    response = requests.get(m3u_url, timeout=10)
    response.raise_for_status()
    lines = response.text.splitlines()
    links = [line.strip() for line in lines if line.strip() and not line.startswith("#")]
    return links

def is_stream_working(url, timeout=10):
    """Attempt to HEAD or GET the stream, return True if it seems alive."""
    try:
        resp = requests.head(url, allow_redirects=True, timeout=timeout)
        if resp.status_code == 200:
            return True
        # Sometimes HEAD returns 405, so fallback to GET for a small byte range
        resp = requests.get(url, headers={'Range': 'bytes=0-1023'}, timeout=timeout, stream=True)
        return resp.status_code == 200 or resp.status_code == 206
    except Exception:
        return False

def check_multiple_m3us(m3u_urls):
    """Iterate through multiple M3U sources. Return {source: [working_links]}."""
    all_working = {}
    for m3u_url in m3u_urls:
        links = fetch_m3u_links(m3u_url)
        working_links = [link for link in links if is_stream_working(link)]
        all_working[m3u_url] = working_links
    return all_working

# Usage example:
if __name__ == "__main__":
    sources = [
        "http://example.com/playlist1.m3u",
        "http://example.com/playlist2.m3u"
    ]
    results = check_multiple_m3us(sources)
    for src, links in results.items():
        print(f"{src}:")
        for link in links:
            print("   ", link)