import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from cryptography.fernet import Fernet

class ConfigApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Settings")
        self.root.geometry("804x474")

        self.locations = set()
        self.key = b'xOp7kyOQNWgriHwqAg_9kde-wILCSDdEMZLoFdb9UOE='
        self.cipher = Fernet(self.key)

        self.create_widgets()
        self.load_saved_locations()

    def create_widgets(self):
        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        self.add_button = tk.Button(self.root, text="Add File", command=self.add_item)
        self.remove_button = tk.Button(self.root, text="Remove", command=self.remove_item)
        self.save_button = tk.Button(self.root, text='Save Location', command=self.save_locations)

        self.add_button.pack(anchor=tk.NE)
        self.remove_button.pack(anchor=tk.NE)
        self.save_button.pack(anchor=tk.NE)

    def add_item(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            if file_path not in self.locations:
                self.locations.add(file_path)
                self.listbox.insert(tk.END, file_path)
            else:
                messagebox.showerror("Error", "Location already added.")

    def remove_item(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select an item to remove.")
        else:
            index = selected_index[0]
            location = self.listbox.get(index)
            self.locations.discard(location)
            self.listbox.delete(index)

    def save_locations(self):
        formatted_locations = '\n'.join(self.locations)
        encrypted_data = self.cipher.encrypt(formatted_locations.encode('utf-8'))

        try:
            with open(r'C:\\s_s\\applocdata.dill', 'wb') as file:
                file.write(encrypted_data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save locations: {str(e)}")

    def load_saved_locations(self):
        try:
            with open(r'C:\\s_s\\applocdata.dill', 'rb') as file:
                encrypted_data = file.read()
                decrypted_data = self.cipher.decrypt(encrypted_data).decode('utf-8')

                # Populate the listbox with decoded locations
                locations_list = decrypted_data.split('\n')
                for location in locations_list:
                    if location:
                        self.locations.add(location)
                        self.listbox.insert(tk.END, location)

        except FileNotFoundError:
            return ''

    def fetch_locations(self):
        return list(self.locations)

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigApp(root)

    # Fetch the locations and print them at the start
    locations = app.fetch_locations()
    root.mainloop()
