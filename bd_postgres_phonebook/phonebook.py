import psycopg2
from tkinter import *
from tkinter.ttk import Combobox, Style
import copy


connection = psycopg2.connect(dbname='phonebook',
                              host='localhost',
                              user='postgres',
                              password='4789')
curr = connection.cursor()


class Table:
    def __init__(self, parent, people, total_rows, total_columns, bg_color='#FFFF99', font_color='#990000'):
        max_column_length = [0] * total_columns
        for p in people:
            for i in range(len(p)):
                max_column_length[i] = max(max_column_length[i], len(str(p[i])))
        for i in range(total_rows):
            for j in range(total_columns):
                if j == total_columns - 1 and bg_color == '#FFFF99':
                    current_width = max_column_length[j]
                else:
                    current_width = max_column_length[j] + 3
                if i == 0:
                    current_font = ('Arial', 14, 'bold')
                else:
                    current_font = ('Arial', 14)
                self.e = Entry(parent, width=current_width, fg=font_color, bg=bg_color, font=current_font)
                self.e.grid(row=i, column=j)
                self.e.insert(END, people[i][j])


def clicked_surname():
    global current_state_surname, enter_id_child_surname, enter_surname_child, root_surname
    current_state_surname = []

    root_surname = Toplevel(root)
    root_surname.title("Фамилии")
    root_surname.geometry('550x300')
    root_surname["bg"] = '#FFCCFF'
    fon_btn = '#CC99FF'
    Button(root_surname, bg=fon_btn, text="Закрыть", font=('arial', 14), command=root_surname.destroy).place(relx=0.75, y=200)

    y_id = 25
    fon_entry = '#FFFFCC'

    lbl_id = Label(root_surname, text="Код", bg=root_surname["bg"], fg='#660066', font=('arial', 14, 'bold'))
    lbl_id.place(x=40, y=y_id, width=level2_width, height=height_label)
    enter_id_child_surname = Entry(root_surname, width=100, bg=fon_entry, font=('arial', 14))
    enter_id_child_surname.place(x=40, y=y_id+25, width=level2_width, height=height_combo)
    lbl_surname = Label(root_surname, text="Фамилия", bg=root_surname["bg"], fg='#660066', font=('arial', 14, 'bold'))
    lbl_surname.place(x=180, y=y_id, width=level1_width, height=height_label)
    enter_surname_child = Entry(root_surname, bg=fon_entry, font=('arial', 14))
    enter_surname_child.place(x=180, y=y_id+25, width=level1_width, height=height_combo)

    btn_search = Button(root_surname, text="Найти", bg=fon_btn, font=('arial', 14), command=child_surname_search)
    btn_search.place(relx=0.75, y=50)
    btn_add = Button(root_surname, text="Добавить", bg=fon_btn, font=('arial', 14), command=child_surname_add)
    btn_add.place(relx=0.75, y=100)
    btn_add = Button(root_surname, text="Удалить", bg=fon_btn, font=('arial', 14), command=child_surname_delete)
    btn_add.place(relx=0.75, y=150)


def child_surname_search():
    global current_state_surname
    input_id = enter_id_child_surname.get().strip()
    input_surname = enter_surname_child.get().strip().lower()
    if any([not x.isdigit() for x in input_id]):
        input_id = ''
    if not input_id and not input_surname:
        Label(root_surname, bg=root_surname["bg"]).place(x=40, y=100, relwidth=0.6, relheight=0.7)
        current_state_surname = []
        return
    req = "SELECT * FROM surname_store WHERE "
    if input_id:
        req += f"id = {input_id}"
    if input_surname:
        if input_id:
            req += " and "
        req += f"lower(surname) = '{input_surname}'"
    req += ';'
    print("req:", req)
    curr.execute(req)
    answer = curr.fetchall()
    if not answer:
        Label(root_surname, bg=root_surname["bg"]).place(x=40, y=100, relwidth=0.6, relheight=0.7)
        current_state_surname = []
        return
    print("answer:", answer)
    current_state_surname = answer[0]
    output = Frame(root_surname, bg=root_surname["bg"])
    answer.insert(0, ("Код", "Фамилия"))
    output.place(x=40, y=100, relwidth=0.6, relheight=0.7)
    table = Table(output, answer, len(answer), 2, '#FFFFCC', '#660066')


def child_surname_add():
    input_surname = enter_surname_child.get().strip().title()
    curr.execute(f"SELECT id FROM surname_store WHERE lower(surname) = '{input_surname.lower()}'")
    answer = curr.fetchall()
    if answer:
        return
    curr.execute(f"INSERT INTO surname_store (surname) VALUES('{input_surname}')")
    connection.commit()
    snos()


