# from ctypes.wintypes import SIZE
# from operator import ne
import sqlite3
from tkinter import *
from tkinter import ttk

# from tkinter import font
from tkinter.messagebox import *

# from xmlrpc.client import DateTime
import tkinter as tk
from PIL import ImageTk, Image
import os
import re


BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
ruta = os.path.join(BASE_DIR, "logo.jpg")


def crear_base():
    con = sqlite3.connect("mi_base.db")
    return con


def crear_tabla(con):
    cursor = con.cursor()
    sql = """CREATE TABLE socios
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             nombre varchar(20) NOT NULL,
             apellido varchar(20) NOT NULL,
             dni integer NOT NULL,
             fecha integer NOT NULL,
             categoria varchar(20) NOT NULL, )
    """
    cursor.execute(sql)
    con.commit()


try:
    con = crear_base()
    crear_tabla(con)
except:
    pass


def seleccionado():
    valor = tree.selection()
    item = tree.item(valor)
    mi_idd = item["text"]
    return mi_idd, valor


def insertar(nombre, apellido, dni, fecha, categoria, tree):
    cadena1 = nombre
    cadena2 = apellido
    patron = "^[A-Za-záéíóú]*$"
    if re.match(patron, cadena1):
        if re.match(patron, cadena2):
            con = crear_base()
            cursor = con.cursor()
            # mi_id = int(mi_id)
            data = (nombre, apellido, dni, fecha, categoria)
            sql = "INSERT INTO socios(nombre, apellido,  dni, fecha, categoria) VALUES (?, ?, ?, ?, ?);"
            cursor.execute(sql, data)
            con.commit()
            actualizar_treeview(tree)
            limpiar_campos()
        else:
            f_error("Campos ingresados en 'Apellido' incorrectos")
    else:
        f_error("Campos ingresados en 'Nombre' incorrectos")


def f_guardar(tree):

    insertar(
        var_nombre.get(),
        var_apellido.get(),
        var_dni.get(),
        var_nacimiento.get(),
        var_categoria.get(),  # PERMITE GUARDAR AUNQUE EL CAMPO CATEGORIA ESTE VACIO. PORQUE????
        tree,
    )


def f_seleccionar(tree):
    bt_guardar["state"] = DISABLED
    limpiar_campos()

    if tree.selection():
        valor = tree.selection()
        item = tree.item(valor)
        mi_id = item["text"]
        campos = item["values"]
        mi_id = int(mi_id)
        completar_campos(campos)
        bt_modificar["state"] = NORMAL
        bt_borrar["state"] = NORMAL
        return mi_id
    else:
        f_error("No hay ningún ítem seleccionado")


def completar_campos(campos):  # Completa los campos de ingreso de datos

    entry_nombre.insert(0, campos[0])
    entry_apellido.insert(0, campos[1])
    entry_dni.insert(0, campos[2])
    entry_nacimiento.insert(0, campos[3])
    entry_categoria.insert(0, campos[4])


def f_borrar(tree):
    bt_borrar["state"] = DISABLED
    bt_modificar["state"] = DISABLED
    if tree.selection():

        mi_id, valor = seleccionado()
        con = crear_base()
        cursor = con.cursor()
        data = (mi_id,)
        sql = "DELETE FROM socios WHERE id = ?;"
        cursor.execute(sql, data)
        con.commit()
        tree.delete(valor)
        limpiar_campos()
        bt_guardar["state"] = NORMAL

    else:
        f_error("No hay ningún ítem seleccionado")


def actualizar_bd(nombre, apellido, dni, fecha, categoria, tree):

    con = crear_base()
    cursor = con.cursor()
    valor = tree.selection()
    item = tree.item(valor)
    mi_id = item["text"]
    mi_id = int(mi_id)
    data = (nombre, apellido, dni, fecha, categoria, mi_id)
    sql = "UPDATE socios SET nombre=?, apellido=?,  dni=?, fecha=?, categoria=? WHERE id= ?;"
    cursor.execute(sql, data)
    con.commit()
    actualizar_treeview(tree)


def f_modificar(tree):
    bt_modificar["state"] = DISABLED
    bt_borrar["state"] = DISABLED
    bt_guardar["state"] = NORMAL
    actualizar_bd(
        var_nombre.get(),
        var_apellido.get(),
        var_dni.get(),
        var_nacimiento.get(),
        var_categoria.get(),
        tree,
    )
    limpiar_campos()


def actualizar_treeview(mitreview):
    records = mitreview.get_children()
    for element in records:
        mitreview.delete(element)

    sql = "SELECT * FROM socios ORDER BY id DESC"
    con = crear_base()
    cursor = con.cursor()
    datos = cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        mitreview.insert(
            "", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5])
        )


master = Tk()
master.title("Planilla del Club")
# master.geometry("800x700")


espacio = Label(master)
espacio.grid(row=0, columnspan=4)
nombre_del_club = Label(master, text="CLUB UNIVERSITARIO")
nombre_del_club.grid(columnspan=4, row=1, column=0)

