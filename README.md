# Shopify Screenshot Tool

A simple Python GUI tool to automatically take full-page screenshots of Shopify store pages — homepage, first category, and first product page.

## Features

- User-friendly GUI (Tkinter)
- Automatically:
  - Captures the homepage of each store
  - Captures the first collection (category) page
  - Captures the first product page from the category
- Saves screenshots in structured folders under `screenshots/`
- Real-time logging and progress bar

## Requirements

- Python 3.8 or higher
- [Playwright for Python](https://playwright.dev/python/)
- Tkinter (usually included with Python)

## Installation

1. Download the script or clone the repository.
2. Open terminal and run:

```bash
pip install playwright
playwright install
```

## Usage

1. Run the app:

```bash
python main.py
```

2. Paste Shopify store URLs (one per line).
3. Click **Start Screenshots**.
4. Screenshots will be saved in the `screenshots/YYYY-MM-DD_HH-MM-SS/` folder.

## Example Folder Structure

```
screenshots/
└── 2025-06-04_09-23-11/
    ├── mystore_com/
    │   ├── homepage.png
    │   ├── category.png
    │   └── product.png
    └── anotherstore_com/
        ├── homepage.png
        └── category.png  # if no product found
```

## Notes

- If no category or product page is found, it logs a message.
- All screenshots are full-page.
- Errors are shown in the log window in real time.

## License

MIT License – use freely and modify as needed.
