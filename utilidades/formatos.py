def dinero_clp(valor: float) -> str:
    try:
        return f"$ {valor:,.0f}".replace(",", ".")
    except Exception:
        return str(valor)
