
"""
Modulo: excepciones.py
Proyecto: Software FJ
Descripcion:
Define la jerarquia de excepciones personalizadas
utilizadas en el sistema de gestion de clientes,
servicios y reservas.
"""


class SoftwareFJError(Exception):
    """
    Excepcion base del sistema Software FJ.

    Todas las excepciones propias del proyecto
    heredan de esta clase.
    """
    pass


# ============================================================
# EXCEPCIONES RELACIONADAS CON CLIENTES
# ============================================================

class ClienteInvalidoError(SoftwareFJError):
    """Se genera cuando los datos de un cliente no son validos."""
    pass


# ============================================================
# EXCEPCIONES RELACIONADAS CON SERVICIOS
# ============================================================

class ServicioInvalidoError(SoftwareFJError):
    """Se genera cuando un servicio contiene datos incorrectos."""
    pass


class ServicioNoDisponibleError(ServicioInvalidoError):
    """Se genera cuando se intenta utilizar un servicio inactivo."""
    pass


# ============================================================
# EXCEPCIONES RELACIONADAS CON RESERVAS
# ============================================================

class ReservaError(SoftwareFJError):
    """Excepcion general para errores durante una reserva."""
    pass


class ReservaCanceladaError(ReservaError):
    """Se genera cuando se intenta procesar una reserva cancelada."""
    pass


class EstadoReservaInvalidoError(ReservaError):
    """Se genera cuando una reserva tiene un estado no permitido."""
    pass


class CalculoCostoError(ReservaError):
    """Se genera cuando ocurre un error al calcular el costo."""
    pass
