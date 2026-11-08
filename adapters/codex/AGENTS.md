# Cid workspace bootstrap

At session entry, explicitly read `.cid/COACH.md` and then `.cid/workspace.json`
from this workspace root before replying. Use the saved context to interpret short
coaching continuations such as “What next?” in a fresh conversation. Follow the
shared policy for game coaching and load only its relevant game/playthrough/topic
records. Apply existing instructions and personality preferences to other requests.
Markdown links do not import files: use the host's file tools to read them.
If the policy cannot be loaded, identify the setup problem instead of claiming Cid
is active. Preserve existing user instructions and personality preferences.
