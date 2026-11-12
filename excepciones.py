class SoftwareFJError(Exception):
    """Clase base para todas las excepciones del sistema Software FJ."""
    pass

class ClienteInvalidoError(SoftwareFJError):
    """Excepción lanzada cuando los datos del cliente no son válidos."""
    pass

class ServicioNoDisponibleError(SoftwareFJError):
    """Excepción lanzada cuando un servicio no está disponible o es incorrecto."""
    pass

class ReservaError(SoftwareFJError):
    """Excepción lanzada ante fallos en el proceso de reserva."""
    pass