def child_surname_delete():
    global current_state_surname
    input_id = enter_id_child_surname.get().strip()
    input_surname = enter_surname_child.get().strip().title()
    if any([not x.isdigit() for x in input_id]):
        input_id = ''
    if not input_id and not input_surname:
        return
    req = "DELETE FROM surname_store WHERE"
    if input_id:
        req += f" id = {input_id}"
    if input_surname:
        if input_id:
            req += " and"
        req += f" surname = '{input_surname}'"
    curr.execute(req)
    connection.commit()
    snos()


def clicked_name():
    global current_state_name, enter_id_child_name, enter_name_child, root_name
    current_state_name = []

    root_name = Toplevel(root)
    root_name.title("Имена")
    root_name.geometry('550x300')
    root_name["bg"] = '#FFCCFF'
    fon_btn = '#CC99FF'
    Button(root_name, bg=fon_btn, text="Закрыть", font=('arial', 14), command=root_name.destroy).place(relx=0.75, y=200)

    y_id = 25
    fon_entry = '#FFFFCC'

    lbl_id = Label(root_name, text="Код", bg=root_name["bg"], fg='#660066', font=('arial', 14, 'bold'))
    lbl_id.place(x=40, y=y_id, width=level2_width, height=height_label)
    enter_id_child_name = Entry(root_name, width=100, bg=fon_entry, font=('arial', 14))
    enter_id_child_name.place(x=40, y=y_id + 25, width=level2_width, height=height_combo)
    lbl_name = Label(root_name, text="Имя", bg=root_name["bg"], fg='#660066', font=('arial', 14, 'bold'))
    lbl_name.place(x=180, y=y_id, width=level1_width, height=height_label)
    enter_name_child = Entry(root_name, bg=fon_entry, font=('arial', 14))
    enter_name_child.place(x=180, y=y_id + 25, width=level1_width, height=height_combo)

    btn_search = Button(root_name, text="Найти", bg=fon_btn, font=('arial', 14), command=child_name_search)
    btn_search.place(relx=0.75, y=50)
    btn_add = Button(root_name, text="Добавить", bg=fon_btn, font=('arial', 14), command=child_name_add)
    btn_add.place(relx=0.75, y=100)
    btn_add = Button(root_name, text="Удалить", bg=fon_btn, font=('arial', 14), command=child_name_delete)
    btn_add.place(relx=0.75, y=150)
    
    
def child_name_search():
    global current_state_name
    input_id = enter_id_child_name.get().strip()
    input_name = enter_name_child.get().strip().lower()
    if any([not x.isdigit() for x in input_id]):
        input_id = ''
    if not input_id and not input_name:
        Label(root_name, bg=root_name["bg"]).place(x=40, y=100, relwidth=0.6, relheight=0.7)
        current_state_name = []
        return
    req = "SELECT * FROM name_store WHERE "
    if input_id:
        req += f"id = {input_id}"
    if input_name:
        if input_id:
            req += " and "
        req += f"lower(name) = '{input_name}'"
    req += ';'
    print("req:", req)
    curr.execute(req)
    answer = curr.fetchall()
    if not answer:
        Label(root_name, bg=root_name["bg"]).place(x=40, y=100, relwidth=0.6, relheight=0.7)
        current_state_name = []
        return
    print("answer:", answer)
    current_state_name = answer[0]
    output = Frame(root_name, bg=root_name["bg"])
    answer.insert(0, ("Код", "Имя"))
    output.place(x=40, y=100, relwidth=0.6, relheight=0.7)
    table = Table(output, answer, len(answer), 2, '#FFFFCC', '#660066')


def child_name_add():
    input_name = enter_name_child.get().strip().title()
    curr.execute(f"SELECT id FROM name_store WHERE lower(name) = '{input_name.lower()}'")
    answer = curr.fetchall()
    if answer:
        return
    curr.execute(f"INSERT INTO name_store (name) VALUES('{input_name}')")
    connection.commit()
    snos()


def child_name_delete():
    global current_state_name
    input_id = enter_id_child_name.get().strip()
    input_name = enter_name_child.get().strip().title()
    if any([not x.isdigit() for x in input_id]):
        input_id = ''
    if not input_id and not input_name:
        return
    req = "DELETE FROM name_store WHERE"
    if input_id:
        req += f" id = {input_id}"
    if input_name:
        if input_id:
            req += " and"
        req += f" name = '{input_name}'"
    curr.execute(req)
    connection.commit()
    snos()


