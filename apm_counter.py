import time
from pynput import keyboard, mouse
from collections import deque
import threading
import tkinter as tk

# Deque to store timestamps of actions within the last 1.3 seconds
action_times = deque()

def estimate_apm():
    """Estimate APM based on actions in the past 1.3 seconds and update the GUI label."""
    while True:
        # Get current time
        current_time = time.time()
        
        # Remove actions that are older than 1.3 seconds
        while action_times and current_time - action_times[0] > 1.3:
            action_times.popleft()

        # Calculate APM by scaling the last 1.3 seconds of actions to a full minute
        apm_estimate = len(action_times) * 46.1538
        apm_label.config(text=f"{apm_estimate:.0f}")
        
        time.sleep(1)  # Update every second

def on_press(key):
    action_times.append(time.time())  # Log keyboard press

def on_click(x, y, button, pressed):
    if pressed:
        action_times.append(time.time())  # Log mouse click

# Set up tkinter GUI
root = tk.Tk()
root.title("APM Counter")
root.geometry("200x100")
root.resizable(False, False)

# Make the window float on top of other windows
root.attributes('-topmost', True)

# Create and place the APM label in the GUI
apm_label = tk.Label(root, text="Current APM: 0", font=("Helvetica", 36))
apm_label.pack(expand=True)

# Set up keyboard and mouse listeners
keyboard_listener = keyboard.Listener(on_press=on_press)
mouse_listener = mouse.Listener(on_click=on_click)

# Start the APM estimation thread
apm_thread = threading.Thread(target=estimate_apm)
apm_thread.daemon = True  # Run thread in the background
apm_thread.start()

# Start listeners for keyboard and mouse events
keyboard_listener.start()
mouse_listener.start()

# Start the tkinter main loop
root.mainloop()

# Stop listeners when GUI window is closed
keyboard_listener.stop()
mouse_listener.stop()
