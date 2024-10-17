from random import choice, shuffle
import pyperclip
from tkinter import *
from tkinter import messagebox
import json

COLOR = "Light Gray"
FONT = ("Poppins", 15, "normal")
BUTTON_FONT = ("Bungee", 10, "normal")
old_data = {}

# TODO:___________PASSWORD GENERATOR_____________
letters = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
    'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'i',
    'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
    'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'  'D'
    ]
numbers = [
    '0', '1', '2', '3', '4',
    '5', '6', '7', '8', '9'
    ]
symbols = [
    '!', '@', '#', '$', '%', '^',
    '&', '*', '(', ')', '-', '+'
    ]


def generate():
    password_letters = [choice(letters) for _ in range(5)]
    password_symbols = [choice(symbols)for _ in range(4)]
    password_numbers = [choice(numbers) for _ in range(5)]
    password = password_letters + password_symbols + password_numbers
    shuffle(password)
    new_password = "".join(password)
    password_entry.delete(0, END)
    password_entry.insert(END, string=f"{new_password}")
    pyperclip.copy(new_password)


# TODO:___________SAVE PASSWORD_____________


def read_json_data():
    with open("saved_password.json", "r") as data_file:
        global old_data
        old_data = json.load(data_file)


def write_jason_data(data):
    with open("saved_password.json", "w") as data_file:
        json.dump(data, data_file, indent=4)


def insert_data():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    user_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    if website == "" or password == "":
        messagebox.showwarning(
            title="Oops",
            message="Please do not left any field!"
        )
    elif "@" not in email or ".com" not in email:
        messagebox.showwarning(
            title="email error",
            message="Please enter a valid email\nlike xyz@abc.com"
        )
    else:
        result = messagebox.askquestion(
            title=f"{website}",
            message=f"These details are enter:\n"
                    f"email:{email}\n"
                    f"Password:{password}\n"
                    "Do you confirm to save?"
        )
        if result == "yes":
            try:
                read_json_data()
            except json.JSONDecodeError:
                write_jason_data(user_data)
            else:
                old_data.update(user_data)
                write_jason_data(old_data)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# TODO:___________FIND PASSWORD_____________


def search_data():
    try:
        read_json_data()
    except json.JSONDecodeError:
        messagebox.showinfo(title="Error", message="No data exist")
    else:
        website = website_string.get()
        if website in old_data:
            message_to_display = (
                f"Email: {old_data[website]["email"]}\n"
                f" Password: {old_data[website]["password"]}"
            )
        else:
            message_to_display = f"{website_string.get()} password is not exist"
        messagebox.showinfo(title=website_string.get(), message=message_to_display)


# TODO:___________UI SETUP_____________
window = Tk()
window.title("Password Manager")
window.config(bg=COLOR, width=500, height=400, padx=70, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0, bg=COLOR)
logo_img = PhotoImage(file="image.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:", font=FONT, bg=COLOR, highlightthickness=0)
website_label.grid(column=0, row=1)
website_string = StringVar()
website_entry = Entry(width=16, font=FONT, textvariable=website_string)
website_entry.grid(column=1, row=1)
website_entry.focus()

email_label = Label(text="Email/Username:", font=FONT, bg=COLOR, highlightthickness=0)
email_label.grid(column=0, row=2)
email_entry = Entry(width=25, font=FONT)
email_entry.insert(0, "azeemsher78@gmail.com")
email_entry.grid(column=1, row=2, columnspan=2)

password_label = Label(text="Password:", font=FONT, bg=COLOR, highlightthickness=0)
password_label.grid(column=0, row=3)
password_entry = (Entry(width=16, font=FONT))
password_entry.grid(column=1, row=3)


search_button = Button(
    width=8,
    text="Search",
    font=BUTTON_FONT,
    activeforeground="Red"
)
search_button.grid(column=2, row=1)
generate_button = Button(
    width=8,
    text="generate",
    font=BUTTON_FONT,
    activeforeground="Blue"
)
generate_button.grid(column=2, row=3)
add_button = Button(
    width=28,
    text="Add",
    font=BUTTON_FONT,
    activeforeground="Green"
)
add_button.grid(column=1, row=4, columnspan=2)
# Actions
search_button["command"] = search_data
generate_button["command"] = generate
add_button["command"] = insert_data
window.mainloop()
