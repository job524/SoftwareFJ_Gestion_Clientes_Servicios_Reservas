from modelos import Cliente, ReservaSalas, AlquilerEquipos, AsesoriasEspecializadas, Reserva
from excepciones import SoftwareFJError
import logging


def ejecutar_simulacion():
    print("=== INICIANDO SIMULACIÓN DE OPERACIONES - SOFTWARE FJ ===\n")
    
    # Lista para almacenar las operaciones simuladas
    operaciones = []
    c1 = s1 = c2 = s2 = c3 = s3 = None

    # Operación 1: Registro de cliente válido y reserva exitosa de Sala
    try:
        print("--- Operación 1: Reserva de Sala Válida ---")
        c1 = Cliente("1020304050", "Carlos Pérez", "carlos.perez@mail.com")
        s1 = ReservaSalas("S01", "Sala Ejecutiva", 50000, 10)
        res1 = Reserva(c1, s1, detalle_tiempo=3)
        res1.procesar_reserva(descuento=0.1, incluir_impuesto=True)
        operaciones.append(res1)
        print(f"Éxito: {res1.estado} - Costo: ${res1.costo_total}\n")
    except SoftwareFJError as e:
        print(f"Excepción capturada: {e}\n")

    # Operación 2: Intento de registro de Cliente con ID inválido (Prueba de excepción)
    try:
        print("--- Operación 2: Cliente con ID Inválido ---")
        c_malo = Cliente("ABC", "Ana Gómez", "ana@mail.com")
    except SoftwareFJError as e:
        print(f"Excepción controlada correctamente: {e}\n")

    # Operación 3: Alquiler de equipos exitoso
    try:
        print("--- Operación 3: Alquiler de Equipos Válido ---")
        c2 = Cliente("9876543210", "Lucía Martínez", "lucia@mail.com")
        s2 = AlquilerEquipos("EQ01", "Kit Servidor de Pruebas", 80000, "Servidor")
        res2 = Reserva(c2, s2, detalle_tiempo=5)
        res2.procesar_reserva(seguro=True)
        operaciones.append(res2)
        print(f"Éxito: {res2.estado} - Costo: ${res2.costo_total}\n")
    except SoftwareFJError as e:
        print(f"Excepción capturada: {e}\n")

    # Operación 4: Asesoría especializada Senior
    try:
        print("--- Operación 4: Asesoría Especializada Senior ---")
        c3 = Cliente("1122334455", "Mateo Restrepo", "mateo@mail.com")
        s3 = AsesoriasEspecializadas("AS01", "Arquitectura Cloud", 120000, "DevOps")
        res3 = Reserva(c3, s3, detalle_tiempo=4)
        res3.procesar_reserva(nivel_experticia="Senior")
        operaciones.append(res3)
        print(f"Éxito: {res3.estado} - Costo: ${res3.costo_total}\n")
    except SoftwareFJError as e:
        print(f"Excepción capturada: {e}\n")

    # Operación 5: Error en tiempo de reserva (tiempo negativo)
    try:
        print("--- Operación 5: Reserva con Parámetro de Tiempo Inválido ---")
        if c1 and s1:
            res4 = Reserva(c1, s1, detalle_tiempo=-2)
            res4.procesar_reserva()
    except SoftwareFJError as e:
        print(f"Excepción controlada correctamente en procesamiento: {e}\n")

    # Operación 6: Correo de cliente inválido
    try:
        print("--- Operación 6: Cliente con Correo Inválido ---")
        c_correo_malo = Cliente("5544332211", "Sofia Ruiz", "correo-sin-arroba")
    except SoftwareFJError as e:
        print(f"Excepción controlada de correo: {e}\n")

    # Operación 7: Alquiler con días inválidos (cero o negativo)
    try:
        print("--- Operación 7: Alquiler con Días Inválidos ---")
        if c2 and s2:
            res5 = Reserva(c2, s2, detalle_tiempo=0)
            res5.procesar_reserva(seguro=False)
    except SoftwareFJError as e:
        print(f"Excepción controlada de alquiler: {e}\n")

    # Operación 8: Asesoría con sesiones erróneas
    try:
        print("--- Operación 8: Asesoría con Sesiones Negativas ---")
        if c3 and s3:
            res6 = Reserva(c3, s3, detalle_tiempo=-1)
            res6.procesar_reserva(nivel_experticia="Junior")
    except SoftwareFJError as e:
        print(f"Excepción controlada de asesoría: {e}\n")

    # Operación 9: Cancelación de una reserva existente
    try:
        print("--- Operación 9: Cancelación de Reserva ---")
        if operaciones:
            operaciones[0].cancelar_reserva()
            print(f"Estado actualizado de la reserva: {operaciones[0].estado}\n")
        else:
            print("No hay reservas registradas para cancelar.\n")
    except Exception as e:
        print(f"Error al cancelar: {e}\n")

    # Operación 10: Nueva reserva válida para verificar la continuidad operativa tras errores
    try:
        print("--- Operación 10: Reserva de Cierre Post-Errores ---")
        if s1:
            c4 = Cliente("6677889900", "Diana Torres", "diana.torres@mail.com")
            res10 = Reserva(c4, s1, detalle_tiempo=2)
            res10.procesar_reserva(descuento=0.0, incluir_impuesto=False)
            operaciones.append(res10)
            print(f"Éxito final: {res10.estado} - Costo: ${res10.costo_total}\n")
    except SoftwareFJError as e:
        print(f"Excepción capturada: {e}\n")

    print("=== SIMULACIÓN FINALIZADA CON ÉXITO ===")
    print("Revisa el archivo 'sistema_fj.log' generado automáticamente para ver el registro de eventos.")


if __name__ == "__main__":
    ejecutar_simulacion()