def clicked_otch():
    global current_state_otch, enter_id_child_otch, enter_otch_child, root_otch
    current_state_otch = []

    root_otch = Toplevel(root)
    root_otch.title("Имена")
    root_otch.geometry('550x300')
    root_otch["bg"] = '#FFCCFF'
    fon_btn = '#CC99FF'
    Button(root_otch, bg=fon_btn, text="Закрыть", font=('arial', 14), command=root_otch.destroy).place(relx=0.75, y=200)

    y_id = 25
    fon_entry = '#FFFFCC'

    lbl_id = Label(root_otch, text="Код", bg=root_otch["bg"], fg='#660066', font=('arial', 14, 'bold'))
    lbl_id.place(x=40, y=y_id, width=level2_width, height=height_label)
    enter_id_child_otch = Entry(root_otch, width=100, bg=fon_entry, font=('arial', 14))
    enter_id_child_otch.place(x=40, y=y_id + 25, width=level2_width, height=height_combo)
    lbl_otch = Label(root_otch, text="Отчество", bg=root_otch["bg"], fg='#660066', font=('arial', 14, 'bold'))
    lbl_otch.place(x=180, y=y_id, width=level1_width, height=height_label)
    enter_otch_child = Entry(root_otch, bg=fon_entry, font=('arial', 14))
    enter_otch_child.place(x=180, y=y_id + 25, width=level1_width, height=height_combo)

    btn_search = Button(root_otch, text="Найти", bg=fon_btn, font=('arial', 14), command=child_otch_search)
    btn_search.place(relx=0.75, y=50)
    btn_add = Button(root_otch, text="Добавить", bg=fon_btn, font=('arial', 14), command=child_otch_add)
    btn_add.place(relx=0.75, y=100)
    btn_add = Button(root_otch, text="Удалить", bg=fon_btn, font=('arial', 14), command=child_otch_delete)
    btn_add.place(relx=0.75, y=150)


def child_otch_search():
    global current_state_otch
    input_id = enter_id_child_otch.get().strip()
    input_otch = enter_otch_child.get().strip().lower()
    if any([not x.isdigit() for x in input_id]):
        input_id = ''
    if not input_id and not input_otch:
        Label(root_otch, bg=root_otch["bg"]).place(x=40, y=100, relwidth=0.6, relheight=0.7)
        current_state_otch = []
        return
    req = "SELECT * FROM otch_store WHERE "
    if input_id:
        req += f"id = {input_id}"
    if input_otch:
        if input_id:
            req += " and "
        req += f"lower(otch) = '{input_otch}'"
    req += ';'
    print("req:", req)
    curr.execute(req)
    answer = curr.fetchall()
    if not answer:
        Label(root_otch, bg=root_otch["bg"]).place(x=40, y=100, relwidth=0.6, relheight=0.7)
        current_state_otch = []
        return
    print("answer:", answer)
    current_state_otch = answer[0]
    output = Frame(root_otch, bg=root_otch["bg"])
    answer.insert(0, ("Код", "Имя"))
    output.place(x=40, y=100, relwidth=0.6, relheight=0.7)
    table = Table(output, answer, len(answer), 2, '#FFFFCC', '#660066')


def child_otch_add():
    input_otch = enter_otch_child.get().strip().title()
    curr.execute(f"SELECT id FROM otch_store WHERE lower(otch) = '{input_otch.lower()}'")
    answer = curr.fetchall()
    if answer:
        return
    curr.execute(f"INSERT INTO otch_store (otch) VALUES('{input_otch}')")
    connection.commit()
    snos()


def child_otch_delete():
    global current_state_otch
    input_id = enter_id_child_otch.get().strip()
    input_otch = enter_otch_child.get().strip().title()
    if any([not x.isdigit() for x in input_id]):
        input_id = ''
    if not input_id and not input_otch:
        return
    req = "DELETE FROM otch_store WHERE"
    if input_id:
        req += f" id = {input_id}"
    if input_otch:
        if input_id:
            req += " and"
        req += f" otch = '{input_otch}'"
    curr.execute(req)
    connection.commit()
    snos()


def clicked_street():
    global current_state_street, enter_id_child_street, enter_street_child, root_street
    current_state_street = []

    root_street = Toplevel(root)
    root_street.title("Улицы")
    root_street.geometry('550x300')
    root_street["bg"] = '#FFCCFF'
    fon_btn = '#CC99FF'
    Button(root_street, bg=fon_btn, text="Закрыть", font=('arial', 14), command=root_street.destroy).place(relx=0.75, y=200)

    y_id = 25
    fon_entry = '#FFFFCC'

    lbl_id = Label(root_street, text="Код", bg=root_street["bg"], fg='#660066', font=('arial', 14, 'bold'))
    lbl_id.place(x=40, y=y_id, width=level2_width, height=height_label)
    enter_id_child_street = Entry(root_street, width=100, bg=fon_entry, font=('arial', 14))
    enter_id_child_street.place(x=40, y=y_id + 25, width=level2_width, height=height_combo)
    lbl_street = Label(root_street, text="Улица", bg=root_street["bg"], fg='#660066', font=('arial', 14, 'bold'))
    lbl_street.place(x=180, y=y_id, width=level1_width, height=height_label)
    enter_street_child = Entry(root_street, bg=fon_entry, font=('arial', 14))
    enter_street_child.place(x=180, y=y_id + 25, width=level1_width, height=height_combo)

    btn_search = Button(root_street, text="Найти", bg=fon_btn, font=('arial', 14), command=child_street_search)
    btn_search.place(relx=0.75, y=50)
    btn_add = Button(root_street, text="Добавить", bg=fon_btn, font=('arial', 14), command=child_street_add)
    btn_add.place(relx=0.75, y=100)
    btn_add = Button(root_street, text="Удалить", bg=fon_btn, font=('arial', 14), command=child_street_delete)
    btn_add.place(relx=0.75, y=150)


