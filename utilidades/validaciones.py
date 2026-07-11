import re

def validar_correo(email: str) -> bool:
    if not email:
        return False
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(patron, email) is not None

def limpiar_rut(rut: str) -> str:
    return rut.replace(".", "").replace("-", "").strip().upper()

def validar_rut(rut: str) -> bool:
    rut = limpiar_rut(rut)
    if len(rut) < 2:
        return False

    cuerpo, dv = rut[:-1], rut[-1]
    if not cuerpo.isdigit():
        return False

    suma = 0
    multiplicador = 2
    for dig in reversed(cuerpo):
        suma += int(dig) * multiplicador
        multiplicador = 2 if multiplicador == 7 else multiplicador + 1

    resto = 11 - (suma % 11)
    dv_esperado = "0" if resto == 11 else "K" if resto == 10 else str(resto)
    return dv == dv_esperado
