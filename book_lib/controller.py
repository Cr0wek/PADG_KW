from tkinter import messagebox
from book_lib.model import User

class MapbookController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self._bind_buttons()
        self.load_users()

    def _bind_buttons(self):
        self.view.btn_add_save.config(command=self.add_user)
        self.view.btn_delete.config(command=self.delete_user)
        self.view.btn_details.config(command=self.show_details)
        self.view.btn_edit.config(command=self.prepare_edit)

    def load_users(self):
        users = self.model.fetch_all_users()
        self.view.refresh_list(users)

    def add_user(self):
        data = self.view.get_form_data()
        if not data['name'] or not data['location']:
            return
        
        try:
            new_user = User(data['name'], data['location'], int(data['posts']), data['img_url'])
            self.model.add_user(new_user)
            self.view.refresh_list(self.model.users)
            self.view.clear_form()
            # Focus map on new user
            self.view.map_widget.set_position(new_user.coords[0], new_user.coords[1])
        except Exception as e:
            print(f"Error adding user: {e}")

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