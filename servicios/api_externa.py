import requests

class ApiExterna:
    @staticmethod
    def obtener_tipo_cambio_usd_a_clp() -> float:
        """
        Consulta una API pública y devuelve el tipo de cambio USD -> CLP.
        Valida la respuesta JSON para evitar KeyError ('rates').
        """
        url = "https://open.er-api.com/v6/latest/USD"
        r = requests.get(url, timeout=10)
        r.raise_for_status()

        data = r.json()

        # Validación del formato esperado
        rates = data.get("rates")
        if not isinstance(rates, dict) or "CLP" not in rates:
            raise RuntimeError(f"Respuesta inesperada de la API (no viene 'rates/CLP'): {data}")

        return float(rates["CLP"])
