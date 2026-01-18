from book_lib.model import Artist, Event, Employee
from tkinter import messagebox

class MapbookController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self.edit_mode = False
        self.edit_idx = None
        self.edit_list_type = None
        
        self.events = []
        self.artists = []
        self.employees = []

        self.view.btn_add_save.config(command=self.save_data)
        self.view.btn_delete.config(command=self.delete_entry)
        self.view.btn_edit.config(command=self.prepare_edit)
        self.view.checkbutton_show_events.config(command=self.load_data)
        
        self.view.combo_people.bind("<<ComboboxSelected>>", self.combobox_changed)
        self.view.combo_filter.bind("<<ComboboxSelected>>", self.filter_changed)
        self.view.listbox_event.bind("<<ListboxSelect>>", self.on_event_select)
        self.view.listbox.bind("<<ListboxSelect>>", self.on_person_select)
        self.load_data()

    def load_data(self):
        self.events = self.model.fetch_events()
        self.artists = self.model.fetch_artists()
        self.employees = self.model.fetch_employees()
        
        event_names=[ev.name for ev in self.events]
        self.view.update_event_options(event_names)
        
        self.view.listbox_event.delete(0, 'end')
        self.view.map_widget.delete_all_marker()
        show_events=self.view.var_show_events.get()
        filter_value=self.view.combo_filter.get()
        for event in self.events:
            self.view.listbox_event.insert('end', event.name)
            if show_events == True:
                if filter_value=="Wszystkie" or filter_value==event.name:
                    self.addmarker(event.coords, event.name, 'green')
            
        self.update_people_lists()
        
    def update_people_lists(self):
        self.view.listbox.delete(0, 'end')
        mode=self.view.combo_people.get()
        filter_value=self.view.combo_filter.get()
        # print(mode)
        if mode=="Artyści":
            curr_list=self.artists
            marker_color='red'
        elif mode=="Organizatorzy":
            curr_list=self.employees
            marker_color='blue'
                
        for p in curr_list:
            if filter_value == "Wszystkie" or p.event_name == filter_value:
                self.view.listbox.insert('end', f"{p.full_name} -> {p.event_name}")
                self.addmarker(p.coords, p.full_name, marker_color)

    def addmarker(self, coords, text, color):
        self.view.map_widget.set_marker(coords[0], coords[1], text=text, marker_color_outside=color, marker_color_circle=f"dark{color}")

    def filter_changed(self, event):
        self.load_data()
        
    def combobox_changed(self, event):
        self.view.map_widget.delete_all_marker()
        self.load_data()
            
    def delete_entry(self):
        idx_event = self.view.listbox_event.curselection()
        idx_people = self.view.listbox.curselection()
        filter_value=self.view.combo_filter.get()
        if idx_people:
            if filter_value != "Wszystkie":
                messagebox.showwarning("Ostrzeżenie", "W celu usunięcia osoby przełącz filtr na 'Wszystkie'")
                return
            idx=idx_people[0]
            mode=self.view.combo_people.get()
            if mode == "Artyści":
                self.model.delete_artist(idx)
            else:
                self.model.delete_employee(idx)
            print("Usunięto osobę z listy")
        elif idx_event:
            idx=idx_event[0]
            self.model.delete_event(idx)
            print("Usunięto wydarzenie")
            
        else:
            print("Nic nie zaznaczono")
            messagebox.showwarning("Ostrzeżenie", "Zaznacz użytkownika/wydarzenie")
            
        self.view.clear_form()
        self.load_data()

    def show_details(self):
        idx = self.view.get_selected_index()
        if idx is None: return
        
        user = self.model.users[idx]
        self.view.show_details(user)

    def prepare_edit(self):
        idx_event = self.view.listbox_event.curselection()
        idx_people = self.view.listbox.curselection()
        
        if idx_people:
            idx=idx_people[0]
            mode=self.view.combo_people.get()
            if mode == "Artyści" and idx < len(self.artists):
                obj=self.artists[idx]
                self.view.fill_form("Artyści", obj.full_name, obj.location, obj.nickname, obj.event_name)
                self.edit_list_type="artist"
            if mode == "Organizatorzy" and idx < len(self.employees):
                obj=self.employees[idx]
                self.view.fill_form("Organizatorzy", obj.full_name, obj.location, obj.role, obj.event_name)
                self.edit_list_type="employee"
            self.edit_mode=True
            print("Tryb edycji ON")
            self.edit_idx=idx
        elif idx_event:
            idx=idx_event[0]
            if idx<len(self.events):
                obj=self.events[idx]
                self.view.fill_form("Wydarzenie", obj.name, obj.location)
                self.edit_list_type="event"
                self.edit_mode=True
                self.edit_idx=idx
        else:
            messagebox.showwarning("Ostrzeżenie", "Zaznacz użytkownika/wydarzenie")
            print("Nie zaznaczono elementu do edycji")

    def save_data(self):
        data = self.view.get_form_data()
        
        if self.edit_mode:
            if self.edit_list_type == "event":
                self.model.update_event(self.edit_idx, data)
            elif self.edit_list_type=="artist":
                self.model.update_artist(self.edit_idx, data)
            elif self.edit_list_type=="employee":
                self.model.update_employee(self.edit_idx, data)
            print("Zaktualizowano dane")
            self.edit_mode=False
            self.edit_idx=None
            self.edit_list_type=None
        else:
            mode = data['mode']
            if mode == "Wydarzenie":
                self.model.add_event(Event(data['p1'], data['p2']))
            elif mode == "Artyści":
                self.model.add_artist(Artist(data['p1'], data['p3'], data['p2'], data['p4']))
            elif mode == "Organizatorzy":
                self.model.add_employee(Employee(data['p1'], data['p3'], data['p2'], data['p4']))
            
        self.view.clear_form()
        self.load_data()
            
    def on_event_select(self, event):
        idx = self.view.listbox_event.curselection()
        if not idx: return
        obj = self.events[idx[0]]
        self.view.map_widget.set_position(obj.coords[0], obj.coords[1])
        self.view.map_widget.set_zoom(10)

    def on_person_select(self, event):
        idx = self.view.listbox.curselection()
        if not idx: return
        
        mode = self.view.combo_people.get()
        if mode == "Artyści":
            obj = self.artists[idx[0]]
            self.view.lbl_val_3.config(text=f"Pseudonim: {obj.nickname}")
        else:
            obj = self.employees[idx[0]]
            # extra = getattr(obj, 'nickname', getattr(obj, 'role', ''))
            self.view.lbl_val_3.config(text=f"Rola: {obj.role}")
        
        self.view.lbl_val_1.config(text=f"Imię i nazwisko: {obj.full_name}")
        self.view.lbl_val_2.config(text=f"Lokalizacja: {obj.location}")