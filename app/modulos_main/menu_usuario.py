from __future__ import annotations
from dao.dispositivo_dao import DispositivoDAO
from dao.usuario_dao import UsuarioDAO
from dao.domicilio_dao import DomicilioDAO
from servicios.gestor_usuario import GestorUsuario
from servicios.gestor_domicilio import GestorDomicilio
from servicios.gestor_automatizacion import GestorAutomatizacion
from modulos_main.menu_crud_automatizaciones import menu_crud_automatizacion
from modulos_main.menu_crud_domicilios import menu_crud_domicilios
from modulos_main.menu_crud_usuarios import menu_crud_usuarios
from modulos_main.menu_crud_dispositivos import gestionar_dispositivos

def menu_usuario(session):
    print(f"\nBienvenido/a {session['nombre']} ({session['rol']})")
    while True:
        print("\n1) Ver mis domicilios") 
        print("2) Ver mis dispositivos") 
        print("3) Ver mis datos personales") 
        if session["rol"] == "Admin":
            print("4) [ADMIN] Gestionar CRUDs")
            
        print("0) Salir")
        op = input("> ").strip()

        if op == "1":
            ver_domicilios_usuario(session["id_usuario"])

        elif op == "2":
            ver_dispositivos_usuario(session["id_usuario"])

        elif op == "3":
            ver_datos_personales(session["dni"])

        elif op == "4" and session["rol"] == "Admin":
            gestor_usuario = GestorUsuario()
            gestor_automatizacion = GestorAutomatizacion()
            while True:
                print("\n[Menú CRUD]")
                print(" 1) Menú CRUD Usuarios")
                print(" 2) Menú CRUD Domicilios")
                print(" 3) Menú CRUD Dispositivos")
                print(" 4) Menú CRUD Automatización")
                print(" 0) Volver al menú anterior")
                sop = input("> ").strip()
                
                if sop == "1":
                    menu_crud_usuarios(session, gestor_usuario)
                    
                elif sop == "2":
                    gestor_domicilio = GestorDomicilio(session["id_usuario"])
                    menu_crud_domicilios(session, gestor_domicilio)
                        
                elif sop == "3":
                    gestionar_dispositivos(session)
                            
                elif sop == "4":
                    menu_crud_automatizacion(session, gestor_automatizacion)
                
                elif sop == "0":
                    break
                
                else:
                    print("Ingrese una opción válida. Intentelo de nuevo")
        
        elif op == "0":
            print("Cerrando Sesión.")
            break
        
        else:
            print("La opción ingresada no es válida. Intentelo nuevamente.")
        
            
def ver_domicilios_usuario(id_usuario: int):
    domicilios_usuario = DomicilioDAO.obtener_domicilio_usuario(id_usuario)
    if domicilios_usuario:    
        for du in domicilios_usuario:
            print(f"\nMI DOMICILIO \nID Domicilio: {du.id_domicilio}\nNombre de Domicilio: {du.nombre_domicilio}\nDirección: {du.direccion}\nCiudad: {du.ciudad}")
    else:
        print("❌ No se encontró domicilio del usuario.")
        
def ver_dispositivos_usuario(id_usuario: int):
    dispositivos_usuario = DispositivoDAO.obtener_dispositivo_usuario(id_usuario)
    if dispositivos_usuario:
        for disp in dispositivos_usuario:
            print(f"\nMI DISPOSITIVO \nID Dispositivo: {disp.id_dispositivo}\nID Domicilio: {disp.id_domicilio}\nEstado: {disp.estado}\nEtiqueta: {disp.etiqueta}")
    else:
        print("❌ No se encontraron dispositivos del usuario.")
        
def ver_datos_personales(dni: int):
    usuario = UsuarioDAO.obtener_por_dni(dni)
    if usuario:
        print(f"\nMIS DATOS PERSONALES \nDNI: {usuario['dni']}\nNombre: {usuario['nombre']}\nApellido: {usuario['apellido']}\n"
              f"Email: {usuario['email']}\nRol: {usuario['rol']}")
    else:
        print("❌ No se encontró ningún usuario con ese DNI.")
        