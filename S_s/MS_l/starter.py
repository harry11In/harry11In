import subprocess
from configer import ConfigApp
import tkinter as tk

def getloclist():
    root = tk.Tk()
    app = ConfigApp(root)
    locations = app.fetch_locations()
    root.destroy()
    
    # Remove duplicates by creating a set
    unique_locations = list(set(locations))
    
    return unique_locations

def creatloclist():
    list0 = getloclist()
    for item in list0:
        # Perform subprocess.call() for each item
        command = item  # item should be the actual command string
        subprocess.call(command, shell=True)

if __name__ == "__main__":
    creatloclist()
