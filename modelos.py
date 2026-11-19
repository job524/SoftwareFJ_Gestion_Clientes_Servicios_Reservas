
"""
Modulo: modelos.py
Proyecto: Software FJ
Curso: Programacion - UNAD

Descripcion:
Contiene las clases principales del sistema de gestion
de clientes, servicios y reservas.

Implementa:
- Programacion orientada a objetos.
- Abstraccion y herencia.
- Polimorfismo.
- Encapsulacion mediante propiedades.
- Validaciones de datos.
- Calculo de costos por tipo de servicio.
- Manejo avanzado de excepciones.
- Registro de clientes, servicios y reservas mediante listas.
"""

from abc import ABC, abstractmethod
import logging
import math
import re

from excepciones import (
    SoftwareFJError,
    ClienteInvalidoError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    ReservaError,
    ReservaCanceladaError,
    EstadoReservaInvalidoError,
    CalculoCostoError
)


# ============================================================
# CONFIGURACION DEL REGISTRO DE EVENTOS
# ============================================================

# Se obtiene un logger para el modulo.
# La configuracion del archivo de logs se realizara desde main.py.
logger = logging.getLogger(__name__)


# ============================================================
# FUNCIONES AUXILIARES DE VALIDACION
# ============================================================

def _validar_texto(valor, campo, excepcion):
    """
    Comprueba que un dato sea una cadena de texto no vacia.

    Retorna el texto sin espacios innecesarios en los extremos.
    """
    if not isinstance(valor, str) or not valor.strip():
        mensaje = f"El campo '{campo}' debe contener texto valido."
        logger.warning(mensaje)
        raise excepcion(mensaje)

    return valor.strip()


def _validar_entero_positivo(valor, campo, excepcion):
    """
    Comprueba que un valor sea un numero entero mayor que cero.

    Los valores booleanos no se aceptan como numeros enteros.
    """
    if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
        mensaje = f"El campo '{campo}' debe ser un entero mayor que cero."
        logger.warning(mensaje)
        raise excepcion(mensaje)

    return valor


def _validar_numero_positivo(valor, campo, excepcion):
    """
    Comprueba que un valor numerico sea positivo y finito.
    """
    if (
        isinstance(valor, bool)
        or not isinstance(valor, (int, float))
        or not math.isfinite(valor)
        or valor <= 0
    ):
        mensaje = f"El campo '{campo}' debe ser un numero positivo y finito."
        logger.warning(mensaje)
        raise excepcion(mensaje)

    return float(valor)


# ============================================================
# CLASE ABSTRACTA GENERAL
# ============================================================

class EntidadBase(ABC):
    """
    Clase abstracta que representa una entidad general
    dentro del sistema Software FJ.

    Las clases que hereden de esta deben implementar
    el metodo obtener_detalles().
    """

    @abstractmethod
    def obtener_detalles(self) -> str:
        """Retorna la informacion descriptiva de la entidad."""
        pass


# ============================================================
# CLASE CLIENTE
# ============================================================

