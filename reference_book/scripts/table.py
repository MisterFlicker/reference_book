import npyscreen as nps  # npyscreen - библиотека для формирования консольного интерфейса
import json
import time
from pynput.keyboard import Key, Controller  # pynput - библиотека, в данном случае, имитирующая нажатия клавиатуры

current_items = ['default']  # Дефолтное значение для переменной, отражающей текущую выборку таблицы
sort_set = ''  # Переменная, представляющая собой "статус" по какому столбцу идет сортировка и в каком порядке
page = 1  # Переменная, показывающая текущую страницу таблицы

# Дефолтные значения для таблицы в случае проблем с доступом к файлу хранения данных таблицы
default_values = {
    1: {
        'name': '',
        'surname': '',
        'patronymic': '',
        'organization': '',
        'work_phone': '',
        'personal_phone': ''
    }
}

# Открытие и чтение из файла хранения данных таблицы
with open('test3.txt') as f:
    data = json.load(f)
if data:
    pass
else:
    data = default_values


def next_page():
    """
    Функция, "перелистывающая" страницу вперед.
    """
    global page
    page = page + 1


def back_page():
    """
    Функция, "перелистывающая" страницу назад.
    """
    global page
    if page > 1:
        page = page - 1


def cursor_right():
    """
    Из-за особенности настроек по умолчанию библиотеки npyscreen заглавные русские буквы Е и А являются горячими
    клавишами и при их вводе не производится их набор. Для исправления данной особенности в том числе используется
    данная функция. Она вызывается после ввода А или Е (с помощью конкатенации строк) для переноса текстового курсора
    на 1 букву вправо после А/Е.
    """
    kb = Controller()

    # Задержка в четверть секунды необходима, если пользователь набирает заглавную букву с помощью shift+буква
    time.sleep(0.250)
    kb.press(Key.right)  # Нажатие стрелки вправо
    kb.release(Key.right)  # Моментальное отпускание стрелки вправо


def sort_name(settings):
    """
    Функция, определяющая сортировку в таблице.
    settings - list или str
    """
    global sort_set

    # Преобразование элемента списка или строки в число и передача значения аргументу sort_set
    if type(settings) is list:
        settings[0] = int(settings[0])
    else:
        settings = int(settings)
    sort_set = settings


