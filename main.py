
"""
Modulo: main.py
Proyecto: Software FJ - Sistema Integral de Gestion

Curso: Programacion
Universidad Nacional Abierta y a Distancia (UNAD)

Descripcion:
Punto de entrada principal de la aplicacion.

Coordina la gestion de clientes, servicios y reservas,
ejecuta diez operaciones de prueba y demuestra el
manejo controlado de excepciones.

No utiliza bases de datos. La informacion se administra
mediante objetos y listas en memoria.
"""

import logging
from pathlib import Path

from modelos import (
    Cliente,
    Reserva,
    ReservaSalas,
    AlquilerEquipos,
    AsesoriasEspecializadas,
    SistemaGestion
)

from excepciones import SoftwareFJError


# ============================================================
# CONFIGURACION GENERAL DEL SISTEMA
# ============================================================

def configurar_logging():
    """
    Configura el sistema de registro de eventos y errores.

    Los registros se almacenan en sistema_fj.log,
    ubicado en el mismo directorio de este archivo.
    """

    ruta_log = Path(__file__).resolve().parent / "sistema_fj.log"

    # Se obtiene el logger principal de Python.
    logger_raiz = logging.getLogger()

    # Se establece el nivel minimo de registro.
    logger_raiz.setLevel(logging.INFO)

    # Se eliminan manejadores anteriores para evitar
    # registros duplicados al reiniciar la aplicacion.
    for manejador in logger_raiz.handlers[:]:
        logger_raiz.removeHandler(manejador)
        manejador.close()

    # Se define el formato de los registros.
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Manejador para almacenar los registros en el archivo.
    manejador_archivo = logging.FileHandler(
        ruta_log,
        mode="a",
        encoding="utf-8"
    )

    manejador_archivo.setLevel(logging.INFO)
    manejador_archivo.setFormatter(formato)

    # Manejador para mostrar los registros en consola.
    manejador_consola = logging.StreamHandler()

    manejador_consola.setLevel(logging.WARNING)
    manejador_consola.setFormatter(formato)

    # Se agregan los manejadores al logger principal.
    logger_raiz.addHandler(manejador_archivo)
    logger_raiz.addHandler(manejador_consola)

    logger = logging.getLogger("SoftwareFJ")

    logger.info("=" * 65)
    logger.info("INICIALIZACION DEL SISTEMA SOFTWARE FJ")
    logger.info("Configuracion de registros completada.")
    logger.info("Archivo de logs: %s", ruta_log)
    logger.info("=" * 65)

    return logger


# ============================================================
# FUNCION GENERAL PARA EJECUTAR OPERACIONES
# ============================================================

def ejecutar_operacion(
    numero,
    descripcion,
    funcion,
    resultados,
    logger
):
    """
    Ejecuta una operacion individual y controla sus excepciones.

    Parametros:
        numero: identificador de la operacion.
        descripcion: nombre de la prueba.
        funcion: funcion que ejecuta la operacion.
        resultados: lista donde se almacenan los resultados.
        logger: objeto encargado de registrar los eventos.

    La funcion permite que un error no detenga las siguientes
    operaciones de la simulacion.
    """

    print(f"\n{'=' * 65}")
    print(f"OPERACION {numero}: {descripcion}")
    print("=" * 65)

    logger.info(
        "Inicio de operacion %s: %s",
        numero,
        descripcion
    )

    try:

        # Se ejecuta la operacion correspondiente.
        resultado = funcion()

    except SoftwareFJError as error:

        # Se captura cualquier excepcion personalizada.
        detalle = f"{type(error).__name__}: {error}"

        resultados.append({
            "numero": numero,
            "descripcion": descripcion,
            "estado": "Error controlado",
            "detalle": detalle
        })

        logger.warning(
            "Operacion %s finalizada con error controlado: %s",
            numero,
            detalle,
            exc_info=True
        )

        print(f"ERROR CONTROLADO: {detalle}")

    except Exception as error:

        # Se capturan errores inesperados para impedir
        # que una operacion interrumpa toda la simulacion.
        detalle = f"{type(error).__name__}: {error}"

        resultados.append({
            "numero": numero,
            "descripcion": descripcion,
            "estado": "Error inesperado",
            "detalle": detalle
        })

        logger.exception(
            "Error inesperado en la operacion %s.",
            numero
        )

        print(f"ERROR INESPERADO: {detalle}")

    else:

        # Este bloque solamente se ejecuta si la operacion
        # termino sin generar ninguna excepcion.
        detalle = str(resultado)

        resultados.append({
            "numero": numero,
            "descripcion": descripcion,
            "estado": "Correcta",
            "detalle": detalle
        })

        logger.info(
            "Operacion %s ejecutada correctamente: %s",
            numero,
            detalle
        )

        print(f"RESULTADO: {detalle}")

    finally:

        # Se ejecuta independientemente del resultado.
        logger.info(
            "Finalizada operacion %s: %s",
            numero,
            descripcion
        )

        print(f"Fin de la operacion {numero}.")


