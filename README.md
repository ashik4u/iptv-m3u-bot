# IPTV Working Streams Combined M3U Bot

This bot fetches multiple IPTV M3U playlists, checks each video stream for availability, and combines all working streams into a single `.m3u` file.

## Features

- Fetches and parses several M3U playlist files
- Checks each stream for availability
- Produces one combined M3U (`combined_working_streams.m3u`) with working streams only
- Automated update via GitHub Actions (fetches + generates daily)

## Usage

### Local

1. **Install dependencies**
    ```
    pip install -r requirements.txt
    ```

2. **Run the script**
    ```
    python m3u_working_streams_combined.py
    ```

3. Your working streams will be in `combined_working_streams.m3u`.

### Automated Workflow

A GitHub Actions workflow runs daily and/or on repository push to regenerate and commit `combined_working_streams.m3u`.

## Customization

- To check different playlists, modify the `M3U_URLS` list at the top of `m3u_working_streams_combined.py`.
- To adjust concurrency or request timeouts, modify respective params in the script.

## License

MIT