def child_street_search():
    global current_state_street
    input_id = enter_id_child_street.get().strip()
    input_street = enter_street_child.get().strip().lower()
    if any([not x.isdigit() for x in input_id]):
        input_id = ''
    if not input_id and not input_street:
        Label(root_street, bg=root_street["bg"]).place(x=40, y=100, relwidth=0.6, relheight=0.7)
        current_state_street = []
        return
    req = "SELECT * FROM street_store WHERE "
    if input_id:
        req += f"id = {input_id}"
    if input_street:
        if input_id:
            req += " and "
        req += f"lower(street) = '{input_street}'"
    req += ';'
    print("req:", req)
    curr.execute(req)
    answer = curr.fetchall()
    if not answer:
        Label(root_street, bg=root_street["bg"]).place(x=40, y=100, relwidth=0.6, relheight=0.7)
        current_state_street = []
        return
    print("answer:", answer)
    current_state_street = answer[0]
    output = Frame(root_street, bg=root_street["bg"])
    answer.insert(0, ("Код", "Имя"))
    output.place(x=40, y=100, relwidth=0.6, relheight=0.7)
    table = Table(output, answer, len(answer), 2, '#FFFFCC', '#660066')


def child_street_add():
    input_street = enter_street_child.get().strip().title()
    curr.execute(f"SELECT id FROM street_store WHERE lower(street) = '{input_street.lower()}'")
    answer = curr.fetchall()
    if answer:
        return
    curr.execute(f"INSERT INTO street_store (street) VALUES('{input_street}')")
    connection.commit()
    snos()


def child_street_delete():
    global current_state_street
    input_id = enter_id_child_street.get().strip()
    input_street = enter_street_child.get().strip().title()
    if any([not x.isdigit() for x in input_id]):
        input_id = ''
    if not input_id and not input_street:
        return
    req = "DELETE FROM street_store WHERE"
    if input_id:
        req += f" id = {input_id}"
    if input_street:
        if input_id:
            req += " and"
        req += f" street = '{input_street}'"
    curr.execute(req)
    connection.commit()
    snos()
                
                
def print_current(people=None):
    if people is None:
        people = []
    global first_found_person
    if not people:
        people = copy.copy(current_people)
    else:
        people = copy.copy(people)
    output = Frame(root, bg=fon)
    if len(people) == 0:
        cover = Label(root, bg=fon)
        output.place(anchor=N, relx=table_relx, rely=table_rely, relwidth=table_relwidth, relheight=table_relheight)
        first_found_person = []
        return
    first_found_person = people[0]
    people.insert(0, ("Фамилия", "Имя", "Отчество", "Улица", "Дом", "Корпус", "Квартира", "Телефон"))
    output.place(anchor=N, relx=table_relx, rely=table_rely, relwidth=table_relwidth, relheight=table_relheight)
    table = Table(output, people, len(people), len(people[0]))