# ============================================================
# FUNCION PRINCIPAL DE SIMULACION
# ============================================================

def ejecutar_simulacion():
    """
    Inicializa el sistema y ejecuta diez operaciones
    de prueba sobre clientes, servicios y reservas.
    """

    # Primero se configura el registro de eventos.
    logger = configurar_logging()

    print("\n")
    print("#" * 65)
    print("       SISTEMA INTEGRAL DE GESTION - SOFTWARE FJ")
    print("#" * 65)

    # Se instancia el administrador central del sistema.
    # Este objeto mantiene las listas internas de informacion.
    sistema = SistemaGestion()

    # Almacenamiento de resultados de las pruebas.
    resultados = []

    # Contexto para conservar los objetos utilizados
    # en diferentes operaciones de la simulacion.
    contexto = {}

    # ========================================================
    # OPERACION 1
    # Registro valido y reserva exitosa de una sala.
    # ========================================================

    def operacion_1():

        cliente = Cliente(
            "1020304050",
            "Carlos Perez",
            "carlos.perez@mail.com"
        )

        servicio = ReservaSalas(
            "S01",
            "Sala Ejecutiva",
            50000,
            10
        )

        sistema.registrar_cliente(cliente)
        sistema.registrar_servicio(servicio)

        reserva = Reserva(
            cliente,
            servicio,
            detalle_tiempo=3
        )

        sistema.registrar_reserva(reserva)

        costo = reserva.procesar_reserva(
            descuento=0.10,
            incluir_impuesto=True
        )

        contexto["cliente_1"] = cliente
        contexto["servicio_1"] = servicio
        contexto["reserva_1"] = reserva

        return (
            f"Reserva {reserva.estado}. "
            f"Cliente: {cliente.nombre}. "
            f"Costo total: ${costo:,.2f}"
        )

    ejecutar_operacion(
        1,
        "Registro valido y reserva exitosa de sala",
        operacion_1,
        resultados,
        logger
    )

    # ========================================================
    # OPERACION 2
    # Intento de registrar un cliente con identificacion invalida.
    # ========================================================

    def operacion_2():

        Cliente(
            "ABC",
            "Ana Gomez",
            "ana@mail.com"
        )

        return "Cliente registrado correctamente."

    ejecutar_operacion(
        2,
        "Registro de cliente con identificacion invalida",
        operacion_2,
        resultados,
        logger
    )

    # ========================================================
    # OPERACION 3
    # Registro de cliente y alquiler exitoso de equipos.
    # ========================================================

    def operacion_3():

        cliente = Cliente(
            "9876543210",
            "Lucia Martinez",
            "lucia@mail.com"
        )

        servicio = AlquilerEquipos(
            "EQ01",
            "Kit Servidor de Pruebas",
            80000,
            "Servidor"
        )

        sistema.registrar_cliente(cliente)
        sistema.registrar_servicio(servicio)

        reserva = Reserva(
            cliente,
            servicio,
            detalle_tiempo=5
        )

        sistema.registrar_reserva(reserva)

        costo = reserva.procesar_reserva(
            seguro=True
        )

        contexto["cliente_2"] = cliente
        contexto["servicio_2"] = servicio
        contexto["reserva_2"] = reserva

        return (
            f"Alquiler {reserva.estado}. "
            f"Equipo: {servicio.tipo_equipo}. "
            f"Costo total: ${costo:,.2f}"
        )

    ejecutar_operacion(
        3,
        "Alquiler exitoso de equipos tecnologicos",
        operacion_3,
        resultados,
        logger
    )

    # ========================================================
    # OPERACION 4
    # Reserva exitosa de asesoria especializada.
    # ========================================================

    def operacion_4():

        cliente = Cliente(
            "1122334455",
            "Mateo Restrepo",
            "mateo@mail.com"
        )

        servicio = AsesoriasEspecializadas(
            "AS01",
            "Arquitectura Cloud",
            120000,
            "DevOps"
        )

        sistema.registrar_cliente(cliente)
        sistema.registrar_servicio(servicio)

        reserva = Reserva(
            cliente,
            servicio,
            detalle_tiempo=4
        )

        sistema.registrar_reserva(reserva)

        costo = reserva.procesar_reserva(
            nivel_experticia="Senior"
        )

        contexto["cliente_3"] = cliente
        contexto["servicio_3"] = servicio
        contexto["reserva_3"] = reserva

        return (
            f"Asesoria {reserva.estado}. "
            f"Area: {servicio.area}. "
            f"Costo total: ${costo:,.2f}"
        )

    ejecutar_operacion(
        4,
        "Reserva de asesoria especializada Senior",
        operacion_4,
        resultados,
        logger
    )

    # ========================================================
    # OPERACION 5
    # Intento de crear una reserva con tiempo negativo.
    # ========================================================

    def operacion_5():

        reserva = Reserva(
            contexto["cliente_1"],
            contexto["servicio_1"],
            detalle_tiempo=-2
        )

        return f"Reserva creada: {reserva.estado}"

    ejecutar_operacion(
        5,
        "Intento de reserva con tiempo negativo",
        operacion_5,
        resultados,
        logger
    )

    # ========================================================
    # OPERACION 6
    # Intento de registrar un cliente con correo invalido.
    # ========================================================

    def operacion_6():

        Cliente(
            "5544332211",
            "Sofia Ruiz",
            "correo-sin-arroba"
        )

        return "Cliente registrado correctamente."

    ejecutar_operacion(
        6,
        "Registro de cliente con correo electronico invalido",
        operacion_6,
        resultados,
        logger
    )

    # ========================================================
    # OPERACION 7
    # Intento de crear un servicio con tarifa negativa.
    # ========================================================

    def operacion_7():

        ReservaSalas(
            "S02",
            "Sala de Capacitacion",
            -50000,
            20
        )

        return "Servicio creado correctamente."

    ejecutar_operacion(
        7,
        "Creacion de servicio con tarifa invalida",
        operacion_7,
        resultados,
        logger
    )

    # ========================================================
    # OPERACION 8
    # Intento de procesar una asesoria con nivel incorrecto.
    # ========================================================

    def operacion_8():

        cliente = contexto["cliente_3"]
        servicio = contexto["servicio_3"]

        reserva = Reserva(
            cliente,
            servicio,
            detalle_tiempo=2
        )

        sistema.registrar_reserva(reserva)

        reserva.procesar_reserva(
            nivel_experticia="Experto"
        )

        return f"Reserva procesada: {reserva.estado}"

    ejecutar_operacion(
        8,
        "Asesoria con nivel de experticia no permitido",
        operacion_8,
        resultados,
        logger
    )

    # ========================================================
    # OPERACION 9
    # Cancelacion de una reserva existente.
    # ========================================================

    def operacion_9():

        reserva = contexto["reserva_1"]

        nuevo_estado = reserva.cancelar_reserva()

        return (
            f"Reserva del cliente {reserva.cliente.nombre} "
            f"actualizada a: {nuevo_estado}"
        )

    ejecutar_operacion(
        9,
        "Cancelacion de una reserva existente",
        operacion_9,
        resultados,
        logger
    )

    # ========================================================
    # OPERACION 10
    # Nueva reserva valida despues de los errores anteriores.
    # ========================================================

    def operacion_10():

        cliente = Cliente(
            "6677889900",
            "Diana Torres",
            "diana.torres@mail.com"
        )

        servicio = contexto["servicio_1"]

        sistema.registrar_cliente(cliente)

        reserva = Reserva(
            cliente,
            servicio,
            detalle_tiempo=2
        )

        sistema.registrar_reserva(reserva)

        costo = reserva.procesar_reserva(
            descuento=0.0,
            incluir_impuesto=False
        )

        contexto["reserva_10"] = reserva

        return (
            f"Reserva final {reserva.estado}. "
            f"Cliente: {cliente.nombre}. "
            f"Costo total: ${costo:,.2f}"
        )

    ejecutar_operacion(
        10,
        "Reserva exitosa despues de los errores anteriores",
        operacion_10,
        resultados,
        logger
    )

    # ========================================================
    # INFORME FINAL DE RESULTADOS
    # ========================================================

    print("\n")
    print("#" * 65)
    print("              INFORME FINAL DE SIMULACION")
    print("#" * 65)

    total = len(resultados)

    correctas = sum(
        1 for resultado in resultados
        if resultado["estado"] == "Correcta"
    )

    errores_controlados = sum(
        1 for resultado in resultados
        if resultado["estado"] == "Error controlado"
    )

    errores_inesperados = sum(
        1 for resultado in resultados
        if resultado["estado"] == "Error inesperado"
    )

    print(f"\nTotal de operaciones ejecutadas: {total}")
    print(f"Operaciones correctas: {correctas}")
    print(f"Errores controlados: {errores_controlados}")
    print(f"Errores inesperados: {errores_inesperados}")

    print("\nDETALLE DE OPERACIONES:")

    for resultado in resultados:

        print(
            f"\n[{resultado['numero']:02d}] "
            f"{resultado['descripcion']}"
        )

        print(f"Estado: {resultado['estado']}")
        print(f"Detalle: {resultado['detalle']}")

    # Se consulta el estado general de las colecciones.
    print("\n")
    print("-" * 65)
    print(sistema.obtener_resumen())
    print("-" * 65)

    # Se registra el resumen en el archivo de logs.
    logger.info(
        "Simulacion finalizada. Total: %s | Correctas: %s | "
        "Errores controlados: %s | Errores inesperados: %s",
        total,
        correctas,
        errores_controlados,
        errores_inesperados
    )

    print("\nArchivo de registros: sistema_fj.log")

    if total == 10 and errores_inesperados == 0:
        print("\nSIMULACION FINALIZADA SIN ERRORES INESPERADOS.")
    else:
        print("\nATENCION: Se deben revisar los resultados.")

    logger.info("FINALIZACION DEL SISTEMA SOFTWARE FJ.")
    logger.info("=" * 65)


# ============================================================
# PUNTO DE ENTRADA DE LA APLICACION
# ============================================================

if __name__ == "__main__":

    try:
        ejecutar_simulacion()

    except KeyboardInterrupt:
        print("\nEjecucion interrumpida por el usuario.")

    except Exception:
        logging.getLogger("SoftwareFJ").exception(
            "Error critico durante la ejecucion principal."
        )
        print(
            "\nSe produjo un error critico. "
            "Consulta el archivo sistema_fj.log."
        )
