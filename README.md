# Trip Forecast Board

A single-page trip weather board. Enter each city and the dates you'll be there;
every stop is matched to its own daily forecast, and any date past the 16-day
model horizon falls back to a ten-year climate normal for that spot on the
calendar.

- **No API key, no build step, no backend** — one HTML file plus icons.
- Data from [Open-Meteo](https://open-meteo.com) (CC BY 4.0): forecast,
  geocoding, and the ERA5 archive for normals.
- Metric is fetched and converted in-page, so the °F/°C switch costs no requests.
- Itinerary and computed normals persist in `localStorage`; export/import as JSON.

## Run locally

```
python serve.py 10000
```

`serve.py` exists only to send `Cache-Control: no-store` — plain
`python -m http.server` lets browsers serve a stale page after an edit.

## Notes

Climate normals are the mean of every observed day within ±3 days of the target
date across the last ten years. They describe what a place is usually like, not
what the weather will do, and are marked with a blue rail rather than presented
as a forecast.

Open-Meteo prices a request by span: anything over 14 days for one location
counts as several API calls. Normals are therefore fetched as one short window
per sampled year (10 calls) rather than one continuous decade (~261 calls).
