import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# Parametros de la Base de Datos
DB_HOST = "localhost"
DB_NAME = "inventario_discos"
DB_USER = "postgres"
DB_PASSWORD = "Soysuficiente91*"  

COLUMNA_STOCK = "stock" # 

# Perfiles de Usuarios 
PERFILES = {
    1: "Gerencia",
    2: "Bodega",
    3: "Vendedores",
}

#version de la aplicacion y registro de actividades
VERSION_APP = "Versión 1.0"
ARCHIVO_LOG = "registro_actividades.txt"

# Funcion conectar: conecta la DB con el codigo en python
def conectar():
    return psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )

# Funcion quickshort: Ordena una lista usando el algoritmo QuickSort.
def quicksort(arr, clave, reverse=False):
    if len(arr) <= 1:
        return arr[:]
    pivot = clave(arr[len(arr)//2])
    less = [x for x in arr if clave(x) < pivot]
    equal = [x for x in arr if clave(x) == pivot]
    greater = [x for x in arr if clave(x) > pivot]
    result = quicksort(less, clave, reverse) + equal + quicksort(greater, clave, reverse)
    return list(reversed(result)) if reverse else result

#Funcion normalizar_str: Elimina espacios en blanco y convierte a minúsculas
def normalizar_str(s):
    return (s or "").strip()

# Registro LOG
#Funcion actividades_LOG: registra los cambios realizados por los usuarios durante su coneccion
def actividades_LOG(username, accion, detalles=""):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{ts}] Usuario: {username} | Acción: {accion} | Detalles: {detalles}\n"
    with open(ARCHIVO_LOG, "a", encoding="utf-8") as f:
        f.write(linea)

#Funcion descargar_log: descarga el archivo log como un bloc de notas 
def descargar_log():
    try:
        ruta = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Bloc de notas", "*.txt"), ("Todos los archivos", "*.*")],
            initialfile=f"registro_actividades_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        if ruta:
            with open(ARCHIVO_LOG, "r", encoding="utf-8") as origen, open(ruta, "w", encoding="utf-8") as destino:
                destino.write(origen.read())
            messagebox.showinfo("Log", f"Registro guardado en:\n{ruta}")
            return True
        return False
    except Exception as e:
        messagebox.showerror("Log", f"No se pudo guardar el registro: {e}")
        return False


# CLASE AUTENTICACION: 

class Auth:
    def __init__(self):
        self.db = conectar()
    #metodo _hash_password: Metodo que usa la ibreria hashlib para proteger contrasenas. UTF8 Convierte la contraseña (string) a bytes (necesario para SHA-256). Hashlib Aplica el algoritmo SHA-256 a los bytes. hexcode Convierte el hash en una cadena hexadecimal legible. 
    def _hash_password(self, password: str) -> str:
        import hashlib
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    #metodo para crear usuarios (insertar tambien en la DB en usuarios y en auth)
    def _crear_usuarios_por_defecto(self):
        cur = self.db.cursor()
        usuarios_defecto = [
            ("Gerencia", "gerencia123", 1),
            ("Danni Brito", "danni123", 2),
            ("Paul Pareja", "paul123", 2),
            ("Fabian Vega", "fabian123", 3),
            ("Jose Galarraga", "jose123", 3),
            ("Cristian Montero", "cristian123", 3)
        ]
        for nombre, password, perfil in usuarios_defecto:
            cur.execute("SELECT id_usuario FROM usuario WHERE nombre_usuario=%s", (nombre,))
            if not cur.fetchone():
                cur.execute(
                    "INSERT INTO usuario (nombre_usuario, correo, id_perfil1) VALUES (%s, %s, %s) RETURNING id_usuario",
                    (nombre, f"{nombre.replace(' ', '').lower()}@test.com", perfil)
                )
                id_usuario = cur.fetchone()[0]
                cur.execute(
                    "INSERT INTO auth (id_usuario, password_hash) VALUES (%s, %s)",
                    (id_usuario, self._hash_password(password))
                )
        self.db.commit()
    #metodo que realiza una consulta en la DB recibiendo los parametros usuario y contrasena para devolvernos una contrasena hasheada (protegida) de ese usuario
    def authenticate(self, username, password):
        cur = self.db.cursor()
        cur.execute("""
            SELECT u.id_usuario, u.nombre_usuario, u.id_perfil1, p.nombre_perfil, a.password_hash
            FROM usuario u
            JOIN perfil p ON u.id_perfil1 = p.id_perfil
            JOIN auth a ON u.id_usuario = a.id_usuario
            WHERE u.nombre_usuario = %s
        """, (username,))
        row = cur.fetchone()
        if row and row[4] == self._hash_password(password):
            return {"id": row[0], "nombre_usuario": row[1], "perfil": row[2], "nombre_perfil": row[3]}
        return None
    #metodo que cierra la ventana de autentificador una vez que se ingreso correctamente el usuario y contrasena
    def close(self):
        self.db.close()


# REPOSITORIO DE DISCOS
class DiscoRepo:
    #: DiscoRepo.listar() devuelve una lista de diccionarios, cada uno representando un disco con sus campos: id_disco, nombre_disco, artista, genero, precio y stock.
    #Se puede usar directamente para mostrar la tabla en la UI
    @staticmethod
    def listar():
        with conectar() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(f"""
                    SELECT id_disco, nombre_disco, artista, genero, precio, {COLUMNA_STOCK} AS stock
                    FROM disco_musica
                """)
                return cur.fetchall()
    #DiscoRepo.insertar()Inserta un nuevo registro en la tabla disco_musica.
    #%s son placeholders para valores seguros (previene SQL injection).
    ##conn.commit() confirma la operación en la base de datos.
    #Retorna new_id para usarlo en la UI o logs.
    @staticmethod
    def insertar(nombre, artista, genero, precio, stock):
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    INSERT INTO disco_musica (nombre_disco, artista, genero, precio, {COLUMNA_STOCK})
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id_disco
                """, (nombre, artista, genero, precio, stock))
                new_id = cur.fetchone()[0]
            conn.commit()
            return new_id
    #DiscoRepo.actualizar()Actualiza los datos de un disco existente identificado por id_disco.
    #Cambia todos los campos: nombre, artista, género, precio y stock.
    #conn.commit() confirma los cambios.
    #No devuelve nada; solo actualiza.
    @staticmethod
    def actualizar(id_disco, nombre, artista, genero, precio, stock):
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    UPDATE disco_musica
                    SET nombre_disco=%s, artista=%s, genero=%s, precio=%s, {COLUMNA_STOCK}=%s
                    WHERE id_disco=%s
                """, (nombre, artista, genero, precio, stock, id_disco))
            conn.commit()
    #DiscoRepo.eliminar()Borra un disco de la base de datos usando su id_disco.
    #También confirma con conn.commit().
    #No retorna nada.
    @staticmethod
    def eliminar(id_disco):
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM disco_musica WHERE id_disco=%s", (id_disco,))
            conn.commit()
    #DiscoRepo.sumar_stock()Modifica el stock de un disco específico.
    #COALESCE({COLUMNA_STOCK},0) asegura que si el stock estaba NULL, lo trate como 0.
    #+ %s permite sumar o restar dependiendo de si cantidad es positiva o negativa.
    #RETURNING {COLUMNA_STOCK} devuelve el stock actualizado.
    #Retorna nuevo_stock para mostrarlo en la interfaz o en logs.
    @staticmethod
    def sumar_stock(id_disco, cantidad):
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    UPDATE disco_musica
                    SET {COLUMNA_STOCK} = COALESCE({COLUMNA_STOCK},0) + %s
                    WHERE id_disco=%s
                    RETURNING {COLUMNA_STOCK}
                """, (cantidad, id_disco))
                nuevo_stock = cur.fetchone()[0]
            conn.commit()
            return nuevo_stock

# UI: LOGIN
#Esta clase representa la interfaz de login de la aplicación. master es la ventana principal de Tkinter donde se mostrará el login.
class LoginUI:
    def __init__(self, master):
        self.master = master
        master.title("FloydMusic - Login")
        master.geometry("440x260")
        master.resizable(False, False)

        cont = ttk.Frame(master, padding=20)
        cont.pack(expand=True, fill="both")
        #Titulo
        ttk.Label(cont, text="FloydMusic", font=("Arial", 20, "bold")).pack(pady=(0, 10))

        frm = ttk.Frame(cont)
        frm.pack(fill="x", pady=10)
        #Campos de ingreso de usuario y contrasena
        ttk.Label(frm, text="Usuario (Nombre Apellido):").grid(row=0, column=0, sticky="w", pady=5)
        self.var_user = tk.StringVar()
        ttk.Entry(frm, textvariable=self.var_user).grid(row=0, column=1, sticky="ew", padx=(10, 0))

        ttk.Label(frm, text="Contraseña (nombreminúsculas+123):").grid(row=1, column=0, sticky="w", pady=5)
        self.var_pass = tk.StringVar()
        ttk.Entry(frm, textvariable=self.var_pass, show="*").grid(row=1, column=1, sticky="ew", padx=(10, 0))

        frm.columnconfigure(1, weight=1)
        #Botón que ejecuta la función self.login cuando el usuario hace clic.
        ttk.Button(cont, text="Ingresar", command=self.login).pack(pady=10)

        # Versión al pie de la ventana (esquina inferior derecha)
        ttk.Label(cont, text=VERSION_APP).pack(side="bottom", anchor="e")
    #metodo Toma los valores que el usuario escribió en los campos de login..strip() elimina espacios al inicio y al final.
    def login(self):
        usuario = self.var_user.get().strip()
        contrasena = self.var_pass.get().strip()

        if not usuario or not contrasena:
            messagebox.showwarning("Login", "Ingrese un usuario y contraseña")
            return

        # Crear instancia de Auth y authenticate Auth() es la clase que maneja la autenticación.
        #authenticate(usuario, contrasena) verifica en la base de datos si las credenciales son correctas.
        #Retorna un diccionario con la información del usuario si es correcto, o None si no coincide.
        #auth.close() cierra la conexión a la base de datos.
        auth = Auth()
        fila = auth.authenticate(usuario, contrasena)
        auth.close()

        if fila:
            actividades_LOG(fila["nombre_usuario"], "Login", f"Perfil: {fila['nombre_perfil']}")
            self.master.destroy()
            root = tk.Tk()
            MainUI(root, fila)
            root.mainloop()
        else:
            messagebox.showerror("Login", "Usuario o contraseña incorrectos")

# UI: PRINCIPAL (inventario)
class MainUI:
    def __init__(self, master, usuario_info):
        self.master = master
        self.user = usuario_info
        self.master.title("FloydMusic - Inventario")
        self.master.geometry("980x600")
        self.master.minsize(900, 560)

        # Barra superior
        top = ttk.Frame(master, padding=8)
        top.pack(side="top", fill="x")

        ttk.Label(top, text=f"Bienvenido: {self.user['nombre_usuario']} ({self.user['nombre_perfil']})",
                  font=("Arial", 11, "bold")).pack(side="left")

        ttk.Button(top, text="Descargar log", command=self.descargar_log).pack(side="right", padx=6)
        ttk.Button(top, text="Cerrar sesión", command=self.logout).pack(side="right")

        # Barra de filtros y ordenamiento
        filtro = ttk.Frame(master, padding=(8, 0))
        filtro.pack(side="top", fill="x")

        ttk.Label(filtro, text="Ordenar por:").pack(side="left")
        self.cb_campo = ttk.Combobox(filtro, state="readonly",
                                     values=["id", "nombre", "artista", "genero", "stock"], width=12)
        self.cb_campo.current(0)
        self.cb_campo.pack(side="left", padx=6)

        ttk.Label(filtro, text="Orden:").pack(side="left", padx=(12, 0))
        self.cb_orden = ttk.Combobox(filtro, state="readonly", values=["Ascendente", "Descendente"], width=12)
        self.cb_orden.current(0)
        self.cb_orden.pack(side="left", padx=6)

        ttk.Button(filtro, text="Aplicar", command=self.cargar_tabla).pack(side="left", padx=6)

        # Tabla de discos
        cols = ("id", "nombre", "artista", "genero", "precio", "stock")
        self.tree = ttk.Treeview(master, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            ancho = 80 if c in ("id", "precio", "stock") else 160
            self.tree.column(c, width=ancho, anchor="w")
        self.tree.pack(expand=True, fill="both", padx=8, pady=8)

        # Botones
        acciones = ttk.Frame(master, padding=8)
        acciones.pack(side="bottom", fill="x")

        ttk.Button(acciones, text="Añadir disco", command=self.agregar_disco).pack(side="left")
        ttk.Button(acciones, text="Modificar disco", command=self.modificar_disco).pack(side="left", padx=6)
        ttk.Button(acciones, text="Eliminar disco", command=self.eliminar_disco).pack(side="left")
        ttk.Button(acciones, text="Añadir stock", command=self.anadir_stock).pack(side="left", padx=6)

        # Versión (esquina inferior derecha)
        self.lbl_version = ttk.Label(master, text=VERSION_APP)
        self.lbl_version.place(relx=1.0, rely=1.0, anchor="se", x=-6, y=-6)

        # Almacena en memoria la imformacion de los discos para el ordenamiento 
        self._memoria_discos = []
        self.cargar_tabla()

    # Herramientas en UI
    #Llama a DiscoRepo.listar(), que obtiene los discos desde la base de datos. Guarda esos discos en self._memoria_discos, que es como un "caché en memoria" para trabajar con ellos.
    def _leer_discos(self):
        self._memoria_discos = DiscoRepo.listar()
    #campo: por qué columna ordenar (id, nombre, artista, genero, stock). desc: si es True, ordenará en descendente; si es False, en ascendente.
    def _ordenar_informacion_discos(self):
        campo = self.cb_campo.get()
        desc = (self.cb_orden.get() == "Descendente")
        #Define una función que indica qué valor usar como clave para ordenar.
        def clave(row):
            if campo == "id":
                return int(row["id_disco"])
            if campo == "nombre":
                return normalizar_str(row["nombre_disco"]).lower()
            if campo == "artista":
                return normalizar_str(row["artista"]).lower()
            if campo == "genero":
                return normalizar_str(row["genero"]).lower()
            if campo == "stock":
                return int(row["stock"] or 0)
            return 0
        #Ordena la lista de discos con el algoritmo quicksort.
        self._memoria_discos = quicksort(self._memoria_discos, clave, reverse=desc)
    #método  que refresca la tabla de discos, los lee de la DB y ordena segun los metodos anteriores
    def cargar_tabla(self):
        try:
            self._leer_discos()
            self._ordenar_informacion_discos()
            # limpiar tabla
            for i in self.tree.get_children():
                self.tree.delete(i)
            # insertar discos ordenados segun usuario como treeview (tabla en tinker)
            for r in self._memoria_discos:
                self.tree.insert("", "end", values=(
                    r["id_disco"], r["nombre_disco"], r["artista"], r["genero"], r["precio"], r["stock"]
                ))
        except Exception as e:
            messagebox.showerror("BD", f"Error al cargar discos: {e}")

    # Funciones principales en UI
    def agregar_disco(self):
        try:
            nombre = simpledialog.askstring("Añadir", "Nombre del disco:")
            if not nombre:
                return
            artista = simpledialog.askstring("Añadir", "Artista:")
            if not artista:
                return
            genero = simpledialog.askstring("Añadir", "Género:")
            if not genero:
                return
            precio = simpledialog.askfloat("Añadir", "Precio:")
            if precio is None:
                return
            stock = simpledialog.askinteger("Añadir", "Stock inicial:", minvalue=0)
            if stock is None:
                return

            new_id = DiscoRepo.insertar(nombre, artista, genero, precio, stock)
            self.cargar_tabla()

            actividades_LOG(self.user["nombre_usuario"], "Añadir disco",
                         f"ID {new_id} | {nombre} - {artista} | género={genero}, precio={precio}, stock={stock}")
            messagebox.showinfo("Discos", "Disco agregado correctamente")
        except Exception as e:
            messagebox.showerror("Discos", f"No se pudo agregar el disco: {e}")

    def _get_sel(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Selecciona", "Elige un disco en la tabla")
            return None
        valores = self.tree.item(sel[0])["values"]
        return {
            "id_disco": valores[0],
            "nombre_disco": valores[1],
            "artista": valores[2],
            "genero": valores[3],
            "precio": valores[4],
            "stock": valores[5],
        }

    def modificar_disco(self):
        fila = self._get_sel()
        if not fila:
            return
        try:
            nuevo_nombre = simpledialog.askstring("Modificar", "Nombre:", initialvalue=fila["nombre_disco"])
            if nuevo_nombre is None:
                return
            nuevo_artista = simpledialog.askstring("Modificar", "Artista:", initialvalue=fila["artista"])
            if nuevo_artista is None:
                return
            nuevo_genero = simpledialog.askstring("Modificar", "Género:", initialvalue=fila["genero"])
            if nuevo_genero is None:
                return
            nuevo_precio = simpledialog.askfloat("Modificar", "Precio:", initialvalue=float(fila["precio"]))
            if nuevo_precio is None:
                return
            nuevo_stock = simpledialog.askinteger("Modificar", "Stock:", initialvalue=int(fila["stock"]))
            if nuevo_stock is None:
                return

            DiscoRepo.actualizar(fila["id_disco"], nuevo_nombre, nuevo_artista, nuevo_genero, nuevo_precio, nuevo_stock)
            self.cargar_tabla()

            cambios = []
            if nuevo_nombre != fila["nombre_disco"]:
                cambios.append(f"nombre: '{fila['nombre_disco']}'→'{nuevo_nombre}'")
            if nuevo_artista != fila["artista"]:
                cambios.append(f"artista: '{fila['artista']}'→'{nuevo_artista}'")
            if nuevo_genero != fila["genero"]:
                cambios.append(f"género: '{fila['genero']}'→'{nuevo_genero}'")
            if float(nuevo_precio) != float(fila["precio"]):
                cambios.append(f"precio: {fila['precio']}→{nuevo_precio}")
            if int(nuevo_stock) != int(fila["stock"]):
                cambios.append(f"stock: {fila['stock']}→{nuevo_stock}")

            actividades_LOG(self.user["nombre_usuario"], "Modificar disco",
                         f"ID {fila['id_disco']} | " + (", ".join(cambios) if cambios else "sin cambios"))
            messagebox.showinfo("Discos", "Disco actualizado")
        except Exception as e:
            messagebox.showerror("Discos", f"No se pudo modificar: {e}")

    def eliminar_disco(self):
        fila = self._get_sel()
        if not fila:
            return
        if not messagebox.askyesno("Eliminar", f"¿Eliminar '{fila['nombre_disco']}'?"):
            return
        try:
            DiscoRepo.eliminar(fila["id_disco"])
            self.cargar_tabla()
            actividades_LOG(self.user["nombre_usuario"], "Eliminar disco",
                         f"ID {fila['id_disco']} | {fila['nombre_disco']} - {fila['artista']}")
            messagebox.showinfo("Discos", "Disco eliminado")
        except Exception as e:
            messagebox.showerror("Discos", f"No se pudo eliminar: {e}")

    def anadir_stock(self):
        fila = self._get_sel()
        if not fila:
            return
        try:
            cant = simpledialog.askinteger("Añadir stock", "Cantidad a añadir:", minvalue=1)
            if not cant:
                return
            nuevo = DiscoRepo.sumar_stock(fila["id_disco"], cant)
            self.cargar_tabla()
            actividades_LOG(self.user["nombre_usuario"], "Añadir stock",
                         f"ID {fila['id_disco']} | {fila['nombre_disco']} | +{cant} → {nuevo}")
            messagebox.showinfo("Discos", f"Stock actualizado a {nuevo}")
        except Exception as e:
            messagebox.showerror("Discos", f"No se pudo actualizar el stock: {e}")

    def logout(self):
        actividades_LOG(self.user["nombre_usuario"], "Logout")
        self.master.destroy()
        root = tk.Tk()
        LoginUI(root)
        root.mainloop()

    def descargar_log(self):
        if descargar_log():
            actividades_LOG(self.user["nombre_usuario"], "Descargar log")

# MAIN
def main():
    auth = Auth()
    auth._crear_usuarios_por_defecto()  # crea usuarios por defecto si no existen
    auth.close()
    
    root = tk.Tk()
    LoginUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()