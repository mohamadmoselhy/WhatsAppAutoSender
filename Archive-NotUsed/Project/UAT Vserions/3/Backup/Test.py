import asyncio
from pyppeteer import launch

async def open_whatsapp_web():
    """Launches the browser and opens WhatsApp Web."""
    browser = await launch(
        executablePath="C:/Program Files/Google/Chrome/Application/chrome.exe",  # Adjust for your OS
        headless=False
    )
    page = await browser.newPage()
    await page.goto("https://web.whatsapp.com/")
    
    print("Please scan the QR code to log in...")
    await page.waitForSelector(".selectable-text.copyable-text", timeout=60000)  # Wait for login
    
    return browser, page  # Return browser and page object for further use

async def click_selector(page, element_type, element_value):
    """Clicks on the specified element based on the provided selector type."""
    try:
        # Determine the correct selector format
        selector = ""
        if element_type == "class":
            selector = f".{element_value}"  # Class selector (e.g., ".button")
        elif element_type == "id":
            selector = f"#{element_value}"  # ID selector (e.g., "#submit")
        elif element_type == "css":
            selector = element_value  # Direct CSS selector (e.g., "button.submit")
        else:
            raise ValueError("Invalid selector type. Use 'class', 'id', or 'css'.")

        await page.waitForSelector(selector, timeout=5000)  # Ensure element is loaded
        await page.click(selector)  # Click the element
        print(f"Clicked on element: {selector}")
    except Exception as e:
        print(f"Error clicking element ({element_type}: {element_value}): {e}")

async def main():
    browser, page = await open_whatsapp_web()
    
    # Example usage:
    await click_selector(page, "class", "selectable-text copyable-text")  # Click input field
    await click_selector(page, "css", "button.submit")  # Click submit button
    
    await browser.close()

asyncio.run(main())
