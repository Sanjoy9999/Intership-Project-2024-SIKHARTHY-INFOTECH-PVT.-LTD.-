import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime




from updateDataSetAndCreateNewModel import TakeImage
from updateDataSetAndCreateNewModel import remove_User
from csvManager import takeAndSaveAttendance, fetch_attendance_data



def mainApp():
    


    menu_bar = tk.Menu(app)

    menu_bar.add_command(label="Attendance", command=show_attendance)
    menu_bar.add_command(label="Add User", command=lambda:admin_login('add_user'))
    menu_bar.add_command(label="Remove User", command=lambda:admin_login('remove_user'))
    menu_bar.add_command(label="Help", command=show_help)
    app.config(menu=menu_bar)
    


    app.configure(background='#708090')
    home_label = tk.Label(app, text="Welcome to the Face Recognition Based Attendance System" ,fg="white",bg="#708090" ,width=60 ,height=6,font=('times', 29, ' bold '))
    home_label.place(x=15, y=30)
    

    # Create a frame to display the current date and time
    frame1 = tk.Frame(app, bg="#c4c6ce")
    frame1.place(relx=0.45, rely=0.09, relwidth=0.25, relheight=0.07)

    frame2 = tk.Frame(app, bg="#c4c6ce")
    frame2.place(relx=0.25, rely=0.09, relwidth=0.27, relheight=0.07)

    # Get the current date
    now = datetime.datetime.now()
    day = now.day
    month = now.month
    year = now.year

    datef = tk.Label(frame2, text = str(day)+"-"+str(month)+"-"+str(year)+"                |       ", fg="orange",bg="green" ,height=5,font=('times', 20, ' bold '))
    datef.pack(fill='both')

    def update_clock():
        # Get the current time
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        clock.config(text=current_time)
        clock.after(1000, update_clock)

    clock = tk.Label(frame1,fg="orange",bg="green" ,width=40 ,height=5,font=('times', 20, ' bold '))
    clock.pack(fill='both')

    # Update the clock every second
    update_clock()
    

    

    # Button to start the camera
    start_camera_button = tk.Button(app, text="Take Attendance", command=takeAndSaveAttendance,bg="blue", font=("Arial", 15),border=5)
    start_camera_button.pack(pady=10)
    start_camera_button.place(x=600,y=300)    


def back():
    for widget in app.winfo_children():
        widget.destroy()
    mainApp()


def show_attendance():
    for widget in app.winfo_children():
        widget.destroy()

    # Fetch attendance data from the CSV file
    records = fetch_attendance_data()

    # Display a title
    title_label = tk.Label(app, text="Attendance Records", font=("Arial", 20),bg="green",border=5)
    title_label.pack(pady=10)

    # Create a Treeview widget with a vertical scrollbar
    tree_frame = tk.Frame(app)
    tree_frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(tree_frame, columns=("Name", "Date", "Time(1.Entry time  2.Out time)", "Status"), show="headings")
    tree.pack(side="left", fill="both", expand=True)

    # Create a vertical scrollbar for the Treeview
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")

    # Define column headers and center-align the data
    headers = ["Name", "Date", "Time(1.Entry time  2.Out time)", "Status"]
    for header in headers:
        tree.heading(header, text=header)
        tree.column(header, width=100, anchor="center")  # Center-align the data

    # Insert the attendance records into the Treeview
    for record in records:
        tree.insert("", "end", values=record)

    # Add a button to return to the home page
    home_button = tk.Button(app, text="Back", command=back, font=("Arial", 15),bg="LightCoral",border=5)
    home_button.pack(pady=10)

