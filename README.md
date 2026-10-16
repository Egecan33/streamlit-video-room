# Streamlit Video Room — Prototype Review Draft

A Streamlit/WebRTC experiment with room query parameters, a password gate and invite-link generation. This is an unfinished prototype; a working multi-user calling architecture has not been verified.

The local authentication draft requires an explicitly configured, nonempty `ROOM_PASS` environment variable and rejects access when it is absent. There is no default shared password. Isolated guard tests cover missing, empty, correct and incorrect passwords; the application has not been deployed or tested with browsers/cameras.

## Open issues before a demo

The repository has no dependency manifest. `WebRtcMode.SFU`, `ClientSettings` and `st.request.host_url` must be checked against supported package APIs; do not assume the current code starts successfully. The join screen creates two buttons with the same label, and room query parsing assumes an older query-parameter return shape. TURN, HTTPS, room isolation, session expiration and multi-user signaling have not been validated.

Resolve the dependency/API and session behavior issues before publishing setup commands or promoting this as a functioning calling service. No project-wide license is declared.