class Cliente(EntidadBase):
    """
    Representa un cliente de Software FJ.

    Implementa encapsulacion mediante atributos privados
    y propiedades con validaciones.
    """

    def __init__(self, identificacion: str, nombre: str, correo: str):

        # Los atributos se asignan mediante sus propiedades.
        # Esto garantiza que las validaciones se ejecuten.
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo

        logger.info(
            "Cliente registrado correctamente: %s",
            self.identificacion
        )

    # --------------------------------------------------------
    # PROPIEDAD: IDENTIFICACION
    # --------------------------------------------------------

    @property
    def identificacion(self):
        """Retorna la identificacion del cliente."""
        return self.__identificacion

    @identificacion.setter
    def identificacion(self, valor):

        if isinstance(valor, bool) or valor is None:
            mensaje = "La identificacion del cliente no es valida."
            logger.warning(mensaje)
            raise ClienteInvalidoError(mensaje)

        identificacion = str(valor).strip()

        if not identificacion.isdigit() or len(identificacion) < 5:
            mensaje = (
                "La identificacion debe ser numerica "
                "y contener al menos 5 digitos."
            )
            logger.warning(mensaje)
            raise ClienteInvalidoError(mensaje)

        self.__identificacion = identificacion

    # --------------------------------------------------------
    # PROPIEDAD: NOMBRE
    # --------------------------------------------------------

    @property
    def nombre(self):
        """Retorna el nombre del cliente."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):

        nombre = _validar_texto(
            valor,
            "nombre",
            ClienteInvalidoError
        )

        if len(nombre) < 2:
            mensaje = "El nombre debe contener al menos 2 caracteres."
            logger.warning(mensaje)
            raise ClienteInvalidoError(mensaje)

        self.__nombre = nombre

    # --------------------------------------------------------
    # PROPIEDAD: CORREO ELECTRONICO
    # --------------------------------------------------------

    @property
    def correo(self):
        """Retorna el correo electronico del cliente."""
        return self.__correo

    @correo.setter
    def correo(self, valor):

        correo = _validar_texto(
            valor,
            "correo",
            ClienteInvalidoError
        )

        patron = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if not re.match(patron, correo):
            mensaje = "El formato del correo electronico no es valido."
            logger.warning(mensaje)
            raise ClienteInvalidoError(mensaje)

        self.__correo = correo

    # --------------------------------------------------------
    # METODOS GENERALES
    # --------------------------------------------------------

    def obtener_detalles(self) -> str:
        """Retorna la informacion general del cliente."""
        return (
            f"Cliente: {self.nombre} | "
            f"Identificacion: {self.identificacion} | "
            f"Correo: {self.correo}"
        )

    def __str__(self):
        return self.obtener_detalles()


# ============================================================
# CLASE ABSTRACTA SERVICIO
# ============================================================

class Servicio(EntidadBase, ABC):
    """
    Clase abstracta que representa los servicios ofrecidos
    por Software FJ.

    Las clases especializadas implementan el calculo de costos,
    la validacion de parametros y la descripcion del servicio.
    """

    def __init__(
        self,
        codigo: str,
        nombre: str,
        tarifa_base: float,
        disponible: bool = True
    ):

        self._codigo = _validar_texto(
            codigo,
            "codigo del servicio",
            ServicioInvalidoError
        )

        self._nombre = _validar_texto(
            nombre,
            "nombre del servicio",
            ServicioInvalidoError
        )

        self._tarifa_base = _validar_numero_positivo(
            tarifa_base,
            "tarifa base",
            ServicioInvalidoError
        )

        self.disponible = disponible

    @property
    def codigo(self):
        """Retorna el codigo del servicio."""
        return self._codigo

    @property
    def nombre(self):
        """Retorna el nombre del servicio."""
        return self._nombre

    @property
    def tarifa_base(self):
        """Retorna la tarifa base del servicio."""
        return self._tarifa_base

    @property
    def disponible(self):
        """Indica si el servicio se encuentra disponible."""
        return self._disponible

    @disponible.setter
    def disponible(self, valor):

        if not isinstance(valor, bool):
            raise ServicioInvalidoError(
                "La disponibilidad debe ser un valor booleano."
            )

        self._disponible = valor

    @abstractmethod
    def validar_parametros(self, cantidad, **kwargs):
        """
        Valida los parametros especificos del servicio.

        Cada servicio especializado debe implementar
        sus propias reglas de validacion.
        """
        pass

    @abstractmethod
    def calcular_costo(self, cantidad, *args, **kwargs) -> float:
        """Calcula el costo del servicio."""
        pass

    @abstractmethod
    def obtener_detalles(self) -> str:
        """Retorna la descripcion especifica del servicio."""
        pass

    def __str__(self):
        return self.obtener_detalles()


# ============================================================
# SERVICIO ESPECIALIZADO: RESERVA DE SALAS
# ============================================================

class ReservaSalas(Servicio):
    """
    Representa el servicio de reserva de salas.

    Permite calcular costos por horas, aplicar descuentos
    y determinar si se incluye el impuesto.
    """

    def __init__(
        self,
        codigo: str,
        nombre: str,
        tarifa_base: float,
        capacidad: int,
        disponible: bool = True
    ):

        super().__init__(
            codigo,
            nombre,
            tarifa_base,
            disponible
        )

        self._capacidad = _validar_entero_positivo(
            capacidad,
            "capacidad de la sala",
            ServicioInvalidoError
        )

    @property
    def capacidad(self):
        """Retorna la capacidad maxima de la sala."""
        return self._capacidad

    def validar_parametros(
        self,
        horas,
        descuento=0.0,
        incluir_impuesto=True
    ):
        """Valida las horas, el descuento y el impuesto."""

        _validar_entero_positivo(
            horas,
            "horas de reserva",
            ServicioInvalidoError
        )

        if (
            isinstance(descuento, bool)
            or not isinstance(descuento, (int, float))
            or not math.isfinite(descuento)
            or not 0 <= descuento <= 1
        ):
            raise ServicioInvalidoError(
                "El descuento debe estar entre 0 y 1."
            )

        if not isinstance(incluir_impuesto, bool):
            raise ServicioInvalidoError(
                "El indicador de impuesto debe ser verdadero o falso."
            )

    def calcular_costo(
        self,
        horas: int,
        descuento: float = 0.0,
        incluir_impuesto: bool = True
    ) -> float:
        """
        Calcula el costo de la reserva de una sala.

        Aplica descuento opcional e impuesto del 19 %.
        """

        try:
            self.validar_parametros(
                horas,
                descuento=descuento,
                incluir_impuesto=incluir_impuesto
            )

            subtotal = self.tarifa_base * horas
            valor_descuento = subtotal * descuento
            subtotal_final = subtotal - valor_descuento

            if incluir_impuesto:
                total = subtotal_final * 1.19
            else:
                total = subtotal_final

            return round(total, 2)

        except SoftwareFJError:
            logger.exception(
                "Validacion fallida al calcular costo de sala."
            )
            raise

        except Exception as error:
            logger.exception(
                "Error inesperado en el calculo de reserva de sala."
            )

            raise CalculoCostoError(
                "No fue posible calcular el costo de la sala."
            ) from error

    def obtener_detalles(self) -> str:
        """Retorna la descripcion de la sala."""

        estado = "Disponible" if self.disponible else "No disponible"

        return (
            f"Reserva de salas: {self.nombre} | "
            f"Codigo: {self.codigo} | "
            f"Tarifa por hora: ${self.tarifa_base:,.2f} | "
            f"Capacidad: {self.capacidad} personas | "
            f"Estado: {estado}"
        )


# ============================================================
# SERVICIO ESPECIALIZADO: ALQUILER DE EQUIPOS
# ============================================================

class AlquilerEquipos(Servicio):
    """
    Representa el alquiler de equipos tecnologicos.

    Permite calcular tarifas por dias y agregar
    un seguro opcional al alquiler.
    """

    def __init__(
        self,
        codigo: str,
        nombre: str,
        tarifa_base: float,
        tipo_equipo: str,
        disponible: bool = True
    ):

        super().__init__(
            codigo,
            nombre,
            tarifa_base,
            disponible
        )

        self._tipo_equipo = _validar_texto(
            tipo_equipo,
            "tipo de equipo",
            ServicioInvalidoError
        )

    @property
    def tipo_equipo(self):
        """Retorna la categoria del equipo."""
        return self._tipo_equipo

    def validar_parametros(self, dias, seguro=False):
        """Valida los dias del alquiler y el seguro."""

        _validar_entero_positivo(
            dias,
            "dias de alquiler",
            ServicioInvalidoError
        )

        if not isinstance(seguro, bool):
            raise ServicioInvalidoError(
                "La opcion de seguro debe ser verdadera o falsa."
            )

    def calcular_costo(
        self,
        dias: int,
        seguro: bool = False
    ) -> float:
        """
        Calcula el costo del alquiler de equipos.

        El seguro tiene un costo adicional de $15.000
        por cada dia de alquiler.
        """

        try:
            self.validar_parametros(
                dias,
                seguro=seguro
            )

            costo = self.tarifa_base * dias

            if seguro:
                costo += 15000 * dias

            return round(costo, 2)

        except SoftwareFJError:
            logger.exception(
                "Validacion fallida al calcular alquiler de equipos."
            )
            raise

        except Exception as error:
            logger.exception(
                "Error inesperado en el calculo del alquiler."
            )

            raise CalculoCostoError(
                "No fue posible calcular el costo del alquiler."
            ) from error

    def obtener_detalles(self) -> str:
        """Retorna la descripcion del equipo."""

        estado = "Disponible" if self.disponible else "No disponible"

        return (
            f"Alquiler de equipos: {self.nombre} | "
            f"Codigo: {self.codigo} | "
            f"Tipo: {self.tipo_equipo} | "
            f"Tarifa diaria: ${self.tarifa_base:,.2f} | "
            f"Estado: {estado}"
        )


# ============================================================
# SERVICIO ESPECIALIZADO: ASESORIAS
# ============================================================

class AsesoriasEspecializadas(Servicio):
    """
    Representa los servicios de asesoria especializada.

    Permite calcular costos por sesiones y aplicar
    tarifas dependiendo del nivel de experticia.
    """

    MULTIPLICADORES = {
        "junior": 1.0,
        "semisenior": 1.25,
        "senior": 1.5
    }

    def __init__(
        self,
        codigo: str,
        nombre: str,
        tarifa_base: float,
        area: str,
        disponible: bool = True
    ):

        super().__init__(
            codigo,
            nombre,
            tarifa_base,
            disponible
        )

        self._area = _validar_texto(
            area,
            "area de asesoria",
            ServicioInvalidoError
        )

    @property
    def area(self):
        """Retorna el area especializada de la asesoria."""
        return self._area

    def validar_parametros(
        self,
        sesiones,
        nivel_experticia="Junior"
    ):
        """Valida las sesiones y el nivel de experticia."""

        _validar_entero_positivo(
            sesiones,
            "sesiones de asesoria",
            ServicioInvalidoError
        )

        if not isinstance(nivel_experticia, str):
            raise ServicioInvalidoError(
                "El nivel de experticia debe ser un texto valido."
            )

        nivel = nivel_experticia.strip().lower()

        if nivel not in self.MULTIPLICADORES:
            raise ServicioInvalidoError(
                "El nivel de experticia debe ser Junior, "
                "SemiSenior o Senior."
            )

    def calcular_costo(
        self,
        sesiones: int,
        nivel_experticia: str = "Junior"
    ) -> float:
        """
        Calcula el costo de una asesoria especializada.

        El valor depende de la cantidad de sesiones
        y del nivel de experticia seleccionado.
        """

        try:
            self.validar_parametros(
                sesiones,
                nivel_experticia=nivel_experticia
            )

            nivel = nivel_experticia.strip().lower()

            multiplicador = self.MULTIPLICADORES[nivel]

            total = self.tarifa_base * sesiones * multiplicador

            return round(total, 2)

        except SoftwareFJError:
            logger.exception(
                "Validacion fallida al calcular asesoria especializada."
            )
            raise

        except Exception as error:
            logger.exception(
                "Error inesperado en el calculo de asesoria."
            )

            raise CalculoCostoError(
                "No fue posible calcular el costo de la asesoria."
            ) from error

    def obtener_detalles(self) -> str:
        """Retorna la descripcion de la asesoria."""

        estado = "Disponible" if self.disponible else "No disponible"

        return (
            f"Asesoria especializada: {self.nombre} | "
            f"Codigo: {self.codigo} | "
            f"Area: {self.area} | "
            f"Tarifa por sesion: ${self.tarifa_base:,.2f} | "
            f"Estado: {estado}"
        )


# ============================================================
# CLASE RESERVA
# ============================================================

class Reserva(EntidadBase):
    """
    Representa una reserva realizada por un cliente.

    Integra un cliente, un servicio, la duracion de la reserva,
    el costo calculado y el estado de la operacion.
    """

    ESTADOS_VALIDOS = (
        "Pendiente",
        "Confirmada",
        "Cancelada",
        "Fallida"
    )

    def __init__(
        self,
        cliente: Cliente,
        servicio: Servicio,
        detalle_tiempo: int
    ):

        if not isinstance(cliente, Cliente):
            raise ReservaError(
                "La reserva debe estar asociada a un cliente valido."
            )

        if not isinstance(servicio, Servicio):
            raise ReservaError(
                "La reserva debe estar asociada a un servicio valido."
            )

        self._detalle_tiempo = _validar_entero_positivo(
            detalle_tiempo,
            "duracion de la reserva",
            ReservaError
        )

        self._cliente = cliente
        self._servicio = servicio
        self._estado = "Pendiente"
        self._costo_total = 0.0

        logger.info(
            "Reserva creada para el cliente %s.",
            self._cliente.identificacion
        )

    # --------------------------------------------------------
    # PROPIEDADES DE CONSULTA
    # --------------------------------------------------------

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def detalle_tiempo(self):
        return self._detalle_tiempo

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    # --------------------------------------------------------
    # PROCESAMIENTO DE LA RESERVA
    # --------------------------------------------------------

    def procesar_reserva(self, *args, **kwargs):
        """
        Procesa una reserva y calcula su costo.

        Utiliza argumentos variables para permitir que cada
        servicio reciba sus propios parametros de calculo.

        Implementa manejo de excepciones y encadenamiento.
        """

        # Solo se pueden procesar reservas pendientes.
        if self._estado != "Pendiente":
            raise EstadoReservaInvalidoError(
                f"No se puede procesar una reserva en estado "
                f"{self._estado}."
            )

        try:

            # Comprueba la disponibilidad del servicio.
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio {self._servicio.nombre} "
                    "no se encuentra disponible."
                )

            logger.info(
                "Procesando reserva del cliente %s.",
                self._cliente.identificacion
            )

            # El calculo depende del tipo de servicio.
            # Aqui se aplica el polimorfismo.
            costo_calculado = self._servicio.calcular_costo(
                self._detalle_tiempo,
                *args,
                **kwargs
            )

        except SoftwareFJError:
            # Se conserva la excepcion personalizada original.
            self._estado = "Fallida"

            logger.exception(
                "La reserva del cliente %s fallo.",
                self._cliente.identificacion
            )

            raise

        except Exception as error:
            # Se convierte un error inesperado en una excepcion
            # propia del sistema, conservando su causa original.
            self._estado = "Fallida"

            logger.exception(
                "Error inesperado durante el procesamiento de la reserva."
            )

            raise ReservaError(
                "Ocurrio un error inesperado al procesar la reserva."
            ) from error

        else:
            # Este bloque se ejecuta solamente si no hubo errores.
            self._costo_total = costo_calculado
            self._estado = "Confirmada"

            logger.info(
                "Reserva confirmada. Cliente: %s. Costo: %.2f",
                self._cliente.identificacion,
                self._costo_total
            )

            return self._costo_total

        finally:
            # Se ejecuta independientemente del resultado.
            logger.info(
                "Finalizacion del procesamiento. Estado: %s",
                self._estado
            )

    # --------------------------------------------------------
    # CANCELACION DE RESERVA
    # --------------------------------------------------------

    def cancelar_reserva(self):
        """Cancela una reserva pendiente o confirmada."""

        if self._estado == "Cancelada":
            raise ReservaCanceladaError(
                "La reserva ya se encuentra cancelada."
            )

        if self._estado != "Pendiente" and self._estado != "Confirmada":
            raise EstadoReservaInvalidoError(
                "No se puede cancelar una reserva en su estado actual."
            )

        self._estado = "Cancelada"

        logger.info(
            "Reserva cancelada para el cliente %s.",
            self._cliente.identificacion
        )

        return self._estado

    # --------------------------------------------------------
    # DESCRIPCION DE LA RESERVA
    # --------------------------------------------------------

    def obtener_detalles(self) -> str:
        """Retorna la informacion completa de la reserva."""

        return (
            f"Reserva | "
            f"Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | "
            f"Duracion: {self._detalle_tiempo} | "
            f"Estado: {self._estado} | "
            f"Costo: ${self._costo_total:,.2f}"
        )

    def __str__(self):
        return self.obtener_detalles()


# ============================================================
# CLASE ADMINISTRADORA DEL SISTEMA
# ============================================================

class SistemaGestion:
    """
    Administra los clientes, servicios y reservas de Software FJ.

    Utiliza listas internas en memoria, sin emplear
    ningun motor de bases de datos.
    """

    def __init__(self):

        self.__clientes = []
        self.__servicios = []
        self.__reservas = []

        logger.info("Sistema de gestion inicializado.")

    # --------------------------------------------------------
    # CONSULTA DE COLECCIONES
    # --------------------------------------------------------

    @property
    def clientes(self):
        """Retorna una vista inmodificable de los clientes."""
        return tuple(self.__clientes)

    @property
    def servicios(self):
        """Retorna una vista inmodificable de los servicios."""
        return tuple(self.__servicios)

    @property
    def reservas(self):
        """Retorna una vista inmodificable de las reservas."""
        return tuple(self.__reservas)

    # --------------------------------------------------------
    # REGISTRO DE CLIENTES
    # --------------------------------------------------------

    def registrar_cliente(self, cliente: Cliente):
        """Registra un cliente evitando identificaciones duplicadas."""

        if not isinstance(cliente, Cliente):
            raise ClienteInvalidoError(
                "El objeto proporcionado no es un cliente valido."
            )

        for cliente_existente in self.__clientes:

            if cliente_existente.identificacion == cliente.identificacion:
                raise ClienteInvalidoError(
                    "Ya existe un cliente con esa identificacion."
                )

        self.__clientes.append(cliente)

        logger.info(
            "Cliente agregado al sistema: %s.",
            cliente.identificacion
        )

        return cliente

    # --------------------------------------------------------
    # REGISTRO DE SERVICIOS
    # --------------------------------------------------------

    def registrar_servicio(self, servicio: Servicio):
        """Registra un servicio evitando codigos duplicados."""

        if not isinstance(servicio, Servicio):
            raise ServicioInvalidoError(
                "El objeto proporcionado no es un servicio valido."
            )

        for servicio_existente in self.__servicios:

            if servicio_existente.codigo == servicio.codigo:
                raise ServicioInvalidoError(
                    "Ya existe un servicio con ese codigo."
                )

        self.__servicios.append(servicio)

        logger.info(
            "Servicio agregado al sistema: %s.",
            servicio.codigo
        )

        return servicio

    # --------------------------------------------------------
    # REGISTRO DE RESERVAS
    # --------------------------------------------------------

    def registrar_reserva(self, reserva: Reserva):
        """
        Registra una reserva si su cliente y servicio
        ya se encuentran registrados en el sistema.
        """

        if not isinstance(reserva, Reserva):
            raise ReservaError(
                "El objeto proporcionado no es una reserva valida."
            )

        cliente_registrado = any(
            cliente.identificacion == reserva.cliente.identificacion
            for cliente in self.__clientes
        )

        servicio_registrado = any(
            servicio.codigo == reserva.servicio.codigo
            for servicio in self.__servicios
        )

        if not cliente_registrado:
            raise ReservaError(
                "El cliente asociado no esta registrado en el sistema."
            )

        if not servicio_registrado:
            raise ReservaError(
                "El servicio asociado no esta registrado en el sistema."
            )

        if reserva in self.__reservas:
            raise ReservaError(
                "Esta reserva ya se encuentra registrada."
            )

        self.__reservas.append(reserva)

        logger.info(
            "Reserva agregada al sistema para el cliente %s.",
            reserva.cliente.identificacion
        )

        return reserva

    # --------------------------------------------------------
    # BUSQUEDA DE CLIENTES
    # --------------------------------------------------------

    def buscar_cliente(self, identificacion: str):
        """Busca un cliente por su identificacion."""

        for cliente in self.__clientes:

            if cliente.identificacion == str(identificacion):
                return cliente

        return None

    # --------------------------------------------------------
    # BUSQUEDA DE SERVICIOS
    # --------------------------------------------------------

    def buscar_servicio(self, codigo: str):
        """Busca un servicio por su codigo."""

        for servicio in self.__servicios:

            if servicio.codigo == codigo:
                return servicio

        return None

    # --------------------------------------------------------
    # RESUMEN GENERAL DEL SISTEMA
    # --------------------------------------------------------

    def obtener_resumen(self) -> str:
        """
        Genera un resumen de los elementos administrados
        por el sistema.
        """

        return (
            "RESUMEN DEL SISTEMA SOFTWARE FJ\n"
            f"Clientes registrados: {len(self.__clientes)}\n"
            f"Servicios registrados: {len(self.__servicios)}\n"
            f"Reservas registradas: {len(self.__reservas)}"
        )
