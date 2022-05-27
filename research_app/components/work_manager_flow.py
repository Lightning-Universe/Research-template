from dataclasses import dataclass
from typing import ClassVar, Generator, Optional, Type

import streamlit as st
from lightning import LightningFlow, LightningWork
from lightning.frontend import StreamlitFrontend
from lightning.utilities.state import AppState
from streamlit_autorefresh import st_autorefresh


@dataclass
class ManagedWork:
    ALL_NAMES: ClassVar = "all_names"

    work: LightningWork
    name: str
    extra_url: Optional[str] = ""

    def set_to_instance(self, inst: LightningFlow) -> None:
        setattr(inst, self.name, self.work)
        setattr(inst, self.name + "_url", self.extra_url)
        setattr(inst, self.ALL_NAMES, getattr(inst, self.ALL_NAMES, list()) + [self.name])

    @classmethod
    def get_from_instance(cls, inst: LightningFlow, name: str) -> "ManagedWork":
        if name not in getattr(inst, cls.ALL_NAMES, list()):
            raise ValueError(f"Sorry, but your instance {inst} does not have a work referenced by name {name}")

        work = getattr(inst, name)
        extra_url = getattr(inst, name + "_url")

        return cls(work, name, extra_url)

    @classmethod
    def get_all_from_instance(cls: Type["ManagedWork"], inst: LightningFlow) -> Generator["ManagedWork", None, None]:
        for name in getattr(inst, cls.ALL_NAMES, list()):
            yield cls.get_from_instance(inst, name)


class WorkManagerFlow(LightningFlow):
    def __init__(self, *works: ManagedWork) -> None:
        super().__init__()
        for work in works:
            work.set_to_instance(self)
        self.all_ready: bool = False

    def run(self) -> None:
        all_ready = True
        for work in ManagedWork.get_all_from_instance(self):
            work.work.run()
            all_ready &= work.work.ready

        self.all_ready = all_ready

    def configure_layout(self):
        return StreamlitFrontend(render_fn=render)


def render(state: AppState):
    st_autorefresh(interval=1000)

    if not state.all_ready:
        st.title("Not ready yet")
        st.write("These components are not ready yet and will appear soon:")

        md = ""
        for name in state.all_names:
            work: LightningWork = getattr(state, name)
            if not work.ready:
                md += f"* {name.capitalize()}\n"

        st.markdown(md)

    else:
        st.title("All components ready!")
        st.write("This tab will close itself soon.")
