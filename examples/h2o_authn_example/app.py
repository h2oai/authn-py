import os

import h2o_authn
from h2o_wave import Q, app, ui
from h2o_wave import main


@app("/")
async def serve(q: Q):
    print(">" * 15, os.environ)  # XXX

    provider = h2o_authn.TokenProvider(
        issuer_url=os.getenv("H2O_WAVE_OIDC_PROVIDER_URL"),
        refresh_token=q.auth.refresh_token,
        client_id=os.getenv("H2O_WAVE_OIDC_CLIENT_ID"),
    )

    q.page["hello"] = ui.markdown_card(
        box="1 1 2 2", title="Hello World!", content=f"{provider()}"
    )

    await q.page.save()