class TableForm(nps.SplitFormWithMenus):
    """
    Форма, определяющая отображение и взаимодействие с таблицей.
    """
    def exit(self):
        """
        Функция, выхода из приложения.
        """
        self.parentApp.switchForm(None)

    # Ниже 6 функций, "печатающие" заглавные А/Е с помощью конкатенации (о причине подробнее в описании cursor_right())
    def name_ch(self, lit: str):
        self.Name.value = self.Name.value + lit
        cursor_right()

    def surname_ch(self, lit: str):
        self.Surname.value = self.Surname.value + lit
        cursor_right()

    def patronymic_ch(self, lit: str):
        self.Patronymic.value = self.Patronymic.value + lit
        cursor_right()

    def organization_ch(self, lit: str):
        self.Organization.value = self.Organization.value + lit
        cursor_right()

    def work_phone_ch(self, lit: str):
        self.WorkPhone.value = self.WorkPhone.value + lit
        cursor_right()

    def personal_phone_ch(self, lit: str):
        self.PersonalPhone.value = self.PersonalPhone.value + lit
        cursor_right()

    """
    Ниже приведены 10 функций, обрабатывающих нажатие кнопки "edit" напротив значений таблицы.
    npyscreen не предполагает передачи аргументов для кнопок. Решение данной проблемы ниже рабочее, хоть и громоздкое.
    
    Можно сократить число данных функций с 10 до 1, но для этого необходимо изменить содержимое файла npyscreen
    /.venv/lib/python3.8/site-packages/npyscreen/wgbutton.py А именно - позволить __init__ класса используемых кнопок
    MiniButtonPress(MiniButton) принимать параметр arguments и использовать его при вызове when_pressed_function
    Тогда, при создании кнопок (236-245 строки), объявив в качестве arguments номер записи, напротив которой находится
    кнопка, можно будет использовать его в качестве индекса current_items в строке 126.
    """
    def buttonpress0(self):
        global current_items

        # Здесь и в функциях ниже, объявление current_items кортежем, содержащим запись напротив выбранной кнопки "edit"
        current_items = current_items[0]
        self.parentApp.switchForm('ADD')

    def buttonpress1(self):
        global current_items
        current_items = current_items[1]
        self.parentApp.switchForm('ADD')

    def buttonpress2(self):
        global current_items
        current_items = current_items[2]
        self.parentApp.switchForm('ADD')

    def buttonpress3(self):
        global current_items
        current_items = current_items[3]
        self.parentApp.switchForm('ADD')

    def buttonpress4(self):
        global current_items
        current_items = current_items[4]
        self.parentApp.switchForm('ADD')

    def buttonpress5(self):
        global current_items
        current_items = current_items[5]
        self.parentApp.switchForm('ADD')

    def buttonpress6(self):
        global current_items
        current_items = current_items[6]
        self.parentApp.switchForm('ADD')

    def buttonpress7(self):
        global current_items
        current_items = current_items[7]
        self.parentApp.switchForm('ADD')

    def buttonpress8(self):
        global current_items
        current_items = current_items[8]
        self.parentApp.switchForm('ADD')

    def buttonpress9(self):
        global current_items
        current_items = current_items[9]
        self.parentApp.switchForm('ADD')

    def main_menu(self):
        """
        Функция, обрабатывающая нажатие кнопки выхода в главное меню.
        """
        self.parentApp.switchForm('MAIN')

    def create(self):
        """
        Функция, создания формы "страницы" с таблицей
        """
        global page, data

        # Отображаемая при первой загрузки таблицы (на первой странице без фильтров и сортировок)
        all_cols = []
        for key, value in data.items():
            if (page - 1) * 10 < int(key) <= page * 10:
                all_cols.append(
                    (
                        value.get('name'),
                        value.get('surname'),
                        value.get('patronymic'),
                        value.get('organization'),
                        value.get('work_phone'),
                        value.get('personal_phone')
                    )
                )

        # Создание кнопки главного меню
        self.add(nps.ButtonPress, name="В главное меню", when_pressed_function=self.main_menu, relx=1, rely=1)

        # Создание инструкции по пользованию фильтрацией
        self.add(nps.FixedText, value='Для фильтрации таблицы наберите искомое значение ниже:', relx=1, rely=3)

        # Создание полей для поиска/фильтрации нужных значений в таблице
        self.Name = self.add(nps.TitleText, name='Name', relx=1, rely=4)
        self.Surname = self.add(nps.TitleText, name='Surname', relx=1, rely=5)
        self.Patronymic = self.add(nps.TitleText, name='Patronymic', relx=1, rely=6)
        self.Organization = self.add(nps.TitleText, name='Organization', relx=1, rely=7)
        self.WorkPhone = self.add(nps.TitleText, name='Work Phone', max_width=29, relx=1, rely=8)
        self.PersonalPhone = self.add(nps.TitleText, name='Personal Phone', max_width=29, relx=1, rely=9)

        # Переопределение горячих клавиш заглавных букв А/Е (подробнее в описании функции cursor_right())
        self.Name.entry_widget.handlers.update({'А': self.name_ch, 'Е': self.name_ch})
        self.Surname.entry_widget.handlers.update({'А': self.surname_ch, 'Е': self.surname_ch})
        self.Patronymic.entry_widget.handlers.update({'А': self.patronymic_ch, 'Е': self.patronymic_ch})
        self.Organization.entry_widget.handlers.update({'А': self.organization_ch, 'Е': self.organization_ch})
        self.WorkPhone.entry_widget.handlers.update({'А': self.work_phone_ch, 'Е': self.work_phone_ch})
        self.PersonalPhone.entry_widget.handlers.update({'А': self.personal_phone_ch, 'Е': self.personal_phone_ch})

        # Создание инструкции для сортировки таблицы
        self.add(nps.FixedText, value='Для сортировки таблицы нажмите ctrl+X', relx=1, rely=11)

        # Создание таблицы
        self.Data = self.add(
            nps.GridColTitles,
            columns=6, relx=9, rely=13, max_height=12, col_margin=1,
            always_show_cursor=True,
            values=all_cols,
            col_titles=['Name', 'Surname', 'Patronymic', 'Organization', 'Work Phone', 'Personal Phone']
        )

        # Создание кнопок "edit" напротив записей таблицы
        self.edit0 = self.add(nps.ButtonPress, name="Edit", when_pressed_function=self.buttonpress0, relx=1, rely=15)
        self.edit1 = self.add(nps.ButtonPress, name="Edit", when_pressed_function=self.buttonpress1, relx=1, rely=16)
        self.edit2 = self.add(nps.ButtonPress, name="Edit", when_pressed_function=self.buttonpress2, relx=1, rely=17)
        self.edit3 = self.add(nps.ButtonPress, name="Edit", when_pressed_function=self.buttonpress3, relx=1, rely=18)
        self.edit4 = self.add(nps.ButtonPress, name="Edit", when_pressed_function=self.buttonpress4, relx=1, rely=19)
        self.edit5 = self.add(nps.ButtonPress, name="Edit", when_pressed_function=self.buttonpress5, relx=1, rely=20)
        self.edit6 = self.add(nps.ButtonPress, name="Edit", when_pressed_function=self.buttonpress6, relx=1, rely=21)
        self.edit7 = self.add(nps.ButtonPress, name="Edit", when_pressed_function=self.buttonpress7, relx=1, rely=22)
        self.edit8 = self.add(nps.ButtonPress, name="Edit", when_pressed_function=self.buttonpress8, relx=1, rely=23)
        self.edit9 = self.add(nps.ButtonPress, name="Edit", when_pressed_function=self.buttonpress9, relx=1, rely=24)

        # Создание подписи текущей страницы таблицы
        self.Page = self.add(nps.FixedText, value=f'Текущая страница:{page}', relx=30, rely=26)

        # Создание кнопок перемещения по страницам назад и вперед
        self.back = self.add(
            nps.ButtonPress, name="Предыдущая страница", when_pressed_function=back_page, relx=1, rely=26
        )
        self.next = self.add(
            nps.ButtonPress, name="Следующая страница", when_pressed_function=next_page, relx=1, rely=27
        )

        # Создание кнопки выхода из приложения
        self.add(nps.ButtonPress, name="Выйти из приложения", when_pressed_function=self.exit, relx=1, rely=29)

        # Создание меню для сортировки таблицы
        self.menu = self.new_menu(name='Сортировка')

        self.menu.addItem(text='По имени', onSelect=sort_name, arguments=[0])
        self.menu.addItem(text='По фамилии', onSelect=sort_name, arguments=[1])
        self.menu.addItem(text='По отчеству', onSelect=sort_name, arguments=[2])
        self.menu.addItem(text='По организации', onSelect=sort_name, arguments=[3])
        self.menu.addItem(text='По рабочему телефону', onSelect=sort_name, arguments=[4])
        self.menu.addItem(text='По личному телефону', onSelect=sort_name, arguments=[5])

        self.menu.addItem(text='Обратная по имени', onSelect=sort_name, arguments=[[0]])
        self.menu.addItem(text='Обратная по фамилии', onSelect=sort_name, arguments=[[1]])
        self.menu.addItem(text='Обратная по отчеству', onSelect=sort_name, arguments=[[2]])
        self.menu.addItem(text='Обратная по организации', onSelect=sort_name, arguments=[[3]])
        self.menu.addItem(text='Обратная по рабочему телефону', onSelect=sort_name, arguments=[[4]])
        self.menu.addItem(text='Обратная по личному телефону', onSelect=sort_name, arguments=[[5]])

    def while_waiting(self):
        """
        функция, обновляющая любые изменения во время просмотра таблицы каждые полсекунды.
        Учитывает выбранную страницу, сортировку и фильтрации таблицы.
        """
        global page, data, sort_set, current_items

        all_cols = []

        # В знакомом блоке кода добавляется key (идентификатор записи, используемый при редактировании записи)
        for key, value in data.items():
            item = (
                value.get('name'),
                value.get('surname'),
                value.get('patronymic'),
                value.get('organization'),
                str(value.get('work_phone')),
                str(value.get('personal_phone')),
                key
            )
            all_cols.append(item)

        # Тип sort_set обозначает прямую/обратную сортировку, а число в переменной - номер колонки таблицы
        if type(sort_set) is str:
            pass
        elif type(sort_set) is list:

            if type(sort_set[0]) is str:
                pass
            else:
                all_cols = sorted(all_cols, key=lambda x: x[sort_set[0]], reverse=True)

        else:
            all_cols = sorted(all_cols, key=lambda x: x[sort_set])

        # Фильтрация согласно значениям полей над таблицей
        if self.Name.value:
            all_cols = [tup for tup in all_cols if tup[0][0:len(self.Name.value)] == self.Name.value]
        if self.Surname.value:
            all_cols = [tup for tup in all_cols if tup[1][0:len(self.Surname.value)] == self.Surname.value]
        if self.Patronymic.value:
            all_cols = [tup for tup in all_cols if tup[2][0:len(self.Patronymic.value)] == self.Patronymic.value]
        if self.Organization.value:
            all_cols = [tup for tup in all_cols if tup[3][0:len(self.Organization.value)] == self.Organization.value]
        if self.WorkPhone.value:
            all_cols = [tup for tup in all_cols if tup[4][0:len(self.WorkPhone.value)] == self.WorkPhone.value]
        if self.PersonalPhone.value:
            all_cols = [tup for tup in all_cols if tup[5][0:len(self.PersonalPhone.value)] == self.PersonalPhone.value]

        # Учет выбранной страницы при отображении таблицы
        current_items = all_cols[(page - 1) * 10:page * 10]

        # Отображение кнопки "edit" только напротив имеющихся записей в таблице
        edit_list = {
            'edit0': self.edit0,
            'edit1': self.edit1,
            'edit2': self.edit2,
            'edit3': self.edit3,
            'edit4': self.edit4,
            'edit5': self.edit5,
            'edit6': self.edit6,
            'edit7': self.edit7,
            'edit8': self.edit8,
            'edit9': self.edit9
        }
        current_edit = 'edit0'
        while len(current_edit) == 5:

            if int(current_edit[-1]) >= len(current_items):
                edit_list[current_edit].hidden = True
            else:
                edit_list[current_edit].hidden = False

            current_edit = current_edit[:4] + str(int(current_edit[-1]) + 1)

        # Создание переменной для передачи обновленной выборки таблицы без идентификаторов записей
        current_items_for_data = []
        for i in current_items:
            i = list(i)
            i.pop(-1)
            i = tuple(i)
            current_items_for_data.append(i)
        self.Data.values = current_items_for_data

        # Обновление надписи текущей страницы
        self.Page.value = f'Текущая страница: {page}'
        self.display()


