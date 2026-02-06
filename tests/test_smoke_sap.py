def test_smoke_sap(sap_session):
    # Smoke test básico: valida que la sesión esté autenticada
    current_url = sap_session.current_url.lower()

    # Validación genérica post-login (ajustable luego)
    assert "sap" in current_url, (
        f"URL inesperada luego del login: {sap_session.current_url}"
    )