def admin_login(x):
    login_window = tk.Toplevel(app,bg="DarkGoldenRod")
    login_window.title("Admin Login")

    # Calculate the screen width and height
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    # Calculate the x and y coordinates to center the login window
    x_coordinate = int((screen_width / 2) - (300 / 2))
    y_coordinate = int((screen_height / 2) - (400 / 2))

    # Set the login window size and position
    login_window.geometry(f"300x200+{x_coordinate}+{y_coordinate}")

    user_id_label = tk.Label(login_window, text="User ID")
    user_id_label.pack(pady=5)

    user_id_entry = tk.Entry(login_window)
    user_id_entry.pack(pady=5)

    password_label = tk.Label(login_window, text="Password")
    password_label.pack(pady=5)

    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    login_button = tk.Button(login_window, text="Login", command=lambda: perform_login(user_id_entry.get(), password_entry.get(), login_window, x),bg="LimeGreen",border=5)
    login_button.pack(pady=20)

def perform_login(user_id, password, window,x):
    if user_id == "admin" and password == "password": 
        window.destroy() 
        if x == 'add_user':
            addUser()
        elif x == 'remove_user':
            removeUser()    
    else:
        messagebox.showerror("Login Failed", "Incorrect username or password.")
        

def addUser():
    # Clear the main window
    for widget in app.winfo_children():
        widget.destroy()

    # Display a title
    title_label = tk.Label(app, text="Add New User", font=("Arial", 20),bg="BlueViolet",fg="white")
    title_label.pack(pady=10)

    user_id_label = tk.Label(app, text="ENTER YOUR NAME", font=("Arial", 15))
    user_id_label.pack(pady=5)

    user_name = tk.Entry(app)
    user_name.pack(pady=5)

    home_button = tk.Button(app, text="Take User Image", command=lambda: TakeImage(user_name.get()), font=("Arial", 15),bg="DarkViolet",border=5)
    home_button.pack(pady=10)

    home_button = tk.Button(app, text="Back", command=back, font=("Arial", 15),bg="Green",border=5)
    home_button.pack(pady=10)


def removeUser():
    # Clear the main window
    for widget in app.winfo_children():
        widget.destroy()

    # Display a title
    title_label = tk.Label(app, text="Remove User", font=("Arial", 20))
    title_label.pack(pady=10)

    user_id_label = tk.Label(app, text="ENTER YOUR NAME", font=("Arial", 15))
    user_id_label.pack(pady=5)

    user_name = tk.Entry(app)
    user_name.pack(pady=5)

    home_button = tk.Button(app, text="Remove User", command=lambda: remove_User(user_name.get()), font=("Arial", 15),bg="DarkRed",border=5)
    home_button.pack(pady=10)

    home_button = tk.Button(app, text="Back", command=back, font=("Arial", 15),bg="Green",border=5)
    home_button.pack(pady=10)


def show_help():
    help_window = tk.Toplevel(app,bg="green")
    help_window.title("Help")

    # Calculate the screen width and height
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    # Calculate the x and y coordinates to center the login window
    x_coordinate = int((screen_width / 2) - (300 / 2))
    y_coordinate = int((screen_height / 2) - (400 / 2))

    # Set the login window size and position
    help_window.geometry(f"400x300+{x_coordinate}+{y_coordinate}")
    
    
    
    help_text = """This app is designed to take attendance using face recognition.
    
1. **Home**: Access the camera to recognize faces and mark attendance.
2. **Attendance**: View the attendance records for the day, including entry and exit times.
3. **Admin**: Admin login for managing attendance records and system settings.
4. **Help**: Get information on how to use the app.

To use the app, click on 'Home' to start face recognition and log attendance. The system will automatically record the time of entry and exit based on recognition events."""
    
    label = tk.Label(help_window, text=help_text, wraplength=350, justify="left", padx=10, pady=10,bg="green",fg="white")
    label.pack(expand=True, fill="both")

    close_button = tk.Button(help_window, text="Close", command=help_window.destroy,bg="LightCoral",border=5)
    close_button.pack(pady=10)


if __name__ == "__main__":
    
    app = tk.Tk()
    app.title("Face Recognition Attendance System")
    app.minsize(1300,500)
    mainApp()
    app.mainloop()

