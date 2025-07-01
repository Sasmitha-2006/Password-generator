from string import ascii_letters, digits, punctuation
from random import choice, sample
import tkinter as tk
from tkinter import messagebox

# === Helper Functions ===

def is_even(integer):
    return integer % 2 == 0

def evaluate_strength(password):
    length = len(password)
    diversity_score = sum([
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in punctuation for c in password),
    ])

    if length < 8:
        return 'VERY WEAK', "#6d0001"
    elif length < 10:
        return 'WEAK', "#cc0000"
    elif length < 12:
        return 'DECENT', "#fc8600"
    elif length < 14:
        return 'GOOD', "#eae200"
    elif length < 16:
        return 'STRONG', "#9ff400"
    elif diversity_score == 4:
        return 'EXCELLENT', "#007715"
    else:
        return 'VERY STRONG', "#001fef"

def calculate_entropy(password):
    pool_size = sum([
        26 if any(c.islower() for c in password) else 0,
        26 if any(c.isupper() for c in password) else 0,
        10 if any(c.isdigit() for c in password) else 0,
        len(punctuation) if any(c in punctuation for c in password) else 0,
    ])
    from math import log2
    return len(password) * log2(pool_size) if pool_size else 0

def generate_password(passlen=8, include_chars="", exclude_chars=""):
    if passlen < 4:
        raise ValueError("Password length must be at least 4.")

    s0 = punctuation.replace(' ', '')
    s1 = ascii_letters
    s3 = digits

    s = s0 + s1
    s_full = s + s3

    if include_chars:
        s_full += include_chars
    if exclude_chars:
        s_full = ''.join(c for c in s_full if c not in exclude_chars)

    pass0 = choice(s0)
    pass1 = "".join(sample(s_full, passlen - 2))
    pass2 = choice(s3)

    password = pass0 + pass1 + pass2
    if password[-1] == ' ':
        password = password[:-1] + choice(s)

    return password

# === New Unique Features ===

def readability_score(password):
    vowels = "aeiouAEIOU"
    score = sum(1 for i in range(1, len(password)) if password[i-1] in vowels and password[i] not in vowels)
    return min(100, int((score / len(password)) * 100))

def password_expiry_recommendation(strength):
    days = {
        "VERY WEAK": 7,
        "WEAK": 15,
        "DECENT": 30,
        "GOOD": 60,
        "STRONG": 90,
        "VERY STRONG": 180,
        "EXCELLENT": 365
    }
    return f"Recommended to change after {days.get(strength, 60)} days."

def detect_weak_patterns(password):
    for i in range(len(password) - 2):
        seq = password[i:i+3]
        if all(ord(seq[j]) + 1 == ord(seq[j + 1]) for j in range(2)):
            return "Contains sequential characters (e.g., abc or 123)"
        if seq[0] == seq[1] == seq[2]:
            return "Contains repeated characters (e.g., aaa)"
    return "No weak patterns detected."

# === GUI ===

def show_result(password, strength, color):
    def copy_to_clipboard():
        root.clipboard_clear()
        root.clipboard_append(password)
        root.update()
        messagebox.showinfo("Copied", "Password copied to clipboard!")

    def regenerate():
        new_password = generate_password(len(password))
        new_strength, new_color = evaluate_strength(new_password)
        root.destroy()
        show_result(new_password, new_strength, new_color)

    def toggle_password_visibility():
        if password_label.cget('text') == password:
            password_label.config(text="*" * len(password))
        else:
            password_label.config(text=password)

    entropy = calculate_entropy(password)
    readability = readability_score(password)
    expiry = password_expiry_recommendation(strength)
    pattern_warning = detect_weak_patterns(password)

    root = tk.Tk()
    root.title("Password Generator Result")
    root.geometry("480x460")
    root.configure(bg=color)

    tk.Label(root, text="Generated Password:", font=("Arial", 12), bg=color, fg="white").pack(pady=(10, 0))
    password_label = tk.Label(root, text=password, font=("Arial", 16, "bold"), bg=color, fg="white")
    password_label.pack(pady=(0, 10))

    tk.Label(root, text="Strength Level:", font=("Arial", 12), bg=color, fg="white").pack()
    tk.Label(root, text=strength, font=("Arial", 14, "bold"), bg=color, fg="white").pack(pady=(0, 10))

    tk.Label(root, text=f"Entropy: {entropy:.2f} bits", font=("Arial", 12), bg=color, fg="white").pack(pady=(5, 5))
    tk.Label(root, text=f"Readability Score: {readability}%", font=("Arial", 11), bg=color, fg="white").pack(pady=(0, 5))
    tk.Label(root, text=expiry, font=("Arial", 11), bg=color, fg="white").pack(pady=(0, 5))
    tk.Label(root, text=f"Pattern Check: {pattern_warning}", font=("Arial", 11), bg=color, fg="white", wraplength=440).pack(pady=(0, 10))

    tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, font=("Arial", 10), bg="white", fg="black").pack(pady=(5, 5))
    tk.Button(root, text="Regenerate Password", command=regenerate, font=("Arial", 10), bg="white", fg="black").pack(pady=(5, 5))
    tk.Button(root, text="Show/Hide Password", command=toggle_password_visibility, font=("Arial", 10), bg="white", fg="black").pack(pady=(5, 5))

    root.mainloop()

# === Main Execution ===

if __name__ == "__main__":
    try:
        user_input = int(input("Enter desired password length (minimum 4): "))
        include_chars = input("Enter characters to include (optional): ")
        exclude_chars = input("Enter characters to exclude (optional): ")

        if user_input < 4:
            print("Password length must be at least 4.")
        else:
            password = generate_password(user_input, include_chars, exclude_chars)
            strength, color = evaluate_strength(password)
            show_result(password, strength, color)

    except ValueError:
        print("Invalid input. Please enter an integer.")
