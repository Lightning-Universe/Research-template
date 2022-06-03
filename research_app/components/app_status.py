import dataclasses
from typing import List, Union

import streamlit as st
from lightning import LightningFlow, LightningWork
from lightning.frontend import StreamlitFrontend
from lightning.utilities.state import AppState
from streamlit_autorefresh import st_autorefresh


@dataclasses.dataclass()
class Status:
    components: List[Union[LightningWork, LightningFlow]]


status = Status([])


class AppStatus(LightningFlow):
    def __init__(self, components: List[Union[LightningWork, LightningFlow]]) -> None:
        super().__init__()
        self.all_ready: bool = False
        status.components = components

    def run(self) -> None:
        if self.all_ready:
            return
        for component in status.components:
            if not component.ready:
                return
        self.all_ready = True

    def configure_layout(self):
        return StreamlitFrontend(render_fn=render)


def render(state: AppState):
    st_autorefresh(interval=1000)

    if not state.all_ready:
        st.title("App status")
        st.write("Some components of this app is not ready yet! Please wait for sometime...")

        md = ""
        for component in status.components:
            print(f"{component} not ready!")
            if getattr(component, "ready") is False:
                md += f"* {component.name.capitalize()} ❌\n"

        st.markdown(md)

    else:
        st.title("All components ready!")
        st.write("This tab will close itself soon.")
