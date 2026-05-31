# IPTV Working Streams Combined M3U Bot

[![Check and Combine M3U Streams](https://github.com/ashik4u/iptv-m3u-bot/actions/workflows/check-and-combine.yml/badge.svg)](https://github.com/ashik4u/iptv-m3u-bot/actions/workflows/check-and-combine.yml)

This bot fetches multiple IPTV M3U playlists, checks each video stream for availability, and combines all working streams into a single `.m3u` file. It automatically validates that streams are actually working before including them in the output.

## 📺 Live Playlist URL

```
https://raw.githubusercontent.com/ashik4u/iptv-m3u-bot/refs/heads/main/output/all.m3u
```

The `all.m3u` file is automatically updated every 15 minutes with only working streams.

## How It Works

1. **Fetches playlists** from multiple M3U sources defined in `data/feed.txt`
2. **Validates each stream** by checking if it responds to HTTP requests (with a 10-second timeout per stream)
3. **Combines working streams** from all sources into a single M3U file
4. **Removes duplicates** and sorts alphabetically by channel name
5. **Automatically updates** via GitHub Actions every 15 minutes

## Features

- ✅ Fetches and parses multiple M3U playlist files
- ✅ Validates each stream's availability (concurrent checking for speed)
- ✅ Produces a single combined M3U file (`all.m3u`) with only working streams
- ✅ Removes duplicate streams
- ✅ Automatically updates every 15 minutes via GitHub Actions
- ✅ Supports custom playlist entries that bypass availability checks

## Usage

### Local Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up data files** (if not already configured)
   - Create `data/feed.txt` with M3U playlist URLs (one per line)
   - Optionally create `data/custom_entries.txt` for custom stream entries

3. **Run the script**
   ```bash
   python scripts/m3u_working_streams_combined.py
   ```

4. Your combined working streams will be in `output/all.m3u`

### Automated Updates (GitHub Actions)

The workflow automatically runs every 15 minutes and:
1. Pulls playlist sources from GitHub Secrets (`FEED_TXT` and `CUSTOM_ENTRIES_TXT`)
2. Validates all streams
3. Combines working streams into `output/all.m3u`
4. Commits and pushes changes automatically

**Note:** Data files are populated from GitHub Secrets during workflow execution, not stored in the repository for privacy.

## Configuration

### Setting Up Your Repository

1. **Add GitHub Secrets** in your repository settings (`Settings` → `Secrets and variables` → `Actions`):
   - `FEED_TXT`: Your M3U playlist URLs (one per line)
   - `CUSTOM_ENTRIES_TXT`: (Optional) Custom M3U entries to include without validation

   Example `FEED_TXT`:
   ```
   https://example.com/playlist1.m3u
   https://example.com/playlist2.m3u
   ```

2. **Customize the script** (optional):
   - Adjust `max_workers` in `check_streams()` to change concurrency (default: 10)
   - Adjust `timeout` parameters for stream checking (default: 10 seconds per stream)

## Data Files

- **`data/feed.txt`**: List of M3U playlist URLs to fetch (created from `FEED_TXT` secret during workflow)
- **`data/custom_entries.txt`**: (Optional) Pre-configured streams to include without availability checks (created from `CUSTOM_ENTRIES_TXT` secret)
- **`output/all.m3u`**: The final combined M3U file with only working streams

## License

MIT
