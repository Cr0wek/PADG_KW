from tkinter import messagebox
from book_lib.model import Artist, Event, Employee

class MapbookController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.load_data()

        self.view.btn_add_save.config(command=self.add_entry)
        self.view.combo_people.bind("<<ComboboxSelected>>", self.combobox_changed)
        self.view.listbox_event.bind("<<ListboxSelect>>", self.on_event_select)
        self.view.listbox.bind("<<ListboxSelect>>", self.on_person_select)


    def load_data(self):
        self.events = self.model.fetch_events()
        self.artists = self.model.fetch_artists()
        self.emplotees = self.model.fetch_employees()
        
        self.view.listbox_event.delete(0, 'end')
        for event in self.events:
            self.view.listbox_event.insert('end', event.name)
            self.view.map_widget.set_marker(event.coords[0], event.coords[1], text=event.name)
            
        self.update_people_lists() #Updating combobox
        
    def update_people_lists(self):
        self.view.listbox.delete(0, 'end')
        mode=self.view.mode.get()
        if mode=="Artysta":
            curr_list=self.artists
            for artist in curr_list:
                self.view.listbox.insert('end', artist.full_name)
                self.view.map_widget.set_marker(artist.coords[0], artist.coords[1], text=artist.full_name)
        elif mode=="Organizator":
            curr_list=self.emplotees
            for emplotee in curr_list:
                self.view.listbox.insert('end', emplotee.full_name)
                self.view.map_widget.set_marker(emplotee.coords[0], emplotee.coords[1], text=emplotee.full_name)

    def combobox_changed(self, event):
        self.view.map_widget.delete_all_marker()
        self.load_data()

    def add_entry(self):
        data = self.view.get_form_data()
        mode = data['mode']
        
        # try:
        if mode == "Wydarzenie":
            # f1=Name, f2=Location
            obj = Event(data['p1'], data['p2'])
            self.model.add_event(obj)
        
        elif mode == "Artysta":
            # f1=Name, f2=Loc, f3=Nick, f4=EventID
            # obj = Artist(data['f1'], data['f3'], data['f2'], int(data['f4']))
            self.model.add_artist(Artist(data['p1'], data['p3'], data['p2'], int(data['p4'])))
            
        elif mode == "Organizator":
            # f1=Name, f2=Loc, f3=Role, f4=EventID
            obj = Employee(data['p1'], data['p3'], data['p2'], int(data['p4']))
            self.model.add_employee(obj)

        self.view.map_widget.delete_all_marker()
        self.load_data()
            
        # except Exception as e:
        #     print(f"Nie udało się dodać: {e}")
        #     messagebox.showerror("Błąd", f"Nie udało się dodać obiektu: {e}")
            
    def delete_user(self):
        idx = self.view.get_selected_index()
        if idx is None: return
        
        self.model.delete_user(idx)
        self.view.refresh_list(self.model.users)

    def show_details(self):
        idx = self.view.get_selected_index()
        if idx is None: return
        
        user = self.model.users[idx]
        self.view.show_details(user)

    def prepare_edit(self):
        idx = self.view.get_selected_index()
        if idx is None: return
        
        user = self.model.users[idx]
        self.view.fill_form(user)
        
        # Change button to "Update" mode
        self.view.btn_add_save.config(text="Zapisz zmiany", command=lambda: self.update_user(idx))

    def update_user(self, idx):
        data = self.view.get_form_data()
        
        updated_user = self.model.update_user(idx, data)
        self.view.refresh_list(self.model.users)
        self.view.show_details(updated_user) # Update details panel too
        
        # Reset form and button
        self.view.clear_form()
        self.view.btn_add_save.config(text="Dodaj obiekt", command=self.add_user)
        
    def on_event_select(self, event):
        idx = self.view.listbox_event.curselection()
        if not idx: return
        obj = self.events[idx[0]]
        self.view.map_widget.set_position(obj.coords[0], obj.coords[1])

    def on_person_select(self, event):
        idx = self.view.listbox.curselection()
        if not idx: return
        
        mode = self.view.combo_type.get()
        if mode == "Artysta":
            obj = self.artists[idx[0]]
        else:
            obj = self.employees[idx[0]]
            
        self.view.map_widget.set_position(obj.coords[0], obj.coords[1])