# Path Gross Flashcards

An Anki-style gross pathology review site built from the gross specimen PDF.

## Features

- Mobile-first review flow with swipe gestures
- Desktop controls with keyboard shortcuts
- Extracted embedded specimen images instead of page screenshots
- Pages with two specimen photos show both images on the same card
- System filters and progress pools
- Local progress saved in browser storage
- Optional top and bottom label-cover toggle

## Controls

- Tap card or press `Space` to reveal the diagnosis
- Swipe right or press `Right Arrow` to mark familiar
- Swipe left or press `Left Arrow` to mark unfamiliar
- Press `R` to reshuffle the current deck

## Build Cards

From the repo root:

```powershell
python .\tools\build_cards.py
```

This generates:

- `cards.js`
- `assets/cards/*.jpg`

## Local Preview

```powershell
python -m http.server 8000
```

Then open `http://localhost:8000`.

## Deploy

Push this repo to GitHub and enable GitHub Pages from the default branch root.
