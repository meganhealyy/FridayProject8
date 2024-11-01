import tkinter as tk
import sqlite3
import getpass

# Function to create the database and the feedback table if it doesn't exist
def create_database():
    conn = sqlite3.connect('feedback.db')  # Connect to (or create) the database
    cursor = conn.cursor()
    # Create a table for feedback if it doesn't exist already
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to save feedback data to the database
def submit_feedback():
    name = entry_name.get()  # Get the entered name
    email = entry_email.get()  # Get the entered email
    feedback = text_feedback.get("1.0", tk.END).strip()  # Get the feedback message

    if name and email and feedback:  # Check if all fields are filled
        conn = sqlite3.connect('feedback.db')  # Connect to the database
        cursor = conn.cursor()
        # Insert the feedback data into the database
        cursor.execute("INSERT INTO feedback (name, email, message) VALUES (?, ?, ?)", (name, email, feedback))
        conn.commit()  # Save the changes
        conn.close()
        # Clear the fields after submission
        entry_name.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        text_feedback.delete("1.0", tk.END)
        print("Feedback submitted successfully!")
    else:
        print("Please fill out all fields.")

# Function to retrieve and display all feedback entries, with password protection
def retrieve_data():
    # Prompt the user for a password (typed into the console)
    guess_password = input("Enter password to retrieve data: ")
    # Check if the password is correct (hardcoded for simplicity)
    if guess_password == "guess_password":  
        conn = sqlite3.connect('feedback.db')  # Connect to the database
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM feedback")  # Fetch all feedback entries
        all_feedback = cursor.fetchall()

        if all_feedback:
            for entry in all_feedback:
                print(f"ID: {entry[0]}, Name: {entry[1]}, Email: {entry[2]}, Feedback: {entry[3]}")
        else:
            print("No feedback entries found.")
        
        conn.close()
    else:
        print("Access denied. Incorrect password.")


# Function to set up the main GUI window
def setup_gui():
    global entry_name, entry_email, text_feedback  # Make these widgets accessible outside the function

    # Create the main window
    window = tk.Tk()
    window.title("Customer Feedback")

    # Name input
    label_name = tk.Label(window, text="Name")
    label_name.pack()
    entry_name = tk.Entry(window)
    entry_name.pack()

    # Email input
    label_email = tk.Label(window, text="Email")
    label_email.pack()
    entry_email = tk.Entry(window)
    entry_email.pack()

    # Feedback input
    label_feedback = tk.Label(window, text="Feedback")
    label_feedback.pack()
    text_feedback = tk.Text(window, height=5, width=40)
    text_feedback.pack()

    # Submit button to save feedback
    submit_button = tk.Button(window, text="Submit", command=submit_feedback)
    submit_button.pack()

    # Retrieve data button (triggers password prompt)
    retrieve_button = tk.Button(window, text="Retrieve Data", command=retrieve_data)
    retrieve_button.pack()

    # Start the Tkinter event loop
    window.mainloop()

# Main function to set up the database and start the GUI
if __name__ == "__main__":
    create_database()  # Create the feedback database if it doesn't exist
    setup_gui()  # Set up and start the GUI