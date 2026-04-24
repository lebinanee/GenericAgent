"""Web interaction tools for GenericAgent.

Provides a set of tools that allow the agent to interact with web pages
via the TMWebDriver session, including navigation, clicking, typing, and
reading page content.
"""

from __future__ import annotations

import time
from typing import Any

from TMWebDriver import Session


def navigate(session: Session, url: str) -> dict[str, Any]:
    """Navigate the browser to the given URL.

    Args:
        session: Active TMWebDriver session.
        url: Fully-qualified URL to load.

    Returns:
        dict with 'success' bool and current 'url' after navigation.
    """
    try:
        session.driver.get(url)
        time.sleep(1.0)  # allow page to begin loading
        return {"success": True, "url": session.driver.current_url}
    except Exception as exc:  # noqa: BLE001
        return {"success": False, "error": str(exc), "url": url}


def get_page_text(session: Session) -> dict[str, Any]:
    """Return the visible text content of the current page.

    Args:
        session: Active TMWebDriver session.

    Returns:
        dict with 'text' (str) and 'url' of the current page.
    """
    try:
        body = session.driver.find_element("tag name", "body")
        return {"text": body.text, "url": session.driver.current_url}
    except Exception as exc:  # noqa: BLE001
        return {"text": "", "error": str(exc), "url": session.driver.current_url}


def click_element(session: Session, selector: str, by: str = "css selector") -> dict[str, Any]:
    """Click a DOM element identified by *selector*.

    Args:
        session: Active TMWebDriver session.
        selector: Selector string (CSS selector by default).
        by: Selenium locator strategy, e.g. 'css selector', 'xpath', 'id'.

    Returns:
        dict with 'success' bool and optional 'error' message.
    """
    try:
        element = session.driver.find_element(by, selector)
        element.click()
        time.sleep(0.5)
        return {"success": True}
    except Exception as exc:  # noqa: BLE001
        return {"success": False, "error": str(exc)}


def type_text(
    session: Session, selector: str, text: str, by: str = "css selector", clear_first: bool = True
) -> dict[str, Any]:
    """Type *text* into an input element.

    Args:
        session: Active TMWebDriver session.
        selector: Selector string for the target input.
        text: Text to type.
        by: Selenium locator strategy.
        clear_first: Whether to clear existing content before typing.

    Returns:
        dict with 'success' bool and optional 'error' message.
    """
    try:
        element = session.driver.find_element(by, selector)
        if clear_first:
            element.clear()
        element.send_keys(text)
        return {"success": True}
    except Exception as exc:  # noqa: BLE001
        return {"success": False, "error": str(exc)}


def get_page_title(session: Session) -> dict[str, Any]:
    """Return the title of the current page.

    Args:
        session: Active TMWebDriver session.

    Returns:
        dict with 'title' (str) and 'url' of the current page.
    """
    try:
        return {"title": session.driver.title, "url": session.driver.current_url}
    except Exception as exc:  # noqa: BLE001
        return {"title": "", "error": str(exc), "url": ""}


def scroll_page(session: Session, direction: str = "down", amount: int = 500) -> dict[str, Any]:
    """Scroll the current page up or down by *amount* pixels.

    Args:
        session: Active TMWebDriver session.
        direction: 'up' or 'down'.
        amount: Number of pixels to scroll.

    Returns:
        dict with 'success' bool.
    """
    try:
        pixels = amount if direction == "down" else -amount
        session.driver.execute_script(f"window.scrollBy(0, {pixels});")
        time.sleep(0.3)
        return {"success": True}
    except Exception as exc:  # noqa: BLE001
        return {"success": False, "error": str(exc)}


# ---------------------------------------------------------------------------
# Tool registry — maps tool names to callables for use by agentmain.py
# ---------------------------------------------------------------------------

WEB_TOOLS: dict[str, Any] = {
    "navigate": navigate,
    "get_page_text": get_page_text,
    "click_element": click_element,
    "type_text": type_text,
    "get_page_title": get_page_title,
    "scroll_page": scroll_page,
}
