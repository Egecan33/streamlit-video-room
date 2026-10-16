import os, hashlib, random, string
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings

# ──────────────────────────────────────────────────────────────
#  CONFIG – edit once, then share only ?room=<room> with users
# ──────────────────────────────────────────────────────────────
DEFAULT_ROOM = "lobby"  # fallback room
ROOM_PASSWORD_ENV = "ROOM_PASS"  # env-var name
ICE_SERVERS = [{"urls": ["stun:stun.l.google.com:19302"]}]  # add TURN for prod


# ──────────────────────────────────────────────────────────────
#  Helpers
# ──────────────────────────────────────────────────────────────
def get_room_from_query():
    qp = st.query_params
    return qp.get("room", [DEFAULT_ROOM])[0]


def check_password(password_input: str) -> bool:
    """Compare the SHA-256 of the supplied password with env var."""
    stored = os.getenv(ROOM_PASSWORD_ENV)
    if not stored:
        return False
    return (
        hashlib.sha256(password_input.encode()).hexdigest()
        == hashlib.sha256(stored.encode()).hexdigest()
    )


def generate_invite(room: str) -> str:
    base = st.request.host_url.rstrip("/")
    return f"{base}/?room={room}"


# ──────────────────────────────────────────────────────────────
#  UI – step 1: join screen
# ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="🔒 Streamlit Video Room", layout="wide")
st.title("🔒 Password-protected Streamlit Video Room")

room = get_room_from_query()
st.write(f"**Room:** `{room}`  (share this link + the password)")

if "joined" not in st.session_state:
    st.session_state.joined = False

if not st.session_state.joined:
    pwd = st.text_input("Room password", type="password", on_change=lambda: None)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Join call") and check_password(pwd):
            st.session_state.joined = True
        elif st.button("Join call"):
            st.error("❌ Wrong password")
    with col2:
        if st.button("❓ Show invite link for this room"):
            st.code(generate_invite(room))
    st.stop()

# ──────────────────────────────────────────────────────────────
#  UI – step 2: the actual WebRTC streamer
# ──────────────────────────────────────────────────────────────
st.success("✅ You’re in!  Allow camera & mic when prompted.")
webrtc_streamer(
    key=f"webrtc-{room}",
    mode=WebRtcMode.SFU,  # multi-user SFU in Python server
    rtc_configuration={"iceServers": ICE_SERVERS},
    media_stream_constraints={"video": True, "audio": True},
    client_settings=ClientSettings(
        rtc_configuration={"iceServers": ICE_SERVERS},
        media_stream_constraints={"video": True, "audio": True},
    ),
)