def clicked_search():
    global current_people, first_found_person

    input_name = combo_name.get().lower()
    curr.execute(f"SELECT id FROM name_store WHERE lower(name_store.name) = '{input_name}'")
    input_name = curr.fetchall()[0][0]

    input_surname = combo_surname.get().lower()
    curr.execute(f"SELECT id FROM surname_store WHERE lower(surname_store.surname) = '{input_surname}'")
    input_surname = curr.fetchall()[0][0]

    input_otch = combo_otch.get().lower()
    curr.execute(f"SELECT id FROM otch_store WHERE lower(otch_store.otch) = '{input_otch}'")
    input_otch = curr.fetchall()[0][0]

    input_street = combo_street.get().lower()
    curr.execute(f"SELECT id FROM street_store WHERE lower(street_store.street) = '{input_street}'")
    input_street = curr.fetchall()[0][0]

    input_house = enter_house.get().lower()
    input_korpus = enter_korpus.get().lower()
    input_flat = enter_flat.get().lower()
    input_number = enter_number.get()

    req = "SELECT * FROM main WHERE"
    if input_name != 1:
        req += f" (name_ = {input_name})"
    if input_surname != 1:
        if len(req) > 24:
            req += " and"
        req += f" (surname = {input_surname})"
    if input_otch != 1:
        if len(req) > 24:
            req += " and"
        req += f" (otch = {input_otch})"
    if input_street != 1:
        if len(req) > 24:
            req += " and"
        req += f" (street = {input_street})"
    if input_house:
        if len(req) > 24:
            req += " and"
        req += f" (lower(house) = '{input_house}')"
    if input_korpus:
        if len(req) > 24:
            req += " and"
        req += f" (lower(korpus) = '{input_korpus}')"
    if input_flat:
        if len(req) > 24:
            req += " and"
        req += f" (lower(flat) = '{input_flat}')"
    if input_number:
        if len(req) > 24:
            req += " and"
        if '%' in input_number:
            req += f"(number LIKE '{input_number}')"
        else:
            req += f" (number = '{input_number}')"

    if len(req) == 24:
        cover = Label(root, bg=fon)
        cover.place(anchor=N, x=0.5, y=0.5, width=1, height=0.5)
        first_found_person = []
        current_people = []
        return
    else:
        req += ';'

    curr.execute(req)
    answer = curr.fetchall()
    for i in range(len(answer)):
        answer[i] = list(answer[i][1:])
        answer[i][0], answer[i][1] = answer[i][1], answer[i][0]

    for i in range(len(answer)):
        curr.execute(f"SELECT surname_store.surname FROM surname_store WHERE surname_store.id = {answer[i][0]}")
        a = curr.fetchall()[0][0]
        answer[i][0] = a

        curr.execute(f"SELECT name_store.name FROM name_store WHERE name_store.id = {answer[i][1]}")
        answer[i][1] = curr.fetchall()[0][0]

        curr.execute(f"SELECT otch_store.otch FROM otch_store WHERE otch_store.id = {answer[i][2]}")
        answer[i][2] = curr.fetchall()[0][0]

        curr.execute(f"SELECT street_store.street FROM street_store WHERE street_store.id = {answer[i][3]}")
        answer[i][3] = curr.fetchall()[0][0]

        answer[i] = tuple(answer[i])

    current_people = answer
    print_current(people=answer)


def clicked_print():
    global current_people
    req = 'SELECT surname_store.surname, name_store.name, otch_store.otch, street_store.street, '\
            'house, korpus, flat, number FROM main '\
            'JOIN name_store ON main.name_ = name_store.id JOIN surname_store ON main.surname = surname_store.id '\
            'JOIN otch_store ON main.otch = otch_store.id JOIN street_store ON main.street = street_store.id;'
    curr.execute(req)
    people = curr.fetchall()
    current_people = people
    print_current(people=people)


def clicked_add():
    input_number = enter_number.get()
    if(input_number == ''):
        return
    input_name = combo_name.get()
    input_name_curr = input_name
    curr.execute(f"SELECT id FROM name_store WHERE name_store.name = '{input_name}'")
    input_name = curr.fetchall()[0][0]

    input_surname = combo_surname.get()
    input_surname_curr = input_surname
    curr.execute(f"SELECT id FROM surname_store WHERE surname_store.surname = '{input_surname}'")
    input_surname = curr.fetchall()[0][0]

    input_otch = combo_otch.get()
    input_otch_curr = input_otch
    curr.execute(f"SELECT id FROM otch_store WHERE otch_store.otch = '{input_otch}'")
    input_otch = curr.fetchall()[0][0]

    input_street = combo_street.get()
    input_street_curr = input_street
    curr.execute(f"SELECT id FROM street_store WHERE street_store.street = '{input_street}'")
    input_street = curr.fetchall()[0][0]

    input_house = enter_house.get()
    input_korpus = enter_korpus.get()
    input_flat = enter_flat.get()
    current_people.insert(0, (input_surname_curr, input_name_curr, input_otch_curr, input_street_curr, input_house, input_korpus, input_flat, input_number))

    req = "INSERT INTO main (surname, name_, otch, street, house, korpus, flat, number) "\
            f"VALUES({input_surname}, {input_name}, {input_otch}, {input_street}, '{input_house}',"\
            f" '{input_korpus}', '{input_flat}', '{input_number}');"
    curr.execute(req)
    connection.commit()
    print("Added")
    print("input_name:",    input_name)
    print("input_surname:", input_surname)
    print("input_otch:",    input_otch)
    print("input_street:",  input_street)
    print("input_house:",   input_house)
    print("input_korpus:",  input_korpus)
    print("input_flat:",    input_flat)
    print("input_number:",  input_number)
    print_current()


