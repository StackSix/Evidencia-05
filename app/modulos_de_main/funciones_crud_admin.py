from app.dao.dispositivos_dao import DispositivoDAO
from app.dao.usuarios_dao import UsuarioDAO
from app.dao.domicilios_dao import DomiciliosDAO

def menu_crud_usuario():
    while True:
        print("CRUD - Usuarios")
        print(" 1) Ver Usuarios Registrados") #listo 
        print(" 2) Actualizar Usuario") 
        print(" 3) Eliminar Usuario")
        print(" 4) Modificar Rol de Usuario")
        print(" 0) Volver al menú anterior")
        print("Seleccione una opción: ")
    
        sop = input("> ").strip()
        
        if sop == "1":
            ver_usuarios_registrados()
        elif sop == "2":
            actualizar_usuario()
        elif sop == "3":
            eliminar_usuario()
        elif sop == "4":
            modificar_rol_usuario()
        elif sop == "0":
            break
        else:
            print("❌ Opción no válida. Intentelo de nuevo.")        
      
def ver_usuarios_registrados():
    usuarios = UsuarioDAO.listar_todos_usuarios()
    if usuarios:    
        for u in usuarios:
            print(f"{u.dni} - {u.nombre} - {u.apellido} - {u.email}")
    else:
        print("❌ No se encontró ningún usuario.")
  
def actualizar_usuario():
    email = input("Ingrese el email del usuario a actualizar: ").strip()
    nuevo_nombre = input("Nuevo nombre: ").strip()
    nuevo_apellido = input("Nuevo apellido: ").strip()
    nueva_contrasena = input("Nueva contraseña: ").strip()

    actualizado = UsuarioDAO.actualizar_usuario(
        email=email,
        nombre=nuevo_nombre,
        apellido=nuevo_apellido,
        contrasena=nueva_contrasena
    )

    if actualizado:
        print("✅ Usuario actualizado correctamente.")
    else:
        print("⚠️ No se encontró ningún usuario con ese email.")

def eliminar_usuario():
    try:
        id_usuario = int(input("Ingrese el ID del usuario a eliminar: ").strip())
    except ValueError:
        print("❌ ID inválido. Debe ser un número entero.")
        return

    confirmacion = input(f"¿Estás seguro que querés eliminar el usuario con ID {id_usuario}? (s/n): ").lower()
    if confirmacion != "s":
        print("❎ Operación cancelada.")
        return

    eliminado = UsuarioDAO.eliminar_usuario(id_usuario)

    if eliminado:
        print("✅ Usuario eliminado correctamente.")
    else:
        print("⚠️ No se encontró ningún usuario con ese ID.")
        
def modificar_rol_usuario():
    try:
        id_usuario = int(input("🧍 Ingrese el ID del usuario al que desea modificar el rol: "))
        nuevo_id_rol = int(input("🔐 Ingrese el nuevo ID de rol: "))
        
        if UsuarioDAO.modificar_rol(id_usuario, nuevo_id_rol):
            print("✅ Rol modificado correctamente.")
        else:
            print("❌ No se encontró el usuario o no se pudo modificar el rol.")
    except ValueError:
        print("⚠️ Entrada inválida. Asegúrese de ingresar números para los IDs.")
    except Exception as e:
        print(f"⚠️ Ocurrió un error al modificar el rol: {e}")



def menu_crud_dispositivos():
    while True:
        print("CRUD - Dispositivos")
        print(" 1) Ver dispositivos") #listo
        print(" 2) Crear Dispositivo")
        print(" 3) Actualizar Dispositivo")
        print(" 4) Eliminar Dispositivo")
        print(" 0) Volver al menú anterior")
        print("Seleccione una opción: ")
    
        sop = input("> ").strip()
    
        if sop == "1":
            ver_dispositivos()
        elif sop == "2":
            registrar_dispositivo()
        elif sop == "3":
            actualizar_dispositivo()
        elif sop == "4":
            eliminar_dispositivo()
        elif sop == "0":
            break
        else:
            print("❌ Opción no válida. Intentelo de nuevo.")

def ver_dispositivos():
    dispositivos = DispositivoDAO.obtener_todos_dispositivos()
    if dispositivos:
        for d in dispositivos:
            print(f"{d.id_dispositivo} - {d.id_domicilio} - {d.id_tipo} - {d.estado} - {d.etiqueta}")
    else:
        print("❌ No se encontró ningún dispositivo.")
        
def registrar_dispositivo():
    # ID de domicilio 
    id_domicilio_input = input("Ingrese el ID del domicilio: ").strip()
    id_domicilio = int(id_domicilio_input) if id_domicilio_input else None

    # ID del tipo de dispositivo
    id_tipo_input = input("Ingrese el ID del tipo de dispositivo: ").strip()
    if not id_tipo_input.isdigit():
        print("❌ ID de tipo inválido.")
        return
    id_tipo = int(id_tipo_input)

    # Etiqueta
    etiqueta = input("Ingrese una etiqueta para el dispositivo: ").strip()
    if not etiqueta:
        print("❌ La etiqueta no puede estar vacía.")
        return

    try:
        nuevo_id = DispositivoDAO.registrar_dispositivo(id_domicilio, id_tipo, etiqueta)
        print(f"✅ Dispositivo registrado correctamente con ID {nuevo_id}.")
    except Exception as e:
        print(f"❌ Error al registrar el dispositivo: {e}")

