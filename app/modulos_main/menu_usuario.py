from typing import Dict
from app.dao.automatizaciones_dao import AutomatizacionesDAO
from app.modulos_main.menu_crud_automatizaciones import menu_crud_automatizacion
from app.modulos_main.menu_crud_dispositivos import menu_crud_dispositivos
from app.modulos_main.menu_crud_domicilios import menu_crud_domicilios
from app.modulos_main.menu_crud_usuarios import menu_crud_usuarios
from app.dao.dispositivos_dao import DispositivoDAO
from app.dao.usuarios_dao import UsuarioDAO
from app.dao.domicilios_dao import DomiciliosDAO
from app.dominio.automatizacion import Automatizacion

def menu_usuario(session):
    print(f"\nBienvenido/a {session['nombre']} ({session['rol']})")
    while True:
        print("\n1) Ver mis domicilios") #listo
        print("2) Ver mis dispositivos") #listo
        print("3) Ver mis datos personales") #listo
        if session["rol"] == "admin":
            print("4) [ADMIN] Gestionar dispositivos (CRUD)")
            print("5) [ADMIN] Menú Gestión de Usuarios")
            
        print("0) Salir")
        op = input("> ").strip()

        if op == "1":
            ver_domicilios_usuario(session["dni"])

        elif op == "2":
            ver_dispositivos_usuario(session["id_usuario"])

        elif op == "3":
            ver_datos_personales(session["dni"])

        elif op == "4" and session["rol"] == "admin":
            # --- Submenú CRUD de dispositivos ---
            while True:
                print("\n[CRUD Dispositivos]")
                print(" 1) Menú Dispositivos")
                print(" 2) Menú Automatización")
                print(" 3) Menú Domicilios")
                print(" 0) Volver al menú anterior")
                sop = input("> ").strip()
                
                if sop == "1":
                    menu_crud_dispositivos(session)
                    
                elif sop == "2":
                    menu_crud_automatizacion(session)
                        
                elif sop == "3":
                    menu_crud_domicilios(session)
                
                elif sop == "0":
                    break
                
                else:
                    print("Ingrese una opción válida. Intentelo de nuevo")
                
        elif op == "5":
             menu_crud_usuarios(session)
             
        elif op == "6":
            break
        
        else:
            print("Ingrese una opción válida. Intentelo de nuevo")
            
def ver_domicilios_usuario(dni: int):
    domicilios_usuario = DomiciliosDAO.obtener_domicilio_usuario(dni)
    if domicilios_usuario:    
        for du in domicilios_usuario:
            print(f"{du.id_domicilio} - {du.nombre_domicilio} - {du.direccion} - {du.ciudad}")
    else:
        print("❌ No se encontró domicilio del usuario.")
        
def ver_dispositivos_usuario(id_usuario: int):
    dispositivos_usuario = DispositivoDAO.obtener_dispositivo_usuario(id_usuario)
    if dispositivos_usuario:
        for disp in dispositivos_usuario:
            print(f"{disp.id_dispositivo} - {disp.id_domicilio} - {disp.id_tipo} - {disp.estado} - {disp.etiqueta}")
    else:
        print("❌ No se encontraron dispositivos del usuario.")
        
def ver_datos_personales(dni: int):
    usuario = UsuarioDAO.obtener_por_dni(dni)
    if usuario:
        print(f"{usuario['dni']} - {usuario['nombre']} - {usuario['apellido']} - "
              f"{usuario['email']} - {usuario['rol']}")
    else:
        print("❌ No se encontró ningún usuario con ese DNI.")