import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import subprocess
import threading
import time
import os
import signal
import sys
import queue
import traceback

class ScriptOutput:
    def __init__(self, widget, prefix=""):
        self.widget = widget
        self.prefix = prefix
        self.queue = queue.Queue()
        self.running = True
        threading.Thread(target=self._update_output, daemon=True).start()
    
    def _update_output(self):
        while self.running:
            try:
                line = self.queue.get(block=True, timeout=0.1)
                self.widget.insert(tk.END, f"{self.prefix}{line}")
                self.widget.see(tk.END)
                self.queue.task_done()
            except queue.Empty:
                pass
            except Exception as e:
                print(f"Error updating output: {e}")
    
    def write(self, text):
        self.queue.put(text)
    
    def flush(self):
        pass
    
    def close(self):
        self.running = False

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Script Runner App")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Get the directory of the current script
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        if not self.script_dir:  # If it's an empty string, use current working directory
            self.script_dir = os.getcwd()
        
        # Configure the main window
        self.root.geometry("800x600")
        
        # Create the output text area
        self.output = ScrolledText(root, width=80, height=20)
        self.output.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.output.insert(tk.END, f"App Started...\n")
        self.output.insert(tk.END, f"Working directory: {self.script_dir}\n")
        self.output.insert(tk.END, f"Current working directory: {os.getcwd()}\n")
        self.output.insert(tk.END, f"Python executable: {sys.executable}\n")
        
        # List files in current directory for debugging
        try:
            files = os.listdir(self.script_dir)
            self.output.insert(tk.END, f"Files in directory: {', '.join(files)}\n")
        except Exception as e:
            self.output.insert(tk.END, f"Error listing directory: {str(e)}\n")
        
        # Create a frame for buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5, fill=tk.X)
        
        # Create buttons
        self.start_button = tk.Button(button_frame, text="Start Script B", command=self.start_script_b)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(button_frame, text="Stop Script B", command=self.stop_script_b, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Create a restart button for Script A
        self.restart_a_button = tk.Button(button_frame, text="Restart Script A", command=self.restart_script_a)
        self.restart_a_button.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initialize script process variables
        self.script_a_process = None
        self.script_b_process = None
        
        # Start Script A on startup
        self.run_script_a()
    
    def restart_script_a(self):
        # Stop Script A if running
        if self.script_a_process and self.script_a_process.poll() is None:
            try:
                if sys.platform == 'win32':
                    import subprocess
                    subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.script_a_process.pid)])
                else:
                    self.script_a_process.terminate()
                    
                # Give it some time to terminate
                time_waited = 0
                while self.script_a_process.poll() is None and time_waited < 3:
                    time.sleep(0.1)
                    time_waited += 0.1
            except Exception as e:
                self.output.insert(tk.END, f"[Error] Failed to stop Script A: {str(e)}\n")
                self.output.see(tk.END)
        
        # Start Script A again
        self.run_script_a()
    
    def run_script_a(self):
        def task():
            try:
                self.status_var.set("Starting Script A...")
                
                # Create a custom output stream for Script A
                script_a_output = ScriptOutput(self.output, "[Script A] ")
                
                # Create full path to server.py
                server_path = os.path.join(self.script_dir, "forward.py")
                
                # Check if file exists
                if not os.path.exists(server_path):
                    error_msg = f"ERROR: server.py not found at {server_path}\n"
                    script_a_output.write(error_msg)
                    self.status_var.set("Error: server.py not found")
                    return
                
                script_a_output.write(f"Starting server.py from: {server_path}\n")
                
                # Start the process with debug mode (show console)
                if sys.platform == 'win32':
                    # On Windows, use a visible console for debugging
                    self.script_a_process = subprocess.Popen(
                        [sys.executable, server_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,  # Capture stderr separately
                        text=True,
                        bufsize=1,
                        universal_newlines=True,
                        cwd=self.script_dir,  # Set working directory explicitly
                        creationflags=subprocess.CREATE_NO_WINDOW  # Remove to show console window
                    )
                else:
                    # On other platforms
                    self.script_a_process = subprocess.Popen(
                        [sys.executable, server_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,  # Capture stderr separately
                        text=True,
                        bufsize=1,
                        universal_newlines=True,
                        cwd=self.script_dir  # Set working directory explicitly
                    )
                
                script_a_output.write(f"Process started with PID: {self.script_a_process.pid}\n")
                
                # Function to read from a pipe and write to output
                def read_pipe(pipe, prefix=""):
                    try:
                        for line in iter(pipe.readline, ''):
                            script_a_output.write(f"{prefix}{line}")
                        pipe.close()
                    except Exception as e:
                        script_a_output.write(f"Error reading pipe: {str(e)}\n{traceback.format_exc()}\n")
                
                # Create threads to read stdout and stderr
                stdout_thread = threading.Thread(
                    target=read_pipe, 
                    args=(self.script_a_process.stdout, ""), 
                    daemon=True
                )
                stderr_thread = threading.Thread(
                    target=read_pipe, 
                    args=(self.script_a_process.stderr, "ERROR: "), 
                    daemon=True
                )
                
                stdout_thread.start()
                stderr_thread.start()
                
                # Wait for process to complete
                return_code = self.script_a_process.wait()
                
                # Wait for reader threads to finish
                stdout_thread.join(timeout=1.0)
                stderr_thread.join(timeout=1.0)
                
                if return_code != 0:
                    script_a_output.write(f"Script A exited with code {return_code}\n")
                    self.status_var.set(f"Script A exited with code {return_code}")
                
                script_a_output.close()
            except Exception as e:
                self.output.insert(tk.END, f"[Error] Failed to run Script A: {str(e)}\n{traceback.format_exc()}\n")
                self.output.see(tk.END)
                self.status_var.set("Error running Script A")
        
        threading.Thread(target=task, daemon=True).start()
    
    def start_script_b(self):
        if self.script_b_process is None or self.script_b_process.poll() is not None:
            try:
                self.status_var.set("Starting Script B...")
                self.output.insert(tk.END, "[App] Starting Script B...\n")
                self.output.see(tk.END)
                
                # Create a custom output stream for Script B
                script_b_output = ScriptOutput(self.output, "[Script B] ")
                
                # Create full path to detect.py
                detect_path = os.path.join(self.script_dir, "app_ml.py")
                
                # Check if file exists
                if not os.path.exists(detect_path):
                    error_msg = f"ERROR: detect.py not found at {detect_path}\n"
                    self.output.insert(tk.END, error_msg)
                    self.output.see(tk.END)
                    self.status_var.set("Error: detect.py not found")
                    return
                
                # Start the process with explicit path
                self.script_b_process = subprocess.Popen(
                    [sys.executable, detect_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                    cwd=self.script_dir  # Set working directory explicitly
                )
                
                # Update button states
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
                
                def monitor_script_b():
                    try:
                        # Read output continuously
                        for line in iter(self.script_b_process.stdout.readline, ''):
                            script_b_output.write(line)
                        
                        # Process has ended
                        self.script_b_process.stdout.close()
                        return_code = self.script_b_process.wait()
                        
                        if return_code != 0 and return_code is not None:
                            script_b_output.write(f"Script B exited with code {return_code}\n")
                        
                        # Update UI from main thread
                        self.root.after(0, self.reset_script_b_ui)
                        script_b_output.close()
                    except Exception as e:
                        self.output.insert(tk.END, f"[Error] Error monitoring Script B: {str(e)}\n{traceback.format_exc()}\n")
                        self.output.see(tk.END)
                        self.root.after(0, self.reset_script_b_ui)
                
                threading.Thread(target=monitor_script_b, daemon=True).start()
            except Exception as e:
                self.output.insert(tk.END, f"[Error] Failed to start Script B: {str(e)}\n{traceback.format_exc()}\n")
                self.output.see(tk.END)
                self.status_var.set("Error starting Script B")
    
    def reset_script_b_ui(self):
        """Reset the UI after Script B stops"""
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_var.set("Script B stopped")
    
    def stop_script_b(self):
        if self.script_b_process and self.script_b_process.poll() is None:
            self.status_var.set("Stopping Script B...")
            self.output.insert(tk.END, "[App] Stopping Script B...\n")
            self.output.see(tk.END)
            
            try:
                if sys.platform == 'win32':
                    import subprocess
                    subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.script_b_process.pid)])
                else:
                    self.script_b_process.terminate()
                    # Give it some time to terminate gracefully
                    time_waited = 0
                    while self.script_b_process.poll() is None and time_waited < 3:
                        time.sleep(0.1)
                        time_waited += 0.1
                    
                    # If still running, force kill
                    if self.script_b_process.poll() is None:
                        self.script_b_process.kill()
                
                self.output.insert(tk.END, "[App] Script B terminated\n")
                self.output.see(tk.END)
                self.reset_script_b_ui()
            except Exception as e:
                self.output.insert(tk.END, f"[Error] Failed to stop Script B: {str(e)}\n{traceback.format_exc()}\n")
                self.output.see(tk.END)
    
    def on_closing(self):
        """Handle window close event"""
        # Stop Script B if running
        if self.script_b_process and self.script_b_process.poll() is None:
            self.stop_script_b()
        
        # Stop Script A if running
        if self.script_a_process and self.script_a_process.poll() is None:
            try:
                if sys.platform == 'win32':
                    import subprocess
                    subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.script_a_process.pid)])
                else:
                    self.script_a_process.terminate()
            except:
                pass
        
        # Close the window
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()