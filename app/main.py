from app.servicios.auth_service import AuthService
from app.servicios.usuarios_service import UsuarioService
from app.servicios.dispositivos_service import DispositivosService
from app.servicios.domicilios_service import DomiciliosService
from app.servicios.habitacion_service import HabitacionService
from app.servicios.automatizaciones_service import AutomatizacionService


def menu_automatizacion(session):
    while True:
        print("\n--- Menú de Automatizaciones ---")
        print("1. Crear automatización")
        print("2. Eliminar automatización")
        print("3. Mostrar detalles de una automatización")
        print("4. Configurar horario de una automatización")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ")
        
        try:
            if opcion == '1':
                id_hogar = int(input("Ingrese el ID del hogar: "))
                nombre = input("Ingrese el nombre de la automatización: ")
                accion = input("Ingrese la acción (ej. 'encender'): ")
                id_dispositivo = int(input("Ingrese el ID del dispositivo asociado: "))
                
                automatizacion_id = AutomatizacionService.crear_automatizacion(
                    current_user=session["current_user"],
                    id_hogar=id_hogar,
                    nombre=nombre,
                    accion=accion,
                    id_dispositivo_asociado=id_dispositivo
                )
                print(f"Automatización '{nombre}' creada con ID: {automatizacion_id}")
            
            elif opcion == '2':
                # Ejemplo de cómo llamar a la función eliminar_automatizacion
                automatizacion_id = int(input("Ingrese el ID de la automatización a eliminar: "))
                AutomatizacionService.eliminar_automatizacion(
                    current_user=session["current_user"],
                    automatizacion_id=automatizacion_id
                )
                print("Automatización eliminada con éxito.")

            elif opcion == '3':
                # Ejemplo de cómo llamar a la función mostrar_detalles_automatizacion
                automatizacion_id = int(input("Ingrese el ID de la automatización a ver: "))
                detalles = AutomatizacionService.mostrar_detalles_automatizacion(
                    current_user=session["current_user"],
                    automatizacion_id=automatizacion_id
                )
                if detalles:
                    print("\n--- Detalles de la automatización ---")
                    for key, value in detalles.items():
                        print(f"{key}: {value}")
                else:
                    print("Automatización no encontrada.")
            
            elif opcion == '4':
                # Ejemplo de cómo llamar a la función configurar_automatizacion_horaria
                automatizacion_id = int(input("Ingrese el ID de la automatización a configurar: "))
                hora_encendido = input("Ingrese la hora de encendido (HH:MM): ")
                hora_apagado = input("Ingrese la hora de apagado (HH:MM): ")
                AutomatizacionService.configurar_automatizacion_horaria(
                    current_user=session["current_user"],
                    automatizacion_id=automatizacion_id,
                    on=hora_encendido,
                    off=hora_apagado
                )
                print("Horario de automatización actualizado con éxito.")

            elif opcion == '5':
                break
            
            else:
                print("Opción no válida. Intente de nuevo.")
        
        except PermissionError as e:
            print(f"Error de permisos: {e}")
        except ValueError as e:
            print(f"Error de validación: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            
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
            UsuariosService.ver_mis_datos(session["id"])

        elif op == "4" and session["rol"] == "admin":
            # --- Submenú CRUD de dispositivos ---
            while True:
                print("\n[CRUD Dispositivos]")
                print(" 1) Menú Automatización")
                print(" 2) Crear")
                print(" 3) Actualizar (mover/renombrar/cambiar tipo)")
                print(" 4) Encender/Apagar")
                print(" 5) Eliminar")
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
    print("Sistema SmartHome - Ejecución en memoria")
    print("Usuario administrador por defecto: admin@example.com / admin123")
    print("1) Registrarse")
    print("2) Iniciar sesión")
    print("3) Recuperar contraseña")
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

if __name__ == "__main__":
    main()