def clicked_save():
    global first_found_person
    print("first_found_person:", first_found_person)

    if not first_found_person or not current_people:
        return

    input_name = combo_name.get()
    input_name_text = input_name
    curr.execute(f"SELECT id FROM name_store WHERE name_store.name = '{input_name}'")
    input_name = curr.fetchall()[0][0]

    input_surname = combo_surname.get()
    input_surname_text = input_surname
    curr.execute(f"SELECT id FROM surname_store WHERE surname_store.surname = '{input_surname}'")
    input_surname = curr.fetchall()[0][0]

    input_otch = combo_otch.get()
    input_otch_text = input_otch
    curr.execute(f"SELECT id FROM otch_store WHERE otch_store.otch = '{input_otch}'")
    input_otch = curr.fetchall()[0][0]

    input_street = combo_street.get()
    input_street_text = input_street
    curr.execute(f"SELECT id FROM street_store WHERE street_store.street = '{input_street}'")
    input_street = curr.fetchall()[0][0]

    input_house = enter_house.get()
    input_korpus = enter_korpus.get()
    input_flat = enter_flat.get()
    input_number = enter_number.get()

    req = "SELECT id FROM main WHERE"
    if input_name != 1:
        curr.execute(f"SELECT id FROM name_store WHERE name_store.name = '{first_found_person[1]}'")
        temp = curr.fetchall()[0][0]
        req += f" (name_ = {temp})"
    if input_surname != 1:
        if len(req) > 25:
            req += " and"
        curr.execute(f"SELECT id FROM surname_store WHERE surname_store.surname = '{first_found_person[0]}'")
        temp = curr.fetchall()[0][0]
        req += f" (surname = {temp})"
    if input_otch != 1:
        if len(req) > 25:
            req += " and"
        curr.execute(f"SELECT id FROM otch_store WHERE otch_store.otch = '{first_found_person[2]}'")
        temp = curr.fetchall()[0][0]
        req += f" (otch = {temp})"
    if input_street != 1:
        if len(req) > 25:
            req += " and"
        curr.execute(f"SELECT id FROM street_store WHERE street_store.street = '{first_found_person[3]}'")
        temp = curr.fetchall()[0][0]
        req += f" (street = {temp})"
    if input_house:
        if len(req) > 25:
            req += " and"
        req += f" (house = '{first_found_person[4]}')"
    if input_korpus:
        if len(req) > 25:
            req += " and"
        req += f" (korpus = '{first_found_person[5]}')"
    if input_flat:
        if len(req) > 25:
            req += " and"
        req += f" (flat = '{first_found_person[6]}')"
    if input_number and '%' not in input_number:
        if len(req) > 25:
            req += " and"
        req += f" (number = '{first_found_person[7]}')"

    if len(req) == 25:
        return
    curr.execute(req)
    updating_id = curr.fetchall()[0][0]
    print("updating_id:", updating_id)

    upd_list = list(current_people[0])
    req = 'UPDATE main SET'
    if input_surname != 1:
        if len(req) > 15:
            req += ','
        req += f" surname = {input_surname}"
        upd_list[0] = input_surname_text
    if input_name != 1:
        if len(req) > 15:
            req += ','
        req += f" name_ = {input_name}"
        upd_list[1] = input_name_text
    if input_otch != 1:
        if len(req) > 15:
            req += ','
        req += f" otch = {input_otch}"
        upd_list[2] = input_otch_text
    if input_street != 1:
        if len(req) > 15:
            req += ','
        req += f" street = {input_street}"
        upd_list[3] = input_street_text
    if input_house != '':
        if len(req) > 15:
            req += ','
        req += f" house = '{input_house}'"
        upd_list[4] = input_house
    if input_korpus != '':
        if len(req) > 15:
            req += ','
        req += f" korpus = '{input_korpus}'"
        upd_list[5] = input_korpus
    if input_flat != '':
        if len(req) > 15:
            req += ','
        req += f" flat = '{input_flat}'"
        upd_list[6] = input_flat
    if input_number != '':
        if len(req) > 15:
            req += ','
        req += f" number = '{input_number}'"
        upd_list[7] = input_number

    current_people[0] = tuple(upd_list)

    if len(req) == 15:
        return
    else:
        req += f" WHERE id = {updating_id};"

    print("req:", req)

    curr.execute(req)
    connection.commit()
    print_current()


