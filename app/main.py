from app.servicios.auth_service import AuthService
from app.servicios.usuarios_service import UsuariosService
from app.servicios.dispositivos_service import DispositivosService
from app.servicios.domicilios_service import DomiciliosService
from app.servicios.habitacion_service import HabitacionService
from app.servicios.automatizaciones_service import AutomatizacionService


def menu_automatizacion(session: dict):
    """
    Menú básico de automatizaciones usando solo los campos que existen en la base.
    Incluye creación, listado y eliminación.
    """
    dni_usuario = session.get("dni")
    if not dni_usuario:
        print("⚠️ No se encontró información del usuario en sesión.")
        return

    # Traer domicilios del usuario
    domicilios = DomiciliosService.listar_por_usuario(dni_usuario)
    if not domicilios:
        print("⚠️ Debes registrar al menos un domicilio antes de usar automatizaciones.")
        return

    while True:
        print("\n--- Menú de Automatizaciones ---")
        print("1. Crear automatización")
        print("2. Eliminar automatización")
        print("3. Mostrar automatizaciones de mis domicilios")
        print("4. Modificar automatización")
        print("0. Volver al menú principal")
        opcion = input("> ")

        if opcion == "1":
            print("\n🏠 Tus domicilios:")
            for d in domicilios:
                print(f"{d['id_hogar']}: {d['nombre_domicilio']} ({d['direccion']})")
            try:
                id_hogar = int(input("Seleccione ID del hogar para la automatización: "))
                if id_hogar not in [d['id_hogar'] for d in domicilios]:
                    print("❌ El ID ingresado no corresponde a ninguno de tus domicilios.")
                    continue
            except ValueError as e:
                print("❌ Se debe ingresar un numero para seleccionar el ID.")
                continue
            
            nombre = input("Ingrese el nombre de la automatización: ").strip()
            if not nombre:
                print("❌ El nombre no debe ingresarse como vacio.")
                
            accion = input("Ingrese la acción (ej. 'encender', 'apagar'): ").strip().lower()
            if accion not in ["encender", "apagar"]:
                print("❌ Acción invalida, debe coincidir con 'encender' o 'apagar'")

            try:
                id_auto = AutomatizacionService.crear_automatizacion(
                    session, id_hogar, nombre, accion
                )
                print(f"✅ Automatización creada con ID {id_auto}.")
            except Exception as e:
                print(f"❌ Error al crear la automatización: {e}")

        elif opcion == "2":
            try:
                id_eliminar = int(input("Ingrese el ID de la automatización a eliminar: "))
                AutomatizacionService.eliminar_automatizacion(session, id_eliminar)
                print(f"✅ Automatización con ID {id_eliminar} eliminada correctamente.")
            except Exception as e:
                print(f"❌ Error al eliminar la automatización: {e}")

        elif opcion == "3":
            print("\n📄 Automatizaciones de tus domicilios:")
            try:
                autos_usuario = AutomatizacionService.listar_automatizaciones_por_usuario(session)
                if not autos_usuario:
                    print("⚠️ No hay automatizaciones registradas en tus domicilios.")
                else:
                    for a in autos_usuario:
                        nombre_hogar = next((d['nombre_domicilio'] for d in domicilios if d['id_hogar'] == a['id_hogar']), "Desconocido")
                        print(f"ID: {a['id_automatizacion']}, Nombre: {a['nombre']}, Acción: {a['accion']}, Hogar: {nombre_hogar}")
            except Exception as e:
                print(f"❌ Error al recuperar automatizaciones: {e}")

        elif opcion == "4":
            try:
                id_modificar = int(input("Ingrese el ID de la automatización a modificar: "))
                nueva_nombre = input("Nuevo nombre (Para no modificar presione enter): ").strip()
                nueva_accion = input("Nueva acción (Para no modificar presione enter): ").strip()

                AutomatizacionService.modificar_automatizacion(
                    session, id_modificar, nueva_nombre or None, nueva_accion or None
                )
                print(f"✅ Automatización con ID {id_modificar} modificada correctamente.")
            except Exception as e:
                print(f"❌ Error al modificar la automatización: {e}")

        elif opcion == "5":
            try:
                automatizacion_id = int(input("ID de la automatización: "))
                hora_on = input("Hora de encendido (HH:MM): ")
                hora_off = input("Hora de apagado (HH:MM): ")
                AutomatizacionService.configurar_automatizacion_horaria(
                    session, automatizacion_id, hora_on, hora_off
                )
                print("✅ Horario configurado correctamente.")
            except Exception as e:
                print(f"❌ Error al configurar horario: {e}")

        elif opcion == "0":
            break

        else:
            print("❌ Opción no válida.")

