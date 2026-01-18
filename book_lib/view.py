from tkinter import *
from tkinter import ttk
import tkintermapview


class MapbookView:
    def __init__(self, root):
        self.root = root
        self.root.title("Mapbook MVC")
        self.root.geometry("1500x870")
        self.markers = {}
    
        self._setup_frames()
        self._setup_lists()
        self._setup_form()
        self._setup_details()
        self._setup_map()
        self.form_update_fields()

    def _setup_frames(self):
        self.frame_list = Frame(self.root)
        self.frame_list_events = Frame(self.frame_list)
        self.frame_list_people = Frame(self.frame_list)
        self.frame_form = Frame(self.root)
        self.frame_details = Frame(self.root)
        self.frame_map = Frame(self.root)

        self.frame_list.grid(row=0, column=0)
        self.frame_form.grid(row=0, column=1)
        self.frame_details.grid(row=1, column=0, columnspan=2)
        self.frame_map.grid(row=2, column=0, columnspan=2)

    def _setup_lists(self):
        # Events 
        self.frame_list_events.grid(row=0, column=0)
        Label(self.frame_list_events, text="Wydarzenia:", font=("Arial", 10, "bold")).grid(row=0, column=0)
        self.listbox_event = Listbox(self.frame_list_events, width=40, height=10)
        self.listbox_event.grid(row=1, column=0)
        
        # People 
        self.frame_list_people.grid(row=0, column=1)
        self.combo_people = ttk.Combobox(self.frame_list_people, values=["Artyści", "Organizatorzy"])
        self.combo_people.current(0)
        self.combo_people.grid(row=0, column=1)
        self.listbox = Listbox(self.frame_list_people, width=40, height=10)
        self.listbox.grid(row=1, column=1)
        
        Label(self.frame_list_people, text="Filtruj wg wydarzenia:").grid(row=0, column=3)
        self.combo_filter = ttk.Combobox(self.frame_list_people, state='readonly')
        self.combo_filter.set("Wszystkie")
        self.combo_filter.grid(row=1, column=3)
        
        self.var_show_events=BooleanVar(value=True)
        self.checkbutton_show_events=Checkbutton(
            self.frame_list_people,
            text="Widoczność wydarzeń na mapie",
            variable=self.var_show_events,
            onvalue=True,
            offvalue=False
        ) 
        self.checkbutton_show_events.grid(row=2, column=3)       

        self.btn_delete = Button(self.frame_list, text="Usuń obiekt")
        self.btn_delete.grid(row=2, column=1)
        self.btn_edit = Button(self.frame_list, text="Edytuj obiekt")
        self.btn_edit.grid(row=2, column=2)

    def _setup_form(self):     
        Label(self.frame_form, text="Formularz:").grid(row=3, column=0, columnspan=2)
        self.mode = StringVar(value="Wydarzenie")
        self.rb_event = Radiobutton(self.frame_form, text="Dodaj wydarzenie", variable=self.mode, value="Wydarzenie", command=self.form_update_fields)
        self.rb_artist = Radiobutton(self.frame_form, text="Dodaj artystę", variable=self.mode, value="Artyści", command=self.form_update_fields)
        self.rb_empl = Radiobutton(self.frame_form, text="Dodaj organizatora", variable=self.mode, value="Organizatorzy", command=self.form_update_fields)
        self.rb_event.grid(row=0, column=0, sticky=W)
        self.rb_artist.grid(row=1, column=0, sticky=W)
        self.rb_empl.grid(row=2, column=0, sticky=W)
        
        self.label_1 = Label(self.frame_form, text="Nazwa wydarzenia: ")
        self.label_1.grid(row=4, column=0, sticky=W)
        self.label_2 = Label(self.frame_form, text="Miejsce wydarzenia: ")
        self.label_2.grid(row=5, column=0, sticky=W)
        self.label_3 = Label(self.frame_form, text="")
        self.label_3.grid(row=6, column=0, sticky=W)
        self.label_4 = Label(self.frame_form, text="")
        self.label_4.grid(row=7, column=0, sticky=W)

        self.entry_1 = Entry(self.frame_form)
        self.entry_1.grid(row=4, column=1)
        self.entry_2 = Entry(self.frame_form)
        self.entry_2.grid(row=5, column=1)
        self.entry_3 = Entry(self.frame_form)
        self.entry_3.grid(row=6, column=1)
        self.combo_event = ttk.Combobox(self.frame_form, width=30, state='readonly')
        self.combo_event.grid(row=7, column=1)

        self.btn_add_save = Button(self.frame_form, text="Dodaj obiekt", bg="#ffffff")
        self.btn_add_save.grid(row=8, column=0, columnspan=2)

    def form_update_fields(self):
        mode = self.mode.get()
        
        if mode == "Wydarzenie":
            self.label_1.config(text="Nazwa wydarzenia: ")
            self.label_2.config(text="Miejsce wydarzenia: ")
            self.label_3.config(text="")
            self.label_4.config(text="")
            self.entry_3.config(state='disabled')
            self.combo_event.set('')
            self.combo_event.config(state='disabled')
        elif mode == "Artyści":
            self.entry_1.config(state='normal')
            self.entry_2.config(state='normal')
            self.label_1.config(text="Imie i nazwisko: ")
            self.label_2.config(text="Lokalizacja: ")
            self.entry_3.config(state='normal')
            self.label_3.config(text="Pseudonim: ")
            self.combo_event.config(state='normal')
            self.label_4.config(text="Wydarzenie powiązane: ")
        elif mode == "Organizatorzy":
            self.entry_1.config(state='normal')
            self.entry_2.config(state='normal')
            self.label_1.config(text="Imie i nazwisko: ")
            self.label_2.config(text="Lokalizacja: ")
            self.entry_3.config(state='normal')
            self.label_3.config(text="Rola: ")
            self.combo_event.config(state='normal')
            self.label_4.config(text="Wydarzenie powiązane: ")


    def _setup_details(self):
        Label(self.frame_details, text="Szczegóły obiektu").grid(row=0, column=0, sticky=W)
        
        Label(self.frame_details, text="Imie: ").grid(row=1, column=0)
        self.lbl_val_name = Label(self.frame_details, text="....")
        self.lbl_val_name.grid(row=1, column=1)

        Label(self.frame_details, text="Lokalizacja: ").grid(row=1, column=2)
        self.lbl_val_loc = Label(self.frame_details, text="....")
        self.lbl_val_loc.grid(row=1, column=3)

        Label(self.frame_details, text="Posty: ").grid(row=1, column=4)
        self.lbl_val_posts = Label(self.frame_details, text="....")
        self.lbl_val_posts.grid(row=1, column=5)

    def _setup_map(self):
        self.map_widget = tkintermapview.TkinterMapView(self.frame_map, width=1500, height=600, corner_radius=10)
        self.map_widget.set_position(52.22977, 21.01178)
        self.map_widget.set_zoom(10)
        self.map_widget.grid(row=0, column=0)


    def get_form_data(self):
        return {
            'mode': self.mode.get(),
            'p1': self.entry_1.get(),
            'p2': self.entry_2.get(),
            'p3': self.entry_3.get(),
            'p4': self.combo_event.get()
        }

    def clear_form(self):
        self.entry_1.delete(0, END)
        self.entry_2.delete(0, END)
        self.entry_3.delete(0, END)
        self.btn_add_save.config(text="Dodaj obiekt", bg="#ffffff")
        
    def update_event_options(self, options):
        self.combo_event['values']=options
        filter_options=["Wszystkie"]+options
        self.combo_filter['values']=filter_options

    def fill_form(self, mode, p1, p2, p3="", p4=""):
        self.mode.set(mode)
        self.form_update_fields()
        self.clear_form()
        self.entry_1.insert(0, p1)
        self.entry_2.insert(0, p2)
        self.entry_3.config(state='normal')
        self.entry_3.insert(0, p3)
        
        self.combo_event.set(str(p4))
        
        if mode == "Wydarzenie":
            self.entry_3.config(state='disabled')
            self.combo_event.config(state='disabled')
        self.btn_add_save.config(text="Zapisz zmiany", bg="#69ff69")

    def refresh_list(self, users):
        self.listbox.delete(0, END)
        self.map_widget.delete_all_marker() # Czyszczenie mapy
        self.markers.clear()
        
        for user in users:
            self.listbox.insert(END, f'{user.name} from {user.location}')
            # Re-add marker
            marker = self.map_widget.set_marker(user.coords[0], user.coords[1], text=user.name)
            self.markers[user.id] = marker

    def show_details(self, user):
        self.lbl_val_name.config(text=user.name)
        self.lbl_val_loc.config(text=user.location)
        self.lbl_val_posts.config(text=str(user.posts))
        self.map_widget.set_position(user.coords[0], user.coords[1])
        
    def get_selected_index(self):
        if not self.listbox.curselection():
            return None
        return self.listbox.index(ACTIVE)