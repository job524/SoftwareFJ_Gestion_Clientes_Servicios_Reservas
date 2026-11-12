from abc import ABC, abstractmethod
import logging
from excepciones import ClienteInvalidoError, ServicioNoDisponibleError, ReservaError

# Configuración del sistema de logs
logging.basicConfig(
    filename='sistema_fj.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class EntidadBase(ABC):
    """Clase abstracta que representa entidades generales del sistema."""
    @abstractmethod
    def obtener_detalles(self):
        pass


class Cliente(EntidadBase):
    def __init__(self, identificacion: str, nombre: str, correo: str):
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo

    @property
    def identificacion(self):
        return self.__identificacion

    @identificacion.setter
    def identificacion(self, valor):
        if not valor or not str(valor).isdigit() or len(str(valor)) < 5:
            logging.error(f"Intento de registrar cliente con ID inválido: {valor}")
            raise ClienteInvalidoError("La identificación debe ser numérica y tener al menos 5 dígitos.")
        self.__identificacion = valor

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or "@" not in valor or "." not in valor:
            logging.error(f"Intento de registrar cliente con correo inválido: {valor}")
            raise ClienteInvalidoError("El formato del correo electrónico no es válido.")
        self.__correo = valor

    def obtener_detalles(self):
        return f"Cliente: {self.nombre} (ID: {self.identificacion}, Correo: {self.correo})"


class Servicio(EntidadBase, ABC):
    def __init__(self, codigo: str, nombre: str, tarifa_base: float):
        self.codigo = codigo
        self.nombre = nombre
        self.tarifa_base = tarifa_base

    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        pass

    def obtener_detalles(self):
        return f"Servicio: {self.nombre} [Código: {self.codigo}] - Tarifa Base: ${self.tarifa_base}"


class ReservaSalas(Servicio):
    def __init__(self, codigo: str, nombre: str, tarifa_base: float, capacidad: int):
        super().__init__(codigo, nombre, tarifa_base)
        self.capacidad = capacidad

    # Método con sobrecarga simulada mediante parámetros opcionales (con impuestos, descuentos)
    def calcular_costo(self, horas: int, descuento: float = 0.0, incluir_impuesto: bool = True) -> float:
        try:
            if horas <= 0:
                raise ValueError("Las horas de reserva deben ser mayores a cero.")
            subtotal = self.tarifa_base * horas
            subtotal_con_descuento = subtotal * (1 - descuento)
            total = subtotal_con_descuento * 1.19 if incluir_impuesto else subtotal_con_descuento
            return round(total, 2)
        except Exception as e:
            logging.error(f"Error calculando costo en ReservaSalas: {e}")
            raise ReservaError(f"Error en cálculo de costo de sala: {e}")


class AlquilerEquipos(Servicio):
    def __init__(self, codigo: str, nombre: str, tarifa_base: float, tipo_equipo: str):
        super().__init__(codigo, nombre, tarifa_base)
        self.tipo_equipo = tipo_equipo

    def calcular_costo(self, dias: int, seguro: bool = False) -> float:
        try:
            if dias <= 0:
                raise ValueError("Los días de alquiler deben ser mayores a cero.")
            costo = self.tarifa_base * dias
            if seguro:
                costo += 15000 * dias  # Costo fijo de seguro diario
            return round(costo, 2)
        except Exception as e:
            logging.error(f"Error calculando costo en AlquilerEquipos: {e}")
            raise ReservaError(f"Error en cálculo de alquiler: {e}")


class AsesoriasEspecializadas(Servicio):
    def __init__(self, codigo: str, nombre: str, tarifa_base: float, area: str):
        super().__init__(codigo, nombre, tarifa_base)
        self.area = area

    def calcular_costo(self, sesiones: int, nivel_experticia: str = "Junior") -> float:
        try:
            if sesiones <= 0:
                raise ValueError("El número de sesiones debe ser mayor a cero.")
            multiplicador = 1.5 if nivel_experticia.lower() == "senior" else 1.0
            return round(self.tarifa_base * sesiones * multiplicador, 2)
        except Exception as e:
            logging.error(f"Error calculando costo en AsesoriasEspecializadas: {e}")
            raise ReservaError(f"Error en cálculo de asesoría: {e}")


class Reserva:
    def __init__(self, cliente: Cliente, servicio: Servicio, detalle_tiempo: int):
        self.cliente = cliente
        self.servicio = servicio
        self.detalle_tiempo = detalle_tiempo
        self.estado = "Pendiente"
        self.costo_total = 0.0

    def procesar_reserva(self, *args, **kwargs):
        """Procesa la reserva aplicando try/except/else/finally exigidos por la guía."""
        try:
            logging.info(f"Iniciando procesamiento de reserva para {self.cliente.nombre}")
            self.costo_total = self.servicio.calcular_costo(self.detalle_tiempo, *args, **kwargs)
        except (ValueError, ReservaError) as ex:
            self.estado = "Fallida"
            logging.warning(f"Reserva fallida controlada: {ex}")
            raise
        else:
            self.estado = "Confirmada"
            logging.info(f"Reserva confirmada exitosamente. Total: ${self.costo_total}")
        finally:
            print(f"[LOG INTERNO] Estado final de la transacción de reserva: {self.estado}")

    def cancelar_reserva(self):
        self.estado = "Cancelada"
        logging.info(f"Reserva cancelada para el cliente {self.cliente.nombre}")
