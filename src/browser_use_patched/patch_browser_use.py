# patch_browser_use.py
import asyncio
import json
import logging
import os
from os import makedirs

from browser_use import Browser as OriginalBrowser
from browser_use.actor.page import Page as OriginalPage
from browser_use.dom.serializer.serializer import DOMTreeSerializer
from browser_use.dom.views import SerializedDOMState
from dotenv import load_dotenv

from .utils.formatting import format_browser_state_for_llm

load_dotenv()
DATA_DIR = os.getenv("DATA_DIR", "./data")
makedirs(DATA_DIR, exist_ok=True)

class Page(OriginalPage):
    async def _get_doom_representation(self) -> SerializedDOMState:
        dom_service = self.dom_service

        enhanced_dom_tree = await dom_service.get_dom_tree(target_id=self._target_id)

        serialized_dom_state, _ = DOMTreeSerializer(
            enhanced_dom_tree, None, paint_order_filtering=True
        ).serialize_accessible_elements()

        return serialized_dom_state
    
    async def get_llm_dom_representation(self) -> str:
        """Returns the LLM representation of the DOM.

        Returns:
            str: The LLM representation of the DOM.
        """
        serialized_dom_state = await self._get_doom_representation()
        return serialized_dom_state.llm_representation()
    
    async def get_evaluation_dom_representation(self) -> str:
        """Returns the evaluation representation of the DOM.
        Returns:
            str: The evaluation representation of the DOM.
        """
        serialized_dom_state = await self._get_doom_representation()
        return serialized_dom_state.eval_representation()

    async def wait_until_fully_loaded(self, max_wait_time: int = 10, min_wait_time: int = 2):
        """Wait until the page is fully loaded by checking document.readyState.

        Args:
            max_wait_time (int, optional): Maximum time to wait for the page to load. Defaults to 10.
            min_wait_time (int, optional): Minimum time to wait before checking the load state. Defaults to 2.

        Returns:
            bool: True if the page is fully loaded, otherwise False.
        """
        wait_time = 0
        state = ""
        await asyncio.sleep(min_wait_time)
        
        while (wait_time + min_wait_time) < max_wait_time and state != "complete":
            state = await self.evaluate("() => document.readyState")
            wait_time += 1
            await asyncio.sleep(1)
        return state == "complete"
    
    async def push_data(self, data: dict):
        """Push data to a JSON file specific to this page.

        Args:
            data (dict): Data to be pushed to the JSON file.
        """
        file_path = os.path.join(DATA_DIR, f"page_data_{self._target_id}.json")
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = []
        
        existing_data.append(data)
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)

        logging.info(f"Data pushed to {file_path}")
        
class Browser(OriginalBrowser):
    async def new_page(self, url: str | None = None) -> Page:
        """Creates a new page in the browser.

        Args:
            url (str | None, optional): The URL to navigate to. Defaults to None.

        Returns:
            Page: The newly created page.
        """
        page = await super().new_page(url)
        return Page(browser_session=self, target_id=page._target_id)
    
    async def get_current_page(self) -> Page | None:
        """Gets the current page of an actor.

        Returns:
            Page | None: The current page or None if no page is open.
        """
        page = await super().get_current_page()
        if page is not None:
            return Page(browser_session=self, target_id=page._target_id)
        
    async def format_browser_state_for_llm(self) -> str:
        """Formats the browser state summary for LLM consumption in code-use mode.
        """
        
        state = await self.get_browser_state_summary(include_screenshot=False)
           
        return await format_browser_state_for_llm(
            state=state, browser_session=self
        )