class AddForm(nps.Form):
    """
    Форма, определяющая создание/редактирование/удаление записей в таблице.
    """
    def main_menu(self):
        """
        Функция, обрабатывающие нажатие на кнопку возврата в главное меню
        """
        self.parentApp.switchForm('MAIN')

    def input_data(self):
        """
        Функция, обрабатывающая запись в данные текстового файла, хранящего данные таблицы.
        Функция обрабатывает как изменение имеющихся записей так и создание новых.
        """
        global data, current_items

        # Запись изменения имеющейся записи в текстовом файле
        if self.AddOrEdit.name == 'Изменить данные':
            for key in data:
                if key == current_items[-1]:
                    data[key] = {
                        'name': self.Name.value,
                        'surname': self.Surname.value,
                        'patronymic': self.Patronymic.value,
                        'organization': self.Organization.value,
                        'work_phone': self.WorkPhone.value,
                        'personal_phone': self.PersonalPhone.value
                    }

                    my_file = open('test3.txt', "w")
                    json.dump(data, my_file)
                    my_file.close()
                    self.parentApp.switchForm('TABLE')

                    break

        else:
            item_data = [
                self.Name.value,
                self.Surname.value,
                self.Patronymic.value,
                self.Organization.value,
                self.WorkPhone.value,
                self.PersonalPhone.value
            ]

            # Вызов предупреждения о необходимости заполнения всех полей записи
            for i in item_data:
                if len(i) == 0:
                    nps.notify_confirm('Все поля должны быть заполнены!', title='Ошибка')
                    break

                # Запись создания новой записи в текстовом файле
                else:
                    max_id = max(list(map(int, list(data.keys()))))
                    data[max_id + 1] = {
                        'name': self.Name.value,
                        'surname': self.Surname.value,
                        'patronymic': self.Patronymic.value,
                        'organization': self.Organization.value,
                        'work_phone': self.WorkPhone.value,
                        'personal_phone': self.PersonalPhone.value
                    }

                    my_file = open('test3.txt', "w")
                    json.dump(data, my_file)
                    my_file.close()
                    self.parentApp.switchForm('TABLE')

                    break

    def delete_data(self):
        """
        Функция, обрабатывающая удаление записи из текстового файла.
        """
        global data, current_items

        for key in data:
            if key == current_items[-1]:
                del data[key]
                break

        my_file = open('test3.txt', "w")
        json.dump(data, my_file)
        my_file.close()
        self.parentApp.switchForm('TABLE')

    def create(self):
        """
        Функция создания формы создания/изменения/удаления записей таблицы
        """

        # Создание кнопки возврата в главное меню
        self.add(nps.ButtonPress, name="В главное меню", when_pressed_function=self.main_menu, relx=1, rely=1)

        # Создание полей записи таблицы
        self.Name = self.add(nps.TitleText, name='Name', relx=1, rely=3)
        self.Surname = self.add(nps.TitleText, name='Surname', relx=1, rely=4)
        self.Patronymic = self.add(nps.TitleText, name='Patronymic', relx=1, rely=5)
        self.Organization = self.add(nps.TitleText, name='Organization', relx=1, rely=6)
        self.WorkPhone = self.add(nps.TitleText, name='WorkPhone', max_width=29, relx=1, rely=7)
        self.PersonalPhone = self.add(nps.TitleText, name='PersonalPhone', max_width=29, relx=1, rely=8)

        # Переопределение горячих клавиш заглавных букв А/Е (подробнее в описании функции cursor_right())
        self.Name.entry_widget.handlers.update({'А': self.name_ch, 'Е': self.name_ch})
        self.Surname.entry_widget.handlers.update({'А': self.surname_ch, 'Е': self.surname_ch})
        self.Patronymic.entry_widget.handlers.update({'А': self.patronymic_ch, 'Е': self.patronymic_ch})
        self.Organization.entry_widget.handlers.update({'А': self.organization_ch, 'Е': self.organization_ch})
        self.WorkPhone.entry_widget.handlers.update({'А': self.work_phone_ch, 'Е': self.work_phone_ch})
        self.PersonalPhone.entry_widget.handlers.update({'А': self.personal_phone_ch, 'Е': self.personal_phone_ch})

        # Создание кнопок внесения и удаления данных
        self.AddOrEdit = self.add(
            nps.ButtonPress, name="Внести данные", when_pressed_function=self.input_data, relx=1, rely=10
        )
        self.DeleteData = self.add(
            nps.ButtonPress, hidden=True,
            name="Удалить данные", when_pressed_function=self.delete_data, relx=1, rely=11
        )

        # Создание кнопки выхода из приложения
        self.add(nps.ButtonPress, name="Выйти из приложения", when_pressed_function=self.exit, relx=1, rely=13)

    def exit(self):
        """
        Функция, обрабатывающая нажатие кнопки выхода из приложения
        """
        self.parentApp.switchForm(None)

    def beforeEditing(self):
        """
        Функция, обрабатывающая контекст при входе на "страницу" заполнения формы
        """
        global current_items

        # Заполнение полей данными записи, которую решено было редактировать
        if type(current_items) is tuple:
            self.AddOrEdit.name = 'Изменить данные'  # Переименование кнопки "Внести данные" на "Изменить данные"
            self.DeleteData.hidden = False
            self.Name.value = current_items[0]
            self.Surname.value = current_items[1]
            self.Patronymic.value = current_items[2]
            self.Organization.value = current_items[3]
            self.WorkPhone.value = str(current_items[4])
            self.PersonalPhone.value = str(current_items[5])

        # При создании новой записи скрывается нерелевантная в данном случае кнопка удаления данных
        else:
            self.AddOrEdit.name = 'Внести данные'
            self.DeleteData.hidden = True

        self.display()

    # Ниже 6 функций, "печатающие" заглавные А/Е с помощью конкатенации (о причине подробнее в описании cursor_right())
    def name_ch(self, lit: str):
        self.Name.value = self.Name.value + lit
        cursor_right()

    def surname_ch(self, lit: str):
        self.Surname.value = self.Surname.value + lit
        cursor_right()

    def patronymic_ch(self, lit: str):
        self.Patronymic.value = self.Patronymic.value + lit
        cursor_right()

    def organization_ch(self, lit: str):
        self.Organization.value = self.Organization.value + lit
        cursor_right()

    def work_phone_ch(self, lit: str):
        self.WorkPhone.value = self.WorkPhone.value + lit
        cursor_right()

    def personal_phone_ch(self, lit: str):
        self.PersonalPhone.value = self.PersonalPhone.value + lit
        cursor_right()


class MenuForm(nps.Form):

    def create(self):
        self.add(nps.ButtonPress, name="Таблица", when_pressed_function=self.button1, relx=1, rely=1)
        self.add(nps.ButtonPress, name="Добавить запись", when_pressed_function=self.button2, relx=1, rely=2)
        self.add(nps.ButtonPress, name="Выйти из приложения", when_pressed_function=self.exit, relx=1, rely=4)

    def button1(self):
        self.parentApp.switchForm('TABLE')

    def button2(self):
        self.parentApp.switchForm('ADD')

    def exit(self):
        self.parentApp.switchForm(None)


class NewApplication(nps.NPSAppManaged):
    """
    Класс-менеджер форм
    """
    keypress_timeout_default = 5  # Определение задержки обновления формы с таблицей = 0,5 сек

    def onStart(self):
        """
        Функция объявляющая формы главного меню, таблицы и создания/изменения/удаление записей таблицы
        """
        self.addForm('MAIN', MenuForm, name='Menu')
        self.addForm('TABLE', TableForm, name='Table', draw_line_at=12)
        self.addForm('ADD', AddForm, name='Add')