def clicked_delete():
    global current_people

    input_name = combo_name.get()
    input_name_curr = input_name
    curr.execute(f"SELECT id FROM name_store WHERE name_store.name = '{input_name}'")
    input_name = curr.fetchall()[0][0]

    input_surname = combo_surname.get()
    input_surname_curr = input_surname
    curr.execute(f"SELECT id FROM surname_store WHERE surname_store.surname = '{input_surname}'")
    input_surname = curr.fetchall()[0][0]

    input_otch = combo_otch.get()
    input_otch_curr = input_otch
    curr.execute(f"SELECT id FROM otch_store WHERE otch_store.otch = '{input_otch}'")
    input_otch = curr.fetchall()[0][0]

    input_street = combo_street.get()
    input_street_curr = input_street
    curr.execute(f"SELECT id FROM street_store WHERE street_store.street = '{input_street}'")
    input_street = curr.fetchall()[0][0]

    input_house = enter_house.get()
    input_korpus = enter_korpus.get()
    input_flat = enter_flat.get()
    input_number = enter_number.get()

    req = "DELETE FROM main WHERE"
    if input_name != 1:
        req += f" (name_ = {input_name})"
    if input_surname != 1:
        if len(req) > 22:
            req += " and"
        req += f" (surname = {input_surname})"
    if input_otch != 1:
        if len(req) > 22:
            req += " and"
        req += f" (otch = {input_otch})"
    if input_street != 1:
        if len(req) > 22:
            req += " and"
        req += f" (street = {input_street})"
    if input_house:
        if len(req) > 22:
            req += " and"
        req += f" (house = '{input_house}')"
    if input_korpus:
        if len(req) > 22:
            req += " and"
        req += f" (korpus = '{input_korpus}')"
    if input_flat:
        if len(req) > 22:
            req += " and"
        req += f" (flat = '{input_flat}')"
    if input_number:
        if len(req) > 22:
            req += " and"
        req += f" (number = '{input_number}')"

    if len(req) == 22:
        return
    else:
        req += ';'
    print("current_people before:", current_people)
    current_people = list(filter(lambda x: (input_surname_curr != x[0] and input_surname_curr != '' or
                                            input_name_curr != x[1] and input_name_curr != '' or
                                            input_otch_curr != x[2] and input_otch_curr != '' or
                                            input_street_curr != x[3] and input_street_curr != '' or
                                            input_house != x[4] and input_house != '' or
                                            input_korpus != x[5] and input_korpus != '' or
                                            input_flat != x[6] and input_flat != '' or
                                            input_number != x[7] and input_number != ''), current_people))
    print("current_people after:", current_people)
    curr.execute(req)
    connection.commit()
    print("Deleted")
    print_current()


def clicked_clear():
    global first_found_person
    s = enter_number.get() + enter_korpus.get() + enter_flat.get() + enter_house.get()
    s += combo_street.get() + combo_name.get() + combo_otch.get() + combo_surname.get()
    if s == '':
        output = Label(root, bg=fon)
        output.place(anchor=N, relx=table_relx, rely=table_rely, relwidth=table_relwidth, relheight=table_relheight)
        first_found_person = []
        return
    enter_number.delete(0, 'end')
    enter_korpus.delete(0, 'end')
    enter_flat.delete(0, 'end')
    enter_house.delete(0, 'end')
    combo_street.delete(0, 'end')
    combo_name.delete(0, 'end')
    combo_otch.delete(0, 'end')
    combo_surname.delete(0, 'end')


def clicked_exit():
    curr.close()
    connection.close()
    root.quit()


def snos():
    global combo_surname, combo_name, combo_otch, combo_street

    curr.execute('SELECT surname FROM surname_store')
    rec = curr.fetchall()
    rec = list(map(lambda x: x[0], rec))
    btn_surname = Button(root, text="Фамилия", bg=fon_btn_table, font=('arial', 14, 'bold'), command=clicked_surname)
    btn_surname.place(anchor=N, x=from_left, y=level1_y, width=level1_width - 40, height=height_label + 10)
    combo_surname = Combobox(root, width=15, font=('arial', 14))
    combo_surname['values'] = tuple(rec)
    combo_surname.place(anchor=N, x=from_left, y=level1_y + 25, width=level1_width, height=height_combo)

    curr.execute('SELECT name FROM name_store')
    rec = curr.fetchall()
    rec = list(map(lambda x: x[0], rec))
    btn_name = Button(root, text="Имя", bg=fon_btn_table, font=('arial', 14, 'bold'), command=clicked_name)
    btn_name.place(anchor=N, x=from_left + 200, y=level1_y, width=level1_width - 50, height=height_label + 10)
    combo_name = Combobox(root, width=15, font=('arial', 14))
    combo_name['values'] = tuple(rec)
    combo_name.place(anchor=N, x=from_left + 200, y=level1_y + 25, width=level1_width, height=height_combo)

    curr.execute('SELECT otch FROM otch_store')
    rec = curr.fetchall()
    rec = list(map(lambda x: x[0], rec))
    btn_otch = Button(root, text="Отчество", bg=fon_btn_table, font=('arial', 14, 'bold'), command=clicked_otch)
    btn_otch.place(anchor=N, x=from_left + 400, y=level1_y, width=level1_width - 40, height=height_label + 10)
    combo_otch = Combobox(root, width=15, font=('arial', 14))
    combo_otch['values'] = tuple(rec)
    combo_otch.place(anchor=N, x=from_left + 400, y=level1_y + 25, width=level1_width, height=height_combo)

    curr.execute('SELECT street FROM street_store')
    rec = curr.fetchall()
    rec = list(map(lambda x: x[0], rec))
    btn_street = Button(root, text="Улица", bg=fon_btn_table, font=('arial', 14, 'bold'), command=clicked_street)
    btn_street.place(anchor=N, x=from_left + 630, y=level1_y, width=level1_width - 50, height=height_label + 10)
    combo_street = Combobox(root, width=15, font=('arial', 14))
    combo_street['values'] = tuple(rec)
    combo_street.place(anchor=N, x=from_left + 630, y=level1_y + 25, width=level1_width + 60, height=height_combo)


