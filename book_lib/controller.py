from tkinter import messagebox
from book_lib.model import Artist, Event, Employee

class MapbookController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.load_data()



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
                self.view.listbox_artist.insert('end', artist.name)
                self.view.map_widget.set_marker(artist.coords[0], artist.coords[1], text=artist.name)
        elif mode=="Pracownik":
            curr_list=self.emplotees
            for emplotee in curr_list:
                self.view.listbox_artist.insert('end', emplotee.name)
                self.view.map_widget.set_marker(emplotee.coords[0], emplotee.coords[1], text=emplotee.name)

    def combobox_changed(self, event):
        self.view.map_widget.delete_all_marker()
        self.load_data()

    def add_entry(self):
        data = self.view.get_form_data()
        mode = data['mode']
        
        try:
            if mode == "Event":
                # f1=Name, f2=Location
                obj = Event(data['f1'], data['f2'])
                self.model.add_event(obj)
            
            elif mode == "Artist":
                # f1=Name, f2=Loc, f3=Nick, f4=EventID
                obj = Artist(data['f1'], data['f3'], data['f2'], int(data['f4']))
                self.model.add_artist(obj)
                
            elif mode == "Employee":
                # f1=Name, f2=Loc, f3=Role, f4=EventID
                obj = Employee(data['f1'], data['f3'], data['f2'], int(data['f4']))
                self.model.add_employee(obj)

            self.view.map_widget.delete_all_marker()
            self.refresh_all()
            
        except Exception as e:
            print(f"Nie udało się dodać: {e}")
            messagebox.showerror("Błąd", f"Nie udało się dodać obiektu: {e}")
            
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