nombre_del_club2 = Label(master, text="DE RUGBY")
nombre_del_club2.grid(columnspan=4, row=2, column=0)
espacio = Label(master)
espacio.grid(row=4, columnspan=4)


logo = Image.open(ruta)
resize_logo = logo.resize((100, 100))
logo2 = ImageTk.PhotoImage(resize_logo)
mi_logo = tk.Label(master, image=logo2)
mi_logo.grid(row=0, column=6, rowspan=4, pady=10)


var_nombre = StringVar()
var_apellido = StringVar()
var_dni = IntVar()
var_nacimiento = IntVar()
var_categoria = StringVar()


def f_error(un_string):
    showerror("ERROR", un_string)


def limpiar_campos():  # Vacia los campos de ingreso de datos

    entry_nombre.delete(0, END)
    entry_apellido.delete(0, END)
    entry_dni.delete(0, END)
    entry_nacimiento.delete(0, END)
    entry_categoria.delete(0, END)

    entry_nombre.insert(0, "")
    entry_apellido.insert(0, "")
    entry_dni.insert(0, "")
    entry_nacimiento.insert(0, "")
    entry_categoria.insert(0, "")


nombre = Label(master, text="Nombre")
nombre.grid(row=7, column=0, sticky=W, padx=10)

apellido = Label(master, text="Apellido", anchor=N)
apellido.grid(row=7, column=2, sticky=W, padx=10)

dni = Label(master, text="DNI", anchor=N)
dni.grid(row=8, column=0, sticky=W, padx=10)

nacimiento = Label(master, text="Fecha de nacimiento", anchor=N)
nacimiento.grid(row=8, column=2, sticky=W, padx=10)

categoria = Label(master, text="Categoria", anchor=N)
categoria.grid(row=9, column=0, sticky=W, padx=10)
w_ancho = 25

entry_nombre = Entry(master, textvariable=var_nombre, width=w_ancho)
entry_nombre.grid(row=7, column=1)

entry_apellido = Entry(master, textvariable=var_apellido, width=w_ancho)
entry_apellido.grid(row=7, column=3)

entry_dni = Entry(master, textvariable=var_dni, width=w_ancho)
entry_dni.grid(row=8, column=1)

entry_nacimiento = Entry(master, textvariable=var_nacimiento, width=w_ancho)
entry_nacimiento.grid(row=8, column=3)

entry_categoria = Entry(master, textvariable=var_categoria, width=w_ancho)
entry_categoria.grid(row=9, column=1)

espacio = Label(master)
espacio.grid(row=10, columnspan=4)
limpiar_campos()


tree = ttk.Treeview(master)

tree["columns"] = ("Nombre", "Apellido", "DNI", "Fecha de Nacimiento", "Categoria")

tree.column("#0", width=50, minwidth=20, anchor=W)
tree.column("Nombre", width=200, minwidth=20, anchor=W)
tree.column("Apellido", width=200, minwidth=20, anchor=W)
tree.column("DNI", width=100, minwidth=20, anchor=W)
tree.column("Fecha de Nacimiento", width=150, minwidth=20, anchor=W)
tree.column("Categoria", width=80, minwidth=20, anchor=W)

tree.heading("#0", text="ID")
tree.heading("Nombre", text="NOMBRE")
tree.heading("Apellido", text="APELLIDO")
tree.heading("DNI", text="DNI")
tree.heading("Fecha de Nacimiento", text="FECHA DE NACIMIENTO")
tree.heading("Categoria", text="CATEGORIA")

tree.grid(column=0, row=11, columnspan=8, padx=10)


actualizar_treeview(tree)

bt_guardar = Button(
    master, text="Guardar", command=lambda: f_guardar(tree), bg="#DCDCDC", width=20
)
bt_guardar.grid(row=10, column=-0, pady=5, padx=5, columnspan=1)

bt_modificar = Button(
    master,
    text="Modificar",
    command=lambda: f_modificar(tree),
    bg="#DCDCDC",
    width=20,
    state=DISABLED,
)
bt_modificar.grid(row=10, column=1, pady=5, padx=5, columnspan=1)

bt_seleccionar = Button(
    master,
    text="Seleccionar",
    command=lambda: f_seleccionar(tree),
    bg="#DCDCDC",
    width=20,
)
bt_seleccionar.grid(row=10, column=3, pady=5, padx=5, columnspan=2)

bt_borrar = Button(
    master,
    text="Borrar",
    command=lambda: f_borrar(tree),
    bg="#DCDCDC",
    width=20,
    state=DISABLED,
)
bt_borrar.grid(row=10, column=5, pady=5, padx=5, columnspan=2)


bt_salir = Button(master, text="Salir", command=master.quit, bg="#DCDCDC", width=15)
bt_salir.grid(row=15, column=6, sticky=SE, padx=10, pady=10)

master.mainloop()