root = Tk()
root.title("Телефонный справочник")
root.geometry('1300x600')
root["bg"] = "#FFCC99"

areaBackground = '#FFFF66'
fon = '#FFCC99'
fon_btn_table = '#CC99FF'
combostyle = Style()
combostyle.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': 'darkred',
                                       'fieldbackground': areaBackground,
                                       'background': 'green'}}})
combostyle.theme_use('combostyle')

level1_y = 50
level1_width = 170
height_label = 18
height_combo = 25
from_left = 200

level2_y = 130
level2_width = 100
level3_y = 220

table_relx = 0.5
table_rely = 0.5
table_relwidth = 0.95
table_relheight = 1

first_found_person = []
current_people = []
current_state_name = []
current_state_surname = []
current_state_otch = []
current_state_street = []

enter_surname_child: []
enter_name_child: []
enter_otch_child: []
enter_street_child: []
enter_id_child_surname: []
enter_id_child_name: []
enter_id_child_otch: []
enter_id_child_street: []

root_surname = 0
root_name = 0
root_otch = 0
root_street = 0

combo_surname: Combobox
combo_name: Combobox
combo_otch: Combobox
combo_street: Combobox
snos()

lbl_house = Label(root, text="Дом", bg=fon, font=('arial', 14, 'bold'))
lbl_house.place(anchor=N, x=from_left, y=level2_y, width=level2_width, height=height_label)
enter_house = Entry(root, width=15, bg=areaBackground, font=('arial', 14))
enter_house.place(anchor=N, x=from_left, y=level2_y + 25, width=level2_width, height=height_combo)

lbl_korpus = Label(root, text="Корпус", bg=fon, font=('arial', 14, 'bold'))
lbl_korpus.place(anchor=N, x=from_left + 150, y=level2_y, width=level2_width, height=height_label)
enter_korpus = Entry(root, width=15, bg=areaBackground, font=('arial', 14))
enter_korpus.place(anchor=N, x=from_left + 150, y=level2_y + 25, width=level2_width, height=height_combo)

lbl_flat = Label(root, text="Квартира", bg=fon, font=('arial', 14, 'bold'))
lbl_flat.place(anchor=N, x=from_left + 300, y=level2_y, width=level2_width, height=height_label)
enter_flat = Entry(root, width=15, bg=areaBackground, font=('arial', 14))
enter_flat.place(anchor=N, x=from_left + 300, y=level2_y + 25, width=level2_width, height=height_combo)

lbl_phone = Label(root, text="Телефон", bg=fon, font=('arial', 14, 'bold'))
lbl_phone.place(anchor=N, x=from_left + 500, y=level2_y, width=level1_width + 10, height=height_label)
enter_number = Entry(root, width=15, bg=areaBackground, font=('arial', 14))
enter_number.place(anchor=N, x=from_left + 500, y=level2_y + 25, width=level1_width + 10, height=height_combo)


btnSearch = Button(root, text="Поиск", bg=areaBackground, command=clicked_search, font=('arial', 14))
btnSearch.place(anchor=NE, x=from_left, y=level3_y, width=level2_width, height=height_combo)

btnPrint = Button(root, text="Печать", bg=areaBackground, command=clicked_print, font=('arial', 14))
btnPrint.place(anchor=NE, x=from_left + 130, y=level3_y, width=level2_width, height=height_combo)

btnAdd = Button(root, text="Добавить", bg=areaBackground, command=clicked_add, font=('arial', 14))
btnAdd.place(anchor=NE, x=from_left + 260, y=level3_y, width=level2_width, height=height_combo)

btnSave = Button(root, text="Сохранить", bg=areaBackground, command=clicked_save, font=('arial', 14))
btnSave.place(anchor=NE, x=from_left + 390, y=level3_y, width=level2_width, height=height_combo)

btnDelete = Button(root, text="Удалить", bg=areaBackground, command=clicked_delete, font=('arial', 14))
btnDelete.place(anchor=NE, x=from_left + 520, y=level3_y, width=level2_width, height=height_combo)

btnClear = Button(root, text="Очистить", bg=areaBackground, command=clicked_clear, font=('arial', 14))
btnClear.place(anchor=NE, x=from_left + 650, y=level3_y, width=level2_width, height=height_combo)

btnExit = Button(root, text="Выход", bg=areaBackground, command=clicked_exit, font=('arial', 14))
btnExit.place(anchor=NE, x=from_left + 780, y=level3_y, width=level2_width, height=height_combo)

root.mainloop()
