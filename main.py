from __future__ import annotations

import api_md  # Import the provided api_md.py

try:
    import httpx
except ImportError:
    raise ImportError("Please install httpx with 'pip install httpx' ")

from textual import events, work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Input, Markdown


class MarkdownAPIApp(App):
    """Fetches markdown data from API as-you-type."""

    CSS_PATH = "main.css"

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter a query", id="query_input")
        with VerticalScroll(id="results-container"):
            yield Markdown(id="results")

    def on_mount(self) -> None:
        """Called when app starts."""
        # Give the input focus, so we can start typing straight away
        self.query_one(Input).focus()

    async def on_key(self, event: events.Key) -> None:
        """Trigger fetching data when the Enter key is pressed"""
        if event.key == 'enter':
            input_widget = self.query_one("#query_input", Input)
            query = input_widget.value
            self.fetch_data(query)

    @work(exclusive=True)
    async def fetch_data(self, query: str) -> None:
        """Fetches data."""
        # Here we call the function from api_md.py
        data = api_md.get_markdown(query)

        if query == self.query_one("#query_input", Input).value:
            self.query_one("#results", Markdown).update(data)


if __name__ == "__main__":
    app = MarkdownAPIApp()
    app.run()