def menu_usuario(session):
    print(f"\nBienvenido/a {session['nombre']} ({session['rol']})")
    while True:
        print("\n1) Ver mis domicilios")
        print("2) Ver mis dispositivos")
        print("3) Ver mis datos personales")
        if session["rol"] == "admin":
            print("4) [ADMIN] Gestionar dispositivos (CRUD)")
            print("5) [ADMIN] Cambiar rol de usuario")
        print("0) Salir")
        op = input("> ").strip()

        if op == "1":
            hogares = DomiciliosService.listar_por_usuario(session["dni"])
            if not hogares:
                print("⚠️  No tienes domicilios registrados aún.")
            else:
                for h in hogares:
                    print(f"- {h['nombre_domicilio']} ({h['direccion']} {h.get('numeracion') or ''})")

        elif op == "2":
            devs = DispositivosService.listar_por_usuario(session["id"])
            if not devs:
                print("⚠️  No tienes dispositivos registrados aún.")
            else:
                for d in devs:
                    print(f"- [{d['nombre_tipo']}] {d['etiqueta']} @ {d['nombre_domicilio']} / {d['nombre_habitacion']}  (id={d['id_dispositivo']})")

        elif op == "3":
            UsuariosService.ver_mis_datos(session["dni"])

        elif op == "4" and session["rol"] == "admin":
            # --- Submenú CRUD de dispositivos ---
            while True:
                print("\n[CRUD Dispositivos]")
                print(" 1) Menú Automatización")
                print(" 2) Crear Dispositivo")
                print(" 3) Actualizar (mover/renombrar/cambiar tipo)")
                print(" 4) Encender/Apagar Dispositivo")
                print(" 5) Eliminar Dispositivo")
                print(" 6) Registrar Domicilio para sus Dispositivos")
                print(" 0) Volver")
                sop = input("> ").strip()
                if sop == "1":
                    menu_automatizacion(session)
                elif sop == "2":
                    ih_txt = input("id_habitacion (vacío=None): ").strip()
                    id_hab = int(ih_txt) if ih_txt else None
                    id_tipo = int(input("id_tipo: ").strip())
                    etiqueta = input("etiqueta: ").strip()
                    nuevo = DispositivosService.crear_admin(session, id_hab, id_tipo, etiqueta)
                    print("✅ Dispositivo creado id:", nuevo)
                elif sop == "3":
                    did = int(input("id_dispositivo: ").strip())
                    ih_txt = input("nuevo id_habitacion (vacío=sin cambio): ").strip()
                    it_txt = input("nuevo id_tipo (vacío=sin cambio): ").strip()
                    nueva_etq = input("nueva etiqueta (vacío=sin cambio): ").strip()
                    DispositivosService.actualizar_admin(
                        session,
                        did,
                        id_habitacion=int(ih_txt) if ih_txt else None,
                        id_tipo=int(it_txt) if it_txt else None,
                        etiqueta=nueva_etq or None,
                    )
                    print("✅ Actualizado.")
                elif sop == "4":
                    did = int(input("id_dispositivo: ").strip())
                    enc = input("encender? [s/n]: ").strip().lower() == "s"
                    DispositivosService.set_estado_admin(session, did, enc)
                    print("✅ Estado actualizado.")
                elif sop == "5":
                    did = int(input("id_dispositivo: ").strip())
                    DispositivosService.eliminar_admin(session, did)
                    print("🗑️  Eliminado.")
                elif sop == "6":
                    print("\n🏡 Crear nuevo domicilio 🏡")
                    try:
                        direccion = input("Ingrese la dirección: ").strip()
                        if not direccion:
                            print("❌ La dirección no puede estar vacía.")
                            continue

                        numeracion = input("Ingrese la numeración (opcional, puede dejar vacío): ").strip()
                        ciudad = input("Ingrese la ciudad: ").strip()
                        if not ciudad:
                            print("❌ La ciudad no puede estar vacía.")
                            continue

                        alias = input("Ingrese un nombre o alias para el domicilio: ").strip()
                        if not alias:
                            print("❌ El alias no puede estar vacío.")
                            continue

                        id_hogar = DomiciliosService.crear(session.get("dni"), direccion, numeracion, ciudad, alias)
                        print(f"✅ Domicilio creado correctamente con ID {id_hogar} y vinculado a tu usuario.")

                    except Exception as e:
                        print(f"❌ Error al crear el domicilio: {e}")
                elif sop == "0":
                    break
                else:
                    print("Opción inválida.")

        elif op == "5" and session["rol"] == "admin":
            uid = int(input("user_id a cambiar: ").strip())
            nr = input("nuevo rol [admin/usuario]: ").strip()
            UsuariosService.cambiar_rol_admin(session, uid, nr)
            print("OK")

        elif op == "0":
            break

def main():
    while True:
        print("Sistema SmartHome - Ejecución en memoria")
        print("Usuario administrador por defecto: admin@example.com / admin123")
        print("1) Registrarse")
        print("2) Iniciar sesión")
        print("3) Recuperar contraseña")
        print("0) Salir")
        op = input("> ").strip()

        if op == "1":
            dni = int(input("DNI: "))
            id_rol = 2  # usuario por defecto
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            email = input("Email: ")
            pw = input("Contraseña: ")
            uid = AuthService.registrar_usuario(dni, id_rol, nombre, apellido, email, pw)
            print("Usuario creado con id:", uid)

        elif op == "2":
            email = input("Email: ")
            pw = input("Contraseña: ")
            session = AuthService.login(email, pw)
            if not session:
                print("Credenciales inválidas.")
                return
            menu_usuario(session)

        elif op == "3":
            email = input("Email: ")
            dni = int(input("DNI: "))
            nueva_contra = input("Nueva contraseña: ")
            ok = AuthService.resetear_contrasena(email, dni, nueva_contra)
            print("Listo" if ok else "No se pudo resetear (email/dni incorrectos).")
        elif op == "0":
                break
        
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
