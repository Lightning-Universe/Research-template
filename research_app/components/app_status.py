import logging
from typing import Dict, List, Union

import streamlit as st
from lightning import LightningFlow, LightningWork
from lightning.app.frontend import StreamlitFrontend
from lightning.app.utilities.state import AppState
from rich.logging import RichHandler
from streamlit_autorefresh import st_autorefresh

FORMAT = "%(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

logger = logging.getLogger(__name__)


# This component is WIP @aniketmaurya
class AppStatus(LightningFlow):
    """This component shows the list of Works which are not ready."""

    def __init__(self, components: List[Union[LightningWork, LightningFlow]]) -> None:
        super().__init__()
        self.components: Dict[str, bool] = {}
        self.close = False
        for component in components:
            self.components[component.name] = getattr(component, "ready", None)

    @property
    def all_ready(self) -> bool:
        for name, ready in self.components.items():
            if ready is False:
                return False
        return True

    def run(self) -> None:
        if self.all_ready:
            self.close = self.all_ready
            return

        for component, ready in self.components.items():
            if not ready:
                return

    def configure_layout(self):
        return StreamlitFrontend(render_fn=render)


def render(state: AppState):
    st_autorefresh(interval=1000)

    if not state.close:
        st.title("App status")
        st.write("Some components of this app is not ready yet! Please wait for sometime...")

        md = ""
        for name, ready in state.components.item():
            logger.debug(f"{name} not ready!")
            if ready is False:
                md += f"* {name.capitalize()} ❌\n"

        st.markdown(md)

    else:
        st.title("All components ready!")
        st.write("This tab will close itself soon.")
