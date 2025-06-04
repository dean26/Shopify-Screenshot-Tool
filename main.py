import os
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def get_domain(url):
    return urlparse(url).netloc.replace('.', '_')


def log(text_widget, message):
    text_widget.insert(tk.END, message + "\n")
    text_widget.see(tk.END)  # Scroll to bottom


def save_screenshot(page, url, name, path, log_widget):
    try:
        log(log_widget, f"Loading: {url}")
        page.goto(url, wait_until="load", timeout=90000)
        log(log_widget, f"Loaded successfully: {url}")
        screenshot_path = os.path.join(path, name)
        page.screenshot(path=screenshot_path, full_page=True)
        log(log_widget, f"Screenshot saved: {screenshot_path}")
    except PlaywrightTimeoutError:
        log(log_widget, f"[{url}] Timeout while loading the page.")
    except Exception as e:
        log(log_widget, f"[{url}] Error: {str(e)}")


def run_screenshots(urls_raw, log_widget, progress_bar):
    log_widget.delete(1.0, tk.END)  # Clear previous logs
    urls = [url.strip() for url in urls_raw.splitlines() if url.strip()]
    if not urls:
        messagebox.showerror("Input Error", "Please enter at least one Shopify store URL.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_root = Path("screenshots") / timestamp
    output_root.mkdir(parents=True, exist_ok=True)

    progress_bar["maximum"] = len(urls)
    progress_bar["value"] = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        for index, url in enumerate(urls, start=1):
            try:
                domain = get_domain(url)
                output_dir = output_root / domain
                output_dir.mkdir(parents=True, exist_ok=True)
                log(log_widget, f"Processing store: {domain}")

                save_screenshot(page, url, "homepage.png", output_dir, log_widget)

                # Category
                page.goto(url, timeout=60000)
                category_link = page.query_selector('a[href*="/collections/"]')
                if category_link:
                    category_url = category_link.get_attribute('href')
                    if not category_url.startswith("http"):
                        category_url = url.rstrip("/") + category_url
                    save_screenshot(page, category_url, "category.png", output_dir, log_widget)

                    # Product
                    page.goto(category_url, timeout=60000)
                    product_link = page.query_selector('a[href*="/products/"]')
                    if product_link:
                        product_url = product_link.get_attribute('href')
                        if not product_url.startswith("http"):
                            product_url = url.rstrip("/") + product_url
                        save_screenshot(page, product_url, "product.png", output_dir, log_widget)
                    else:
                        log(log_widget, f"[{domain}] No product link found.")
                else:
                    log(log_widget, f"[{domain}] No category link found.")
            except Exception as e:
                log(log_widget, f"[{url}] Unexpected Error: {str(e)}")
            finally:
                progress_bar["value"] = index
                progress_bar.update()

        browser.close()

    messagebox.showinfo("Done", f"All screenshots saved in '{output_root}'.")


def start_gui():
    window = tk.Tk()
    window.title("Shopify Screenshot Tool")
    window.geometry("700x650")

    tk.Label(window, text="Paste Shopify store URLs (one per line):").pack(pady=(10, 5))

    url_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=12)
    url_text.pack(padx=10)

    progress_bar = ttk.Progressbar(window, orient="horizontal", length=600, mode="determinate")
    progress_bar.pack(pady=10)

    log_label = tk.Label(window, text="Log:")
    log_label.pack()

    log_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=15, bg="#111", fg="#0f0")
    log_text.pack(padx=10, pady=(0, 10))

    run_button = tk.Button(
        window,
        text="Start Screenshots",
        command=lambda: run_screenshots(url_text.get("1.0", tk.END), log_text, progress_bar)
    )
    run_button.pack(pady=(5, 10))

    window.mainloop()


if __name__ == "__main__":
    start_gui()
