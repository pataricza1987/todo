import os
from datetime import datetime

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")

st.set_page_config(page_title="Todo", layout="centered")
st.title("TODO")
st.caption(f"Backend: {BACKEND_URL}")


def api_get(path: str):
    r = requests.get(f"{BACKEND_URL}{path}", timeout=10)
    r.raise_for_status()
    return r.json()


def api_post(path: str, body: dict):
    r = requests.post(f"{BACKEND_URL}{path}", json=body, timeout=10)
    r.raise_for_status()
    return r.json()


def api_patch(path: str, body: dict):
    r = requests.patch(f"{BACKEND_URL}{path}", json=body, timeout=10)
    r.raise_for_status()
    return r.json()


def api_delete(path: str):
    r = requests.delete(f"{BACKEND_URL}{path}", timeout=10)
    if r.status_code not in (200, 204):
        r.raise_for_status()
    return None


with st.sidebar:
    st.header("Szűrők")
    filter_mode = st.radio("Mutasd", options=["Minden", "Nyitott", "Kész"], index=0)
    only_open = None
    if filter_mode == "Nyitott":
        only_open = True
    elif filter_mode == "Kész":
        only_open = False

    st.divider()
    st.header("Új TODO")
    new_title = st.text_input("Cím")
    new_desc = st.text_area("Leírás", height=80)
    new_priority = st.slider("Prioritás (1=high, 5=low)", 1, 5, 3)
    new_due = st.date_input("Határidő (opcionális)", value=None)

    if st.button("Mentés", use_container_width=True, type="primary"):
        if not new_title.strip():
            st.error("A cím kötelező")
        else:
            due_dt = None
            if new_due:
                due_dt = datetime.combine(new_due, datetime.min.time()).isoformat()
            api_post(
                "/todos",
                {
                    "title": new_title.strip(),
                    "description": new_desc.strip() or None,
                    "priority": int(new_priority),
                    "due_date": due_dt,
                },
            )
            st.success("Feladat létrehozva")
            st.rerun()


try:
    params = "" if only_open is None else f"?only_open={str(only_open).lower()}"
    todos = api_get(f"/todos{params}")
except Exception as e:
    st.error(f"Nem érem el a backendet: {e}")
    st.stop()

st.subheader("Feladatok")

for t in todos:
    with st.container(border=True):
        top = st.columns([0.08, 0.62, 0.30])
        done = top[0].checkbox(
            "Kész",
            value=bool(t.get("done")),
            key=f"done_{t['id']}",
            label_visibility="collapsed",
        )
        title = t.get("title", "")
        prio = t.get("priority", 3)
        due = t.get("due_date")
        top[1].markdown(f"**{title}**  ·  priority: `{prio}`")
        top[2].caption(f"due: {due}" if due else "")

        if done != bool(t.get("done")):
            api_patch(f"/todos/{t['id']}", {"done": done})
            st.rerun()

        desc = t.get("description")
        if desc:
            st.write(desc)

        quote = t.get("last_quote")
        c1, c2 = st.columns([0.7, 0.3])
        if quote:
            c1.info(quote)
        if c2.button("Motiváció", key=f"enrich_{t['id']}"):
            api_post(f"/todos/{t['id']}/enrich", {})
            st.rerun()

        if st.button("Törlés", key=f"del_{t['id']}"):
            api_delete(f"/todos/{t['id']}")
            st.rerun()