def actualizar_dispositivo():
    # ID obligatorio
    id_disp_input = input("Ingrese el ID del dispositivo a actualizar: ").strip()
    if not id_disp_input.isdigit():
        print("❌ ID de dispositivo inválido.")
        return
    id_dispositivo = int(id_disp_input)

    # Campos opcionales
    id_domicilio_input = input("Ingrese el nuevo ID de domicilio (deje vacío para no modificar): ").strip()
    id_domicilio = int(id_domicilio_input) if id_domicilio_input else None

    id_tipo_input = input("Ingrese el nuevo ID de tipo (deje vacío para no modificar): ").strip()
    id_tipo = int(id_tipo_input) if id_tipo_input else None

    etiqueta = input("Ingrese la nueva etiqueta (deje vacío para no modificar): ").strip() or None

    # Verificar que al menos haya un cambio
    if id_domicilio is None and id_tipo is None and etiqueta is None:
        print("⚠️ No se ingresó ningún cambio.")
        return

    try:
        DispositivoDAO.actualizar_dispositivo(
            id_dispositivo,
            id_domicilio=id_domicilio,
            id_tipo=id_tipo,
            etiqueta=etiqueta
        )
        print("✅ Dispositivo actualizado correctamente.")
    except Exception as e:
        print(f"❌ Error al actualizar el dispositivo: {e}")

def eliminar_dispositivo():
    # ID del dispositivo
    id_disp_input = input("Ingrese el ID del dispositivo a eliminar: ").strip()
    if not id_disp_input.isdigit():
        print("❌ ID inválido. Debe ser un número entero.")
        return
    id_dispositivo = int(id_disp_input)

    # Confirmación
    confirm = input(f"¿Está seguro que desea eliminar el dispositivo con ID {id_dispositivo}? (s/n): ").lower()
    if confirm != "s":
        print("❎ Operación cancelada.")
        return

    try:
        DispositivoDAO.eliminar_dispositivo(id_dispositivo)
        print("✅ Dispositivo eliminado correctamente.")
    except Exception as e:
        print(f"❌ Error al eliminar el dispositivo: {e}")
        
        
def menu_crud_domicilio():
    while True:
        print("CRUD - Automatizaciones")
        print(" 1) Ver Domicilios")
        print(" 2) Crear Domicilio")
        print(" 3) Actualizar Domicilio")
        print(" 4) Eliminar Domicilio")
        print(" 0) Volver al menú anterior")
        print("Seleccione una opción: ")
        
        sop = input("> ")
        
        if sop == "1":
                ver_domicilios()
        elif sop == "2":
                registrar_domicilio()
        elif sop == "3":
                actualizar_domicilio()
        elif sop == "4":
                eliminar_domicilio()
        elif sop == "0":
            break
        else:
            print("❌ Opción no válida. Intentelo de nuevo.")
            
def ver_domicilios():
    domicilios = DomiciliosDAO.obtener_todos_domicilios()
    if domicilios:
        for d in domicilios:
            print(f"{d.id_domicilio} - {d.direccion} - {d.ciudad} - {d.nombre_domicilio}")
    else:
        print("❌ No se encontro ningun domicilio registrado.")

def registrar_domicilio():
    """
    Para registrar un nuevo domicilio.
    """
    print("\n🏠 Registrar nuevo domicilio")
    
    direccion = input("Ingrese la dirección: ").strip()
    numeracion = input("Ingrese la numeración: ").strip()
    ciudad = input("Ingrese la ciudad: ").strip()
    nombre_domicilio = input("Ingrese un nombre o alias para el domicilio: ").strip()

    if not direccion or not numeracion or not ciudad or not nombre_domicilio:
        print("❌ Todos los campos son obligatorios.")
        return

    try:
        id_domicilio = DomiciliosDAO.registrar_domicilio(direccion, numeracion, ciudad, nombre_domicilio)
        print(f"✅ Domicilio registrado correctamente con ID: {id_domicilio}")
    except Exception as e:
        print(f"❌ Error al registrar domicilio: {e}")

def actualizar_domicilio():
    """
    Para actualizar los datos de un domicilio existente.
    """
    try:
        id_domicilio = int(input("Ingrese el ID del domicilio a actualizar: ").strip())
    except ValueError:
        print("❌ ID inválido.")
        return

    # Pedir los nuevos datos
    direccion = input("Ingrese la nueva dirección: ").strip()
    numeracion = input("Ingrese la nueva numeración: ").strip()
    ciudad = input("Ingrese la nueva ciudad: ").strip()
    nombre_domicilio = input("Ingrese el nuevo nombre o alias del domicilio: ").strip()

    if not direccion or not numeracion or not ciudad or not nombre_domicilio:
        print("❌ Todos los campos son obligatorios.")
        return

    try:
        actualizado = DomiciliosDAO.actualizar_domicilio(id_domicilio, direccion, numeracion, ciudad, nombre_domicilio)
        if actualizado:
            print("✅ Domicilio actualizado correctamente.")
        else:
            print("❌ No se encontró el domicilio o no hubo cambios.")
    except Exception as e:
        print(f"❌ Error al actualizar el domicilio: {e}")

def eliminar_domicilio():
    """
    Para eliminar un domicilio existente.
    """
    try:
        id_domicilio = int(input("Ingrese el ID del domicilio a eliminar: ").strip())
    except ValueError:
        print("❌ ID inválido.")
        return

    confirmacion = input(f"¿Está seguro de eliminar el domicilio con ID {id_domicilio}? (s/n): ").strip().lower()
    if confirmacion != "s":
        print("❌ Operación cancelada.")
        return

    try:
        eliminado = DomiciliosDAO.eliminar_domicilio(id_domicilio)
        if eliminado:
            print("✅ Domicilio eliminado correctamente.")
        else:
            print("❌ No se encontró el domicilio.")
    except Exception as e:
        print(f"❌ Error al eliminar el domicilio: {e}")
    