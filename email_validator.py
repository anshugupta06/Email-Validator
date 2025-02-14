import dns.resolver
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # To handle images
from difflib import get_close_matches  # For typo correction

# Check if domain has MX records (i.e., mail servers exist for the domain)
# dns.resolver is used to check that the email that has been entered is able to send and receives emails.
def check_mx_record(domain):
    try:
        records = dns.resolver.resolve(domain, 'MX')
        return True if records else False    #true if MX or the email is valid otherwise false
    except dns.resolver.NoAnswer:
        return False
    except Exception as e:              #Handles exceptions to prevent the program from crashing if the DNS query fails.
        print("DNS Error:", e)
        return False

# List of static domains whose spelling shouldn't be changed
static_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com","aol.com", "zoho.com", "protonmail.com", "mail.com", "gmx.com","edu.com", "ac.in", "ac.uk", "alumni.stanford.edu", "alumni.harvard.edu",
    "mit.edu", "berkeley.edu", "ox.ac.uk", "cam.ac.uk", "ucla.edu","yandex.ru", "qq.com", "naver.com", "daum.net", "163.com",
    "126.com", "sina.com", "rediffmail.com", "indiatimes.com","web.de", "t-online.de", "orange.fr", "libero.it", "uol.com.br"]

# Email Validation Logic
def validate_email():
    email = entry_email.get().strip()  # Trim any surrounding whitespace
    k = j = d = 0

    # Condition 1: Maximum length of 254 characters
    if len(email) > 254:
        messagebox.showerror("Error", "Email must not exceed 254 characters.")
        return

    # Condition 2: Minimum length of 6 characters
    if len(email) >= 6:
        # Condition 3: First character must be an alphabet
        if email[0].isalpha():
            # Condition 4: Contains exactly one '@' character
            if ("@" in email) and (email.count("@") == 1):
                # Split email into username and domain parts
                username, domain = email.split("@")

                # Condition 5: Ends with a valid domain (.com, .net, etc.)
                if (email[-4] == ".") ^ (email[-3] == "."):
                    # Condition 6: If domain is in static_domains, it must be exactly the same
                    if any(domain.endswith(d) for d in static_domains):
                        if domain not in static_domains:
                            messagebox.showerror("Error", f"Domain must be exactly '{domain}' as it is a reserved domain.")
                            return
                    
                    # Typo Check for domains
                    if domain not in static_domains:
                        # Check for close matches with one character difference
                        close_matches = get_close_matches(domain, static_domains, n=1, cutoff=0.8)
                        if close_matches:
                            suggestion = close_matches[0]
                            messagebox.showerror("Error", f"Invalid domain. Did you mean '{suggestion}'?")
                            return
                        else:
                            messagebox.showerror("Error", "Invalid domain.")
                            return

                    # Condition 7: Special characters are allowed but not at start or end
                    special_chars = set("!#$%&'*+/=?^_`{|}~-")
                    if (email[0] in special_chars) or (email[-1] in special_chars):
                        messagebox.showerror("Error", "Special characters are not allowed at the start or end.")
                        return

                    # Loop to check each character
                    for i in email:
                        if i.isspace():
                            k = 1
                        elif i.isalpha():
                            if i.isupper():
                                j = 1
                        elif i.isdigit():
                            continue
                        elif i in ["_", ".", "@"] or i in special_chars:
                            continue
                        else:
                            d = 1
                    # Error messages for specific conditions
                    if k == 1:
                        messagebox.showerror("Error", "Email cannot contain spaces.")
                    elif j == 1:
                        messagebox.showerror("Error", "Uppercase letters are not allowed.")
                    elif d == 1:
                        messagebox.showerror("Error", "Invalid characters detected.")
                    else:
                        messagebox.showinfo("Success", "Valid Email!")
                else:
                    messagebox.showerror("Error", "Invalid domain format.")
            else:
                messagebox.showerror("Error", "Invalid '@' usage.")
        else:
            messagebox.showerror("Error", "First character must be an alphabet.")
    else:
        messagebox.showerror("Error", "Email must be at least 6 characters long.")
    email = entry_email.get().strip()  # Get email from input field
    if "@" in email:
        domain = email.split('@')[1]
        if check_mx_record(domain):
            messagebox.showinfo("Success", "Valid Email!")
        else:
            messagebox.showerror("Error", "Invalid domain or domain has no mail server.")
    else:
        messagebox.showerror("Error", "Invalid email format.")

def check_mx_record(domain):
    try:
        records = dns.resolver.resolve(domain, 'MX')
        return True if records else False
    except dns.resolver.NoAnswer:
        return False
    except Exception as e:
        print("DNS Error:", e)
        return False


# Hover Effect Functions
def on_enter(e):
    e.widget.config(bg="#007acc", fg="white")
def on_leave(e):
    e.widget.config(bg="#4da6ff", fg="white")

# Animated Heading Function
def animate_heading():
    current_text = heading.cget("text")
    new_text = current_text[1:] + current_text[0]  # Rotate text
    heading.config(text=new_text)
    heading.after(300, animate_heading)  # Adjust speed of animation

# Setting up the GUI window
root = tk.Tk()
root.title("Email Validation")
root.attributes('-fullscreen', True)  # Fullscreen mode

# Background Color and Pattern
root.configure(bg="#e6f7ff")  # Soft pastel blue background

# Frame for Email Panel
panel_frame = tk.Frame(root, bg="white", bd=2, relief="groove")
panel_frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=500)

# Animated Heading
heading = tk.Label(panel_frame, text="Email Validation", font=("Helvetica", 30, "bold"), bg="white", fg="#4da6ff")
heading.pack(pady=10)
animate_heading()

# Subheading
subheading = tk.Label(panel_frame, text="Check if your email is valid and formatted correctly!", font=("Helvetica", 12), bg="white", fg="#999999")
subheading.pack(pady=5)

# Fancy Divider
divider = tk.Frame(panel_frame, height=2, width=350, bg="#4da6ff")
divider.pack(pady=5)

# Email Entry
entry_frame = tk.Frame(panel_frame, bg="white")
entry_frame.pack(pady=20)
email_icon = tk.Label(entry_frame, text="✉️", font=("Helvetica", 16), bg="white")
email_icon.pack(side="left", padx=5)
entry_email = tk.Entry(entry_frame, font=("Helvetica", 16), bd=2, relief="solid")
entry_email.pack(side="left")

# Validate Button
validate_button = tk.Button(panel_frame, text="Validate Email", font=("Helvetica", 16, "bold"), bg="#4da6ff", fg="white", command=validate_email)
validate_button.pack(pady=10)
validate_button.bind("<Enter>", on_enter)
validate_button.bind("<Leave>", on_leave)

# Exit Button
exit_button = tk.Button(root, text="Exit", font=("Helvetica", 12), bg="#ff6666", fg="white", command=root.destroy)
exit_button.place(relx=0.98, rely=0.02, anchor="ne")
exit_button.bind("<Enter>", on_enter)
exit_button.bind("<Leave>", on_leave)

# Footer Text
footer = tk.Label(root, text="© 2025 Email Validator | Made with ❤️ using Tkinter", font=("Helvetica", 10), bg="#e6f7ff", fg="#666666")
footer.place(relx=0.5, rely=0.95, anchor="center")

# Loading Image
try:
    image = Image.open('/mnt/data/image.png')
    image = image.resize((100, 100), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(image)
    img_label = tk.Label(panel_frame, image=img, bg="white")
    img_label.pack(pady=5)
except Exception as e:
    print("Image loading failed:", e)

root.mainloop()
