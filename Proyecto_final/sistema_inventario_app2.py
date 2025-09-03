import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib
from datetime import datetime

# =============================
# Configuración de la Base de Datos
# =============================
DB_NAME = "inventario_discos"
DB_USER = "postgres"
DB_PASS = "Soysuficiente91*"  # <--- CAMBIA AQUÍ TU CONTRASEÑA
DB_HOST = "localhost"
DB_PORT = 5432

# =============================
# Utilidades
# =============================

def hash_password(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def default_password_from_nombre_usuario(nombre_usuario: str) -> str:
    # Regla: contraseña = primer nombre en minúsculas + "123"
    # Ej: "Carlos Pérez" -> "carlos123"
    primer_nombre = (nombre_usuario.strip().split()[0] if nombre_usuario else "").lower()
    return primer_nombre + "123"


def quicksort(lista, key_fn, reverse=False):
    if len(lista) <= 1:
        return lista
    pivote = lista[len(lista)//2]
    k = key_fn(pivote)
    menores = [x for x in lista if key_fn(x) < k]
    iguales = [x for x in lista if key_fn(x) == k]
    mayores = [x for x in lista if key_fn(x) > k]
    res = quicksort(menores, key_fn) + iguales + quicksort(mayores, key_fn)
    return list(reversed(res)) if reverse else res

# =============================
# Capa de Datos
# =============================
class Database:
    _instance = None


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._conn = None
        return cls._instance

    def connect(self):
        if self._conn is None or self._conn.closed:
            self._conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                host=DB_HOST,
                port=DB_PORT
            )
            self._conn.autocommit = True
        return self._conn

    def cursor(self):
        return self.connect().cursor(cursor_factory=RealDictCursor)

    def commit(self):
        if self._conn:
            self._conn.commit()

# =============================
# Autenticación y Gestión de Usuarios
# =============================
class AuthManager:
    def __init__(self):
        self.db = Database()
        self.ensure_perfiles()
        self.ensure_default_users()
        self.sync_new_users_passwords()  # Auto-crea contraseñas para usuarios nuevos en BD

    def ensure_perfiles(self):
        cur = self.db.cursor()
        # Asegura que existan 1=Gerencia, 2=Bodega, 3=Vendedores
        cur.execute("""
            INSERT INTO perfil (id_perfil, nombre_perfil) VALUES
            (1,'Gerencia') ON CONFLICT (id_perfil) DO NOTHING;
        """)
        cur.execute("""
            INSERT INTO perfil (id_perfil, nombre_perfil) VALUES
            (2,'Bodega') ON CONFLICT (id_perfil) DO NOTHING;
        """)
        cur.execute("""
            INSERT INTO perfil (id_perfil, nombre_perfil) VALUES
            (3,'Vendedores') ON CONFLICT (id_perfil) DO NOTHING;
        """)

    def ensure_default_users(self):
        """Crea 1 usuario Gerencia, 2 Bodega, 3 Vendedores si no existen."""
        cur = self.db.cursor()
        defaults = [
            ("Ana Gerente", "ana.gerente@demo.com", 1),
            ("Luis Bodega", "luis.bodega@demo.com", 2),
            ("Marta Bodega", "marta.bodega@demo.com", 2),
            ("Carlos Vendedor", "carlos.vendedor@demo.com", 3),
            ("Sofía Vendedora", "sofia.vendedora@demo.com", 3),
            ("Pedro Vendedor", "pedro.vendedor@demo.com", 3),
        ]
        for nombre, correo, perfil in defaults:
            cur.execute("SELECT id_usuario FROM usuario WHERE nombre_usuario=%s", (nombre,))
            row = cur.fetchone()
            if not row:
                cur.execute(
                    "INSERT INTO usuario (nombre_usuario, correo, id_perfil1) VALUES (%s,%s,%s) RETURNING id_usuario",
                    (nombre, correo, perfil)
                )
                new_id = cur.fetchone()["id_usuario"]
                # Crear contraseña por regla
                pwd = default_password_from_nombre_usuario(nombre)
                cur.execute(
                    "INSERT INTO auth (id_usuario, password_hash) VALUES (%s,%s)",
                    (new_id, hash_password(pwd))
                )

    def sync_new_users_passwords(self):
        """Para cada usuario sin fila en auth, crea password_hash = primer_nombre+123."""
        cur = self.db.cursor()
        cur.execute(
            """
            SELECT u.id_usuario, u.nombre_usuario
            FROM usuario u
            LEFT JOIN auth a ON a.id_usuario = u.id_usuario
            WHERE a.id_usuario IS NULL
            """
        )
        rows = cur.fetchall()
        for r in rows:
            pwd = default_password_from_nombre_usuario(r["nombre_usuario"])  # regla
            cur.execute(
                "INSERT INTO auth (id_usuario, password_hash) VALUES (%s,%s)",
                (r["id_usuario"], hash_password(pwd))
            )

    def authenticate(self, nombre_usuario: str, password: str):
        # Sincroniza por si hay usuarios nuevos recién agregados
        self.sync_new_users_passwords()
        cur = self.db.cursor()
        cur.execute(
            """
            SELECT u.id_usuario, u.nombre_usuario, u.id_perfil1, p.nombre_perfil, a.password_hash
            FROM usuario u
            JOIN perfil p ON p.id_perfil = u.id_perfil1
            JOIN auth a   ON a.id_usuario = u.id_usuario
            WHERE u.nombre_usuario = %s
            """,
            (nombre_usuario,)
        )
        row = cur.fetchone()
        if row and row["password_hash"] == hash_password(password):
            return {
                "id": row["id_usuario"],
                "nombre": row["nombre_usuario"],
                "perfil": row["id_perfil1"],
                "perfil_nombre": row["nombre_perfil"],
            }
        return None

    def add_user(self, nombre_usuario: str, correo: str, perfil: int, password: str | None = None):
        cur = self.db.cursor()
        try:
            cur.execute(
                "INSERT INTO usuario (nombre_usuario, correo, id_perfil1) VALUES (%s,%s,%s) RETURNING id_usuario",
                (nombre_usuario, correo, perfil)
            )
            new_id = cur.fetchone()["id_usuario"]
            pwd = password or default_password_from_nombre_usuario(nombre_usuario)
            cur.execute(
                "INSERT INTO auth (id_usuario, password_hash) VALUES (%s,%s)",
                (new_id, hash_password(pwd))
            )
            messagebox.showinfo("Usuario creado", f"Usuario: {nombre_usuario} Contraseña: {pwd}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el usuario: {e}")
            return False

    def delete_user(self, nombre_usuario: str):
        cur = self.db.cursor()
        try:
            cur.execute("SELECT id_usuario FROM usuario WHERE nombre_usuario=%s", (nombre_usuario,))
            row = cur.fetchone()
            if not row:
                messagebox.showwarning("Atención", "Usuario no encontrado")
                return False
            uid = row["id_usuario"]
            cur.execute("DELETE FROM auth WHERE id_usuario=%s", (uid,))
            cur.execute("DELETE FROM usuario WHERE id_usuario=%s", (uid,))
            messagebox.showinfo("OK", "Usuario eliminado")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")
            return False

# =============================
# Repositorio de Discos
# =============================
class DiscoRepository:
    def __init__(self):
        self.db = Database()

    def list_all(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM disco_musica ORDER BY id_disco")
        return cur.fetchall()

    def search(self, texto: str):
        cur = self.db.cursor()
        like = f"%{texto.lower()}%"
        cur.execute(
            """
            SELECT * FROM disco_musica
            WHERE LOWER(nombre_disco) LIKE %s
               OR LOWER(artista) LIKE %s
               OR LOWER(genero) LIKE %s
            ORDER BY id_disco
            """,
            (like, like, like)
        )
        return cur.fetchall()

    def get_by_id(self, id_disco: int):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM disco_musica WHERE id_disco=%s", (id_disco,))
        return cur.fetchone()

    def add(self, nombre, precio, artista, fecha, peso_mb, genero, stock=0):
        cur = self.db.cursor()
        cur.execute(
            """
            INSERT INTO disco_musica (nombre_disco, precio, artista, fecha_lanzamiento, peso_mb, genero, stock)
            VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id_disco
            """,
            (nombre, precio, artista, fecha, peso_mb, genero, stock)
        )
        return cur.fetchone()["id_disco"]

    def update(self, id_disco, nombre, precio, artista, fecha, peso_mb, genero, stock):
        cur = self.db.cursor()
        cur.execute(
            """
            UPDATE disco_musica
            SET nombre_disco=%s, precio=%s, artista=%s, fecha_lanzamiento=%s, peso_mb=%s, genero=%s, stock=%s
            WHERE id_disco=%s
            """,
            (nombre, precio, artista, fecha, peso_mb, genero, stock, id_disco)
        )

    def delete(self, id_disco):
        cur = self.db.cursor()
        cur.execute("DELETE FROM disco_musica WHERE id_disco=%s", (id_disco,))

    def add_stock(self, id_disco: int, cantidad: int, id_usuario: int):
        cur = self.db.cursor()
        cur.execute("UPDATE disco_musica SET stock = stock + %s WHERE id_disco=%s RETURNING stock", (cantidad, id_disco))
        nuevo = cur.fetchone()["stock"]
        # Registrar movimiento
        cur.execute(
            "INSERT INTO movimiento_inventario (id_usuario, id_disco, tipo, cantidad) VALUES (%s,%s,'entrada',%s)",
            (id_usuario, id_disco, cantidad)
        )
        return nuevo

# =============================
# Logger de Actividades (archivo .txt descargable)
# =============================
class ActivityLogger:
    def __init__(self, username: str):
        self.username = username
        self.log_path = "activity_log.txt"

    def log(self, action: str, detail: str):
        t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{t}] Usuario: {self.username} | Acción: {action} | Detalles: {detail}"
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(line)

    def export(self):
        ruta = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            filetypes=[("Texto", "*.txt")]
        )
        if ruta:
            try:
                with open(self.log_path, "r", encoding="utf-8") as fsrc, open(ruta, "w", encoding="utf-8") as fdst:
                    fdst.write(fsrc.read())
                messagebox.showinfo("OK", f"Log guardado en {ruta}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

# =============================
# Editor de Discos (Toplevel)
# =============================
class DiscEditor(tk.Toplevel):
    def __init__(self, master, row=None):
        super().__init__(master)
        self.title("Editar Disco" if row else "Agregar Disco")
        self.resizable(False, False)
        self.result = None

        labels = [
            ("Nombre", 0), ("Precio", 1), ("Artista", 2), ("Fecha (YYYY-MM-DD)", 3),
            ("Peso (MB)", 4), ("Género", 5), ("Stock", 6)
        ]
        for text, r in labels:
            ttk.Label(self, text=text).grid(row=r, column=0, sticky="e", padx=6, pady=4)

        self.e_nombre = ttk.Entry(self); self.e_nombre.grid(row=0, column=1, padx=6, pady=4)
        self.e_precio = ttk.Entry(self); self.e_precio.grid(row=1, column=1, padx=6, pady=4)
        self.e_artista = ttk.Entry(self); self.e_artista.grid(row=2, column=1, padx=6, pady=4)
        self.e_fecha = ttk.Entry(self); self.e_fecha.grid(row=3, column=1, padx=6, pady=4)
        self.e_peso  = ttk.Entry(self); self.e_peso.grid(row=4, column=1, padx=6, pady=4)
        self.e_genero= ttk.Entry(self); self.e_genero.grid(row=5, column=1, padx=6, pady=4)
        self.e_stock = ttk.Entry(self); self.e_stock.grid(row=6, column=1, padx=6, pady=4)

        if row:
            self.e_nombre.insert(0, row["nombre_disco"])
            self.e_precio.insert(0, str(row["precio"]))
            self.e_artista.insert(0, row["artista"])
            self.e_fecha.insert(0, str(row["fecha_lanzamiento"]))
            self.e_peso.insert(0, str(row["peso_mb"]))
            self.e_genero.insert(0, row["genero"] or "")
            self.e_stock.insert(0, str(row["stock"]))

        ttk.Button(self, text="Guardar", command=self.on_save).grid(row=7, column=0, columnspan=2, pady=8)

    def on_save(self):
        try:
            nombre = self.e_nombre.get().strip()
            precio = float(self.e_precio.get()) if self.e_precio.get() else None
            artista= self.e_artista.get().strip()
            fecha  = self.e_fecha.get().strip() or None
            peso   = float(self.e_peso.get()) if self.e_peso.get() else None
            genero = self.e_genero.get().strip() or None
            stock  = int(self.e_stock.get() or 0)
            if not nombre:
                messagebox.showwarning("Validación", "Nombre requerido")
                return
            self.result = (nombre, precio, artista, fecha, peso, genero, stock)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")

# =============================
# Aplicación Principal
# =============================
class MainApp:
    def __init__(self, user):
        self.user = user
        self.db = Database()
        self.auth = AuthManager()
        self.repo = DiscoRepository()
        self.logger = ActivityLogger(user["nombre"])

        self.root = tk.Tk()
        self.root.title("FloydMusic — Inventario")
        self.root.geometry("1100x640")

        # ======= BARRA SUPERIOR =======
        top = ttk.Frame(self.root, padding=6)
        top.pack(side="top", fill="x")
        ttk.Label(top, text=f"Bienvenido: {user['nombre']} ({user['perfil_nombre']})", font=("Arial", 12, "bold")).pack(side="left")
        ttk.Button(top, text="Generar Log", command=self.on_export_log).pack(side="right", padx=4)
        ttk.Button(top, text="Cerrar Sesión", command=self.logout).pack(side="right", padx=4)
        if user["perfil"] == 1:
            ttk.Button(top, text="Gestionar Usuarios", command=self.open_user_admin).pack(side="right", padx=4)

        # ======= CONTROLES DE BÚSQUEDA / ORDEN =======
        ctrl = ttk.Frame(self.root, padding=6)
        ctrl.pack(side="top", fill="x")
        ttk.Label(ctrl, text="Buscar:").pack(side="left")
        self.var_search = tk.StringVar()
        ttk.Entry(ctrl, textvariable=self.var_search, width=40).pack(side="left", padx=4)
        ttk.Button(ctrl, text="Ir", command=self.on_search).pack(side="left")

        ttk.Label(ctrl, text=" | Ordenar por:").pack(side="left", padx=(12, 4))
        self.var_field = tk.StringVar(value="id")
        self.cbo_field = ttk.Combobox(ctrl, width=12, state="readonly",
                                      values=["id", "nombre", "artista", "genero", "stock"],
                                      textvariable=self.var_field)
        self.cbo_field.pack(side="left")
        self.var_desc = tk.BooleanVar(value=False)
        ttk.Checkbutton(ctrl, text="Desc", variable=self.var_desc).pack(side="left", padx=4)
        ttk.Button(ctrl, text="Ordenar (QuickSort)", command=self.on_sort).pack(side="left", padx=8)

        # ======= TREEVIEW =======
        cols = ("id", "nombre", "precio", "artista", "fecha", "peso", "genero", "stock")
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=120 if c != "nombre" else 200, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=6, pady=6)

        # ======= BOTONES DE ACCIÓN =======
        bar = ttk.Frame(self.root, padding=6)
        bar.pack(side="bottom", fill="x")
        ttk.Button(bar, text="Añadir disco", command=self.on_add).pack(side="left")
        ttk.Button(bar, text="Modificar disco", command=self.on_edit).pack(side="left", padx=6)
        ttk.Button(bar, text="Eliminar disco", command=self.on_delete).pack(side="left")
        ttk.Button(bar, text="Añadir stock", command=self.on_add_stock).pack(side="left", padx=6)

        # ======= VERSION EN ESQUINA INFERIOR DERECHA =======
        self.lbl_ver = ttk.Label(self.root, text="Versión 1.0")
        self.lbl_ver.place(relx=1.0, rely=1.0, anchor="se")

        self.discos_cache = []
        self.load_all()
        self.root.mainloop()

    # --------- utilidades UI ---------
    def clear_tree(self):
        for it in self.tree.get_children():
            self.tree.delete(it)

    def push_rows(self, rows):
        self.clear_tree()
        for r in rows:
            self.tree.insert("", "end", values=(
                r["id_disco"], r["nombre_disco"],
                (f"${float(r['precio']):.2f}" if r["precio"] is not None else ""),
                r["artista"], r["fecha_lanzamiento"], r["peso_mb"], r.get("genero", ""), r["stock"]
            ))

    def load_all(self):
        self.discos_cache = self.repo.list_all()
        self.push_rows(self.discos_cache)

    # --------- acciones ---------
    def on_search(self):
        txt = self.var_search.get().strip()
        if not txt:
            self.load_all()
            return
        rows = self.repo.search(txt)
        self.discos_cache = rows
        self.push_rows(rows)

    def on_sort(self):
        campo = self.var_field.get()
        desc = self.var_desc.get()
        keymap = {
            "id": lambda r: r["id_disco"],
            "nombre": lambda r: (r["nombre_disco"] or "").lower(),
            "artista": lambda r: (r["artista"] or "").lower(),
            "genero": lambda r: (r.get("genero") or "").lower(),
            "stock": lambda r: int(r["stock"] or 0),
        }
        ordenados = quicksort(list(self.discos_cache), keymap[campo], reverse=desc)
        self.push_rows(ordenados)

    def on_add(self):
        dlg = DiscEditor(self.root)
        self.root.wait_window(dlg)
        if dlg.result:
            nombre, precio, artista, fecha, peso, genero, stock = dlg.result
            try:
                new_id = self.repo.add(nombre, precio, artista, fecha, peso, genero, stock)
                self.logger.log("Agregar disco", f"ID {new_id} · {nombre} · {artista} · stock {stock}")
                messagebox.showinfo("OK", "Disco agregado")
                self.load_all()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def on_edit(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un disco")
            return
        item = self.tree.item(sel[0])
        id_disco = int(item["values"][0])
        row = self.repo.get_by_id(id_disco)
        dlg = DiscEditor(self.root, row)
        self.root.wait_window(dlg)
        if dlg.result:
            nombre, precio, artista, fecha, peso, genero, stock = dlg.result
            try:
                self.repo.update(id_disco, nombre, precio, artista, fecha, peso, genero, stock)
                self.logger.log("Modificar disco", f"ID {id_disco} → {nombre}/{artista}/stock {stock}")
                messagebox.showinfo("OK", "Disco actualizado")
                self.load_all()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def on_delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un disco")
            return
        item = self.tree.item(sel[0])
        id_disco = int(item["values"][0])
        row = self.repo.get_by_id(id_disco)
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{row['nombre_disco']}' de {row['artista']}?"):
            try:
                self.repo.delete(id_disco)
                self.logger.log("Eliminar disco", f"ID {id_disco} · {row['nombre_disco']}")
                messagebox.showinfo("OK", "Disco eliminado")
                self.load_all()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def on_add_stock(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un disco")
            return
        item = self.tree.item(sel[0])
        id_disco = int(item["values"][0])
        row = self.repo.get_by_id(id_disco)
        cantidad = simpledialog.askinteger("Añadir Stock", f"¿Cuántas unidades añadir a '{row['nombre_disco']}'?", minvalue=1)
        if not cantidad:
            return
        try:
            nuevo = self.repo.add_stock(id_disco, cantidad, self.user["id"])
            self.logger.log("Añadir stock", f"ID {id_disco} +{cantidad} (nuevo stock={nuevo})")
            messagebox.showinfo("OK", f"Stock actualizado: {nuevo}")
            self.load_all()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_export_log(self):
        self.logger.export()

    def logout(self):
        self.root.destroy()
        LoginWindow()  # volver al login

# =============================
# Admin de Usuarios (solo Gerencia)
# =============================
class UserAdmin(tk.Toplevel):
    def __init__(self, master, auth: AuthManager):
        super().__init__(master)
        self.title("Gestión de Usuarios")
        self.auth = auth
        self.resizable(False, False)

        ttk.Label(self, text="Nombre y Apellido").grid(row=0, column=0, sticky="e", padx=6, pady=4)
        ttk.Label(self, text="Correo").grid(row=1, column=0, sticky="e", padx=6, pady=4)
        ttk.Label(self, text="Perfil (1=Gerencia,2=Bodega,3=Vendedores)").grid(row=2, column=0, sticky="e", padx=6, pady=4)
        ttk.Label(self, text="Contraseña (opcional)").grid(row=3, column=0, sticky="e", padx=6, pady=4)

        self.e_nombre = ttk.Entry(self, width=30); self.e_nombre.grid(row=0, column=1, padx=6, pady=4)
        self.e_correo = ttk.Entry(self, width=30); self.e_correo.grid(row=1, column=1, padx=6, pady=4)
        self.e_perfil = ttk.Entry(self, width=10); self.e_perfil.grid(row=2, column=1, padx=6, pady=4, sticky="w")
        self.e_pass   = ttk.Entry(self, width=30, show="*"); self.e_pass.grid(row=3, column=1, padx=6, pady=4)

        ttk.Button(self, text="Agregar Usuario", command=self.add_user).grid(row=4, column=0, pady=8)
        ttk.Button(self, text="Eliminar Usuario", command=self.delete_user).grid(row=4, column=1, pady=8)

    def add_user(self):
        nombre = self.e_nombre.get().strip()
        correo = self.e_correo.get().strip()
        try:
            perfil = int(self.e_perfil.get().strip())
        except:
            messagebox.showwarning("Validación", "Perfil inválido")
            return
        pwd = self.e_pass.get().strip() or None
        if self.auth.add_user(nombre, correo, perfil, pwd):
            messagebox.showinfo("OK", "Usuario agregado")

    def delete_user(self):
        nombre = self.e_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Validación", "Indique el nombre de usuario a eliminar")
            return
        self.auth.delete_user(nombre)

# =============================
# Login
# =============================
class LoginWindow:
    def __init__(self):
        self.auth = AuthManager()

        self.win = tk.Tk()
        self.win.title("FloydMusic — Login")
        self.win.geometry("420x200")

        frm = ttk.Frame(self.win, padding=12)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Usuario (Nombre y Apellido)").grid(row=0, column=0, sticky="e", pady=6)
        ttk.Label(frm, text="Contraseña (primer_nombre + 123)").grid(row=1, column=0, sticky="e", pady=6)

        self.e_user = ttk.Entry(frm, width=30); self.e_user.grid(row=0, column=1, padx=6)
        self.e_pass = ttk.Entry(frm, width=30, show="*"); self.e_pass.grid(row=1, column=1, padx=6)
        ttk.Button(frm, text="Ingresar", command=self.try_login).grid(row=2, column=0, columnspan=2, pady=12)

       

        self.win.mainloop()

    def try_login(self):
        u = self.e_user.get().strip()
        p = self.e_pass.get().strip()
        user = self.auth.authenticate(u, p)
        if user:
            self.win.destroy()
            MainApp(user)
        else:
            messagebox.showerror("Login", "Usuario o contraseña incorrectos")

# =============================
# Helpers
# =============================
    

def abrir_admin_usuarios(root, auth):
    UserAdmin(root, auth)

# Vincular método al MainApp
MainApp.open_user_admin = lambda self: UserAdmin(self.root, self.auth)

# =============================
# Entry point
# =============================
if __name__ == "__main__":
    LoginWindow()
