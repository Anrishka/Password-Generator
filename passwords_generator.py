# Генератор паролей

# Импорт необходимых библиотек
import random
import string
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sv_ttk
import ctypes

# Устанавливаем DpiAwareness для обеспечения совместимости с разными экранами
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(True)
except Exception:
    pass

# Создаем корневое окно Tkinter
root = Tk()
root.geometry('+700+400')  # Устанавливаем начальные координаты корневого окна
root.resizable(False, False)  # Запрещаем изменение размеров корневого окна
# Устанавливаем иконку для корневого окна
root.iconbitmap(r'C:\Users\user\Desktop\курс питон записи\GPT_tasks\password_generator\password.ico')
root.title('')  # Устанавливаем пустой заголовок для корневого окна

# Подключаемся к базе данных SQLite и создаем курсор для работы с ней
conn = sqlite3.connect('accounts.sqlite')
cursor = conn.cursor()

# Создаем таблицу в базе данных, если она не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY, 
    Website TEXT NOT NULL, 
    Login TEXT NOT NULL,
    Passwords TEXT NOT NULL
)
''')

# Функция создания нового аккаунта
def create_account():
    # Внутренняя функция для получения пароля
    def get_password():
        # Внутренняя функция для закрытия окна нового пароля
        def close_new_password_window():
            new_password.destroy()

        # Внутренняя функция для показа пароля
        def show_password():
            if password_entry['show'] == '':
                password_entry['show'] = '*'
                show_password_button['text'] = 'Показать пароль'
            else:
                password_entry['show'] = ''
                show_password_button['text'] = 'Скрыть пароль'

        # Создаем новое окно Toplevel для ввода данных нового аккаунта
        new_password = Toplevel(root)
        new_password.geometry('+700+400')
        new_password.grab_set()
        new_password.resizable(False, False)
        new_password.iconbitmap(r'C:\Users\user\Desktop\курс питон записи\GPT_tasks\password_generator\password.ico')
        new_password.title('')

        # Получаем данные от пользователя
        web_site = website.get()
        log_in = login.get()
        password_len1 = password_len.get()

        try:
            int(password_len1)
        except ValueError:
            new_password.destroy()
            account_creation.grab_set()
            messagebox.showerror('ValueError', 'Длина пароля должна быть в виде целого числа.')

        # Генерируем пароль
        everything = string.punctuation + string.digits + string.ascii_letters
        password_list = [random.choice(everything) for _ in range(int(password_len1))]
        password = ''.join(password_list)

        # Проверяем длину пароля
        if len(password) >= 31:
            new_password.destroy()
            account_creation.grab_set()
            messagebox.showerror('ValueError', 'Длина пароля не должна превышать 30 символов.')
        else:
            pass

        # Добавляем данные в базу данных
        cursor.execute('INSERT INTO passwords (Website, Login, Passwords) VALUES (?, ?, ?)',
                       (web_site, log_in, password))
        conn.commit()

        # Создаем и размещаем виджеты для отображения данных
        website1_label = ttk.Label(new_password, text='Сайт:')
        website1_label.grid(column=0, row=1, sticky=W, pady=10, padx=10)
        website1 = ttk.Entry(new_password, width=30)
        website1.grid(column=0, row=2, padx=10, pady=10)

        login1_label = ttk.Label(new_password, text='Логин:')
        login1_label.grid(column=0, row=3, sticky=W, pady=10, padx=10)
        login1 = ttk.Entry(new_password, width=30)
        login1.grid(column=0, row=4, padx=10, pady=10)

        password_label = ttk.Label(new_password, text='Пароль:')
        password_label.grid(column=0, row=5, sticky=W, pady=10, padx=10)
        password_entry = ttk.Entry(new_password, width=30, show='*')
        password_entry.grid(column=0, row=6, padx=10, pady=10)

        website1.insert(0, web_site)
        login1.insert(0, log_in)
        password_entry.insert(0, password)

        show_password_button = ttk.Button(new_password, text='Показать пароль', command=show_password)
        show_password_button.grid(column=0, row=7, pady=10, padx=10)

        close_new_password = ttk.Button(new_password, text='Закрыть', command=close_new_password_window)
        close_new_password.grid(column=0, row=8, pady=10, padx=10)

        account_creation.destroy()

        messagebox.showinfo('Создание аккаунта', 'Аккаунт успешно создан и сохранён!')

    # Создаем новое окно Toplevel для ввода данных нового аккаунта
    account_creation = Toplevel()
    account_creation.geometry('+700+400')
    account_creation.grab_set()
    account_creation.resizable(False, False)
    account_creation.iconbitmap(r'C:\Users\user\Desktop\курс питон записи\GPT_tasks\password_generator\password.ico')
    account_creation.title('')

    # Создаем и размещаем виджеты для ввода данных нового аккаунта
    website_label = ttk.Label(account_creation, text='Введите название сайта:')
    website_label.grid(column=0, row=1, sticky=W, pady=10, padx=10)
    website = ttk.Entry(account_creation, width=30)
    website.grid(column=0, row=2, padx=10, pady=10)

    login_label = ttk.Label(account_creation, text='Введите логин:')
    login_label.grid(column=0, row=3, sticky=W, pady=10, padx=10)
    login = ttk.Entry(account_creation, width=30)
    login.grid(column=0, row=4, padx=10, pady=10)

    password_len_label = ttk.Label(account_creation, text='Введите длину пароля:')
    password_len_label.grid(column=0, row=5, sticky=W, pady=10, padx=10)
    password_len = ttk.Entry(account_creation, width=30)
    password_len.grid(column=0, row=6, padx=10, pady=10)

    get_password_button = ttk.Button(account_creation, text='Получить пароль', command=get_password)
    get_password_button.grid(column=0, row=7, pady=15)

# Функция отображения аккаунтов
def show_accounts():
    # Внутренняя функция для удаления аккаунта
    def delete_account(account_id):
        cursor.execute('DELETE FROM passwords WHERE id = ?', (account_id,))
        conn.commit()
        accounts_window.destroy()
        show_accounts()

    # Создаем новое окно Toplevel для отображения аккаунтов
    accounts_window = Toplevel()
    accounts_window.geometry('+700+400')
    accounts_window.grab_set()
    accounts_window.resizable(False, False)
    accounts_window.iconbitmap(r'C:\Users\user\Desktop\курс питон записи\GPT_tasks\password_generator\password.ico')
    accounts_window.title('')

    # Получаем данные из базы данных
    cursor.execute('SELECT * FROM passwords')
    all_data = cursor.fetchall()

    # Если нет аккаунтов, выводим сообщение
    if len(all_data) == 0:
        no_accounts_label = Label(accounts_window, text='На данный момент в базе нет аккаунтов')
        no_accounts_label.grid(row=1)
        close_button = Button(accounts_window, text='Закрыть', command=accounts_window.destroy)
        close_button.grid(row=3, columnspan=3, pady=10)
    else:
        # Если есть аккаунты, отображаем их
        for i, data in enumerate(all_data, start=1):
            website = data[1]
            login = data[2]
            password = data[3]

            website_label = ttk.Label(accounts_window, text=f'Аккаунт #{i}: {website}', font='Ariel 10 bold')
            website_label.grid(row=i, column=0, sticky=W, padx=10, pady=10)

            login_entry = ttk.Entry(accounts_window)
            login_entry.insert(0, login)
            login_entry.grid(row=i, column=1, padx=10, pady=10)

            password_entry = ttk.Entry(accounts_window)
            password_entry.insert(0, password)
            password_entry.grid(row=i, column=2, padx=10, pady=10)

            # Создаем кнопку для удаления аккаунта
            delete = Button(accounts_window, text='Удалить', command=lambda id=data[0]: delete_account(id))
            delete.grid(row=i, column=3, padx=10, pady=10)

        close_button = Button(accounts_window, text='Закрыть', command=accounts_window.destroy)
        close_button.grid(row=len(all_data) + 2, columnspan=3, padx=10, pady=10)


# Функция для выхода из программы
def exit_program():
    root.destroy()

# Создаем кнопки для взаимодействия с программой
create_account_button = ttk.Button(text='Создать новый аккаунт', width=20, command=create_account)
create_account_button.grid(column=1, row=1, padx=18, pady=10)

show_accounts_button = ttk.Button(text='Показать аккаунты', width=20, command=show_accounts)
show_accounts_button.grid(column=1, row=2, padx=18, pady=10)

exit_program = ttk.Button(text='Выйти из программы', width=20, command=exit_program)
exit_program.grid(column=1, row=3, padx=18, pady=10)

# Устанавливаем тему для виджетов ttk
sv_ttk.set_theme("dark")

# Запускаем цикл событий Tkinter
root.mainloop()



























































