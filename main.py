import tkinter as tk
from tkinter import ttk
import sqlite3


# Создание главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.tree = ttk.Treeview(root,
                                 columns=('id', 'name', 'phone', 'email', 'salary'),
                                 height=45, show='headings')
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        self.search_img = tk.PhotoImage(file='./img/search.png')
        self.del_img = tk.PhotoImage(file='./img/delete.png')
        self.edit_img = tk.PhotoImage(file='./img/update.png')
        self.add_img = tk.PhotoImage(file='./img/add.png')
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='slategray', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        btn_add = tk.Button(toolbar, bg='slategray', bd=0,
                            image=self.add_img,
                            command=self.open_dialog)
        btn_add.pack(side=tk.LEFT)

        # Создание кнопки редактирования сотрудника
        btn_edit = tk.Button(toolbar, bg='slategray', bd=0,
                             image=self.edit_img,
                             command=self.open_edit)
        btn_edit.pack(side=tk.LEFT)
        # Создание кнопки удаления сотрудника
        btn_del = tk.Button(toolbar, bg='slategray', bd=0,
                            image=self.del_img,
                            command=self.delete_records)
        btn_del.pack(side=tk.LEFT)
        # Создание кнопки поиска сотрудника
        btn_search = tk.Button(toolbar, bg='slategray', bd=0,
                               image=self.search_img,
                               command=self.open_search)
        btn_search.pack(side=tk.LEFT)

        # Создание кнопки обновления таблицы
        btn_refresh = tk.Button(toolbar, bg='slategray', bd=0,
                                image=self.refresh_img,
                                command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # Настройка отображения таблицы
        self.tree.column('id', width=125, anchor=tk.CENTER)
        self.tree.column('name', width=125, anchor=tk.CENTER)
        self.tree.column('phone', width=125, anchor=tk.CENTER)
        self.tree.column('email', width=125, anchor=tk.CENTER)
        self.tree.column('salary', width=125, anchor=tk.CENTER)

        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='Эл. Почта')
        self.tree.heading('salary', text='Зарплата')
        self.tree.pack(side=tk.LEFT)
        scroll = tk.Scrollbar(root, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # Метод добавления сотрудника
    def records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()
        self.db.conn.commit()

    # Метод редактирования
    def edit_record(self, name, phone, email, salary):
        ind = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute('''
            UPDATE Users SET name = ?, phone = ?, email = ?, salary = ?
            WHERE id = ?
        ''', (name, phone, email, salary, ind))
        self.db.conn.commit()
        self.view_records()

    # Метод удаления записей
    def delete_records(self):
        for i in self.tree.selection():
            id = self.tree.set(i, '#1')
            self.db.cur.execute('''
                DELETE FROM Users
                WHERE id = ?
            ''', (id,))
        self.db.conn.commit()
        self.view_records()

    # Метод поиска записей
    def search_records(self, name):
        [self.tree.delete(i) for i in self.tree.get_children()]
        self.db.cur.execute('SELECT * FROM Users WHERE name LIKE ?',
                            ('%' + name + '%',))
        [self.tree.insert('', 'end', values=i) for i in self.db.cur.fetchall()]

    def open_dialog(self):
        Add()
        # child.init_child()

    def open_edit(self):
        Update()

    def open_search(self):
        Search()

    # Метод поиска
    def view_records(self):
        [self.tree.delete(i) for i in self.tree.get_children()]
        self.db.cur.execute('SELECT *FROM Users')
        [self.tree.insert('', 'end', values=i) for i in self.db.cur.fetchall()]


# Класс окна добавления
class Add(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.btn_ok = tk.Button(self, text='Готово', command=self.add_contact)
        self.entry_salary = tk.Entry(self)
        self.entry_email = tk.Entry(self)
        self.entry_phone = tk.Entry(self)
        self.entry_name = tk.Entry(self)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавление сотрудника')
        self.geometry('400x200')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text='Телефон')
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text='Эл. Почта')
        label_email.place(x=50, y=110)
        label_salary = tk.Label(self, text='Зарплата')
        label_salary.place(x=50, y=140)
        self.entry_name.place(x=200, y=50)
        self.entry_phone.place(x=200, y=80)
        self.entry_email.place(x=200, y=110)
        self.entry_salary.place(x=200, y=135)

        self.btn_ok.place(x=300, y=160)
        btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=220, y=160)

    def add_contact(self):  # Метод добавления
        self.view.records(
            self.entry_name.get(),
            self.entry_phone.get(),
            self.entry_email.get(),
            self.entry_salary.get()
        )


# Класс окна обновления
class Update(Add):
    def __init__(self):
        super().__init__()
        self.db = db
        self.init_edit()
        self.load_data()

    def init_edit(self):
        self.title('Редактирование сотрудника')
        self.btn_ok.destroy()
        self.btn_ok = tk.Button(self, text='Готово')
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.edit_record(
            self.entry_name.get(), self.entry_phone.get(),
            self.entry_email.get(), self.entry_salary.get()))

        self.btn_ok.bind('<Button-1>', lambda ev: self.destroy(),
                         add='+')
        self.btn_ok.place(x=300, y=160)

    # Метод автозаполнения
    def load_data(self):
        self.db.cur.execute('''SELECT * FROM Users WHERE id = ?''',
                            self.view.tree.set(self.view.tree.selection()[0], '#1'))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])


# Класс окна поиска сотрудников
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.btn_ok = tk.Button(self, text='Найти')
        self.entry_name = tk.Entry(self)
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск сотрудника')
        self.geometry('300x100')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        # Создание формы
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=50, y=30)
        self.entry_name.place(x=150, y=30)
        self.btn_ok.bind('<Button-1>',
                         lambda ev: self.view.search_records(self.entry_name.get()))
        self.btn_ok.bind('<Button-1>',
                         lambda ev: self.destroy(), add='+')
        self.btn_ok.place(x=230, y=70)
        btn_cancel = tk.Button(self, text='Закрыть',
                               command=self.destroy)
        btn_cancel.place(x=160, y=70)


# Класс БД
class Db:
    def __init__(self):
        self.conn = sqlite3.connect('Employees.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''
                CREATE TABLE IF NOT EXISTS Users(
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        phone TEXT,
                        email TEXT,
                        salary INTEGER
                        )''')

    # Метод добавления данных в БД
    def insert_data(self, name, phone, email, salary):
        self.cur.execute('''
            INSERT INTO Users (name, phone, email, salary) 
            VALUES (?,?,?,?)''', (name, phone, email, salary))


# Основной цикл
if __name__ == '__main__':
    root = tk.Tk()
    db = Db()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников компании')
    root.geometry('655x400')
    root.resizable(False, False)
    root.protocol('WM_DELETE_WINDOW', app.quit)
    root.mainloop()
