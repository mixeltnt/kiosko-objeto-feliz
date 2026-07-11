import requests

class ApiTiempo:
    @staticmethod
    def obtener_clima_santiago():
        """
        Obtiene clima actual de Santiago (Chile) desde API pública.
        Retorna un diccionario con datos relevantes.
        """
        # Coordenadas de Santiago
        lat = -33.45
        lon = -70.66

        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&current_weather=true"
        )

        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()

        clima = data.get("current_weather")
        if not clima:
            raise RuntimeError("No se pudo obtener el clima desde la API.")

        return {
            "temperatura": clima["temperature"],
            "viento": clima["windspeed"],
            "direccion_viento": clima["winddirection"],
            "hora": clima["time"]
        }
