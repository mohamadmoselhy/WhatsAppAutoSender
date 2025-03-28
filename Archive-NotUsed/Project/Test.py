
async def type_text(page, element_type, element_value, text):
    """Types text into the specified element based on the provided selector type."""
    try:
        # Determine the correct selector format
        selector = ""
        if element_type.lower() == "class":
            selector = f".{element_value}"  # Class selector (e.g., ".input-field")
        elif element_type.lower() == "id":
            selector = f"#{element_value}"  # ID selector (e.g., "#username")
        elif element_type.lower() == "css":
            selector = element_value  # Direct CSS selector (e.g., "input[name='email']")
        else:
            raise ValueError("Invalid selector type. Use 'class', 'id', or 'css'.")

        await page.waitForSelector(selector, timeout=5000)  # Ensure element is loaded
        await page.type(selector, text)  # Type the text
        print(f"Typed text into element: {selector}")
    except Exception as e:
        print(f"Error typing text ({element_type}: {element_value}): {e}")


type_text()