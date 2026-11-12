"""
Personal Toolkit
----------------
A menu-driven program with four tools:
  1. Unit Converter       - length, weight and temperature conversions
  2. Expense Tracker      - record purchases, see totals by category
  3. Password Checker     - scores a password and suggests improvements
  4. Flashcard Quiz       - practice Python keywords and functions
"""

import random

BIG_EXPENSE = 100.0  # expenses at or above this amount are flagged

LENGTH_TO_METRES = {"m": 1.0, "km": 1000.0, "ft": 0.3048, "mi": 1609.344}
WEIGHT_TO_KG = {"kg": 1.0, "g": 0.001, "lb": 0.45359237, "oz": 0.0283495}

COMMON_PASSWORDS = ["password", "123456", "qwerty", "letmein", "admin"]

FLASHCARDS = [
    {"question": "Which keyword starts a function definition?", "answer": "def"},
    {"question": "Which keyword starts a loop that repeats while a condition holds?", "answer": "while"},
    {"question": "Which function reads text typed by the user?", "answer": "input"},
    {"question": "Which function shows text on the screen?", "answer": "print"},
    {"question": "Which keyword adds another condition after an if?", "answer": "elif"},
    {"question": "Which list method adds an item to the end?", "answer": "append"},
    {"question": "Which keyword opens a file so it closes automatically?", "answer": "with"},
    {"question": "Which function returns the number of items in a list?", "answer": "len"},
]


# ---------- Shared helper ----------

def ask_number(prompt):
    """Keep asking until the user types a valid number. Returns a float."""
    while True:
        text = input(prompt).strip()
        try:
            return float(text)
        except ValueError:
            print(f"  '{text}' is not a number. Please try again.")


# ---------- Tool 1: Unit Converter ----------

# Converts length or weight by changing the value into a base unit first,
# then into the target unit.
def convert_length_or_weight(table, kind):
    print(f"Units: {', '.join(table)}")
    source = input("From unit: ").strip().lower()
    target = input("To unit: ").strip().lower()
    if source not in table or target not in table:
        print("  Please use one of the units listed above.")
        return
    value = ask_number("Value: ")
    result = value * table[source] / table[target]
    print(f"  {value:g} {source} = {result:,.4g} {target}")


# Temperature needs its own formulas, so it converts through Celsius.
def convert_temperature():
    print("Scales: C (Celsius), F (Fahrenheit), K (Kelvin)")
    source = input("From scale: ").strip().upper()
    target = input("To scale: ").strip().upper()
    if source not in ("C", "F", "K") or target not in ("C", "F", "K"):
        print("  Please use C, F or K.")
        return
    value = ask_number("Value: ")

    # Step 1: convert the value to Celsius
    if source == "F":
        celsius = (value - 32) * 5 / 9
    elif source == "K":
        celsius = value - 273.15
    else:
        celsius = value

    # Step 2: convert from Celsius to the target scale
    if target == "F":
        result = celsius * 9 / 5 + 32
    elif target == "K":
        result = celsius + 273.15
    else:
        result = celsius

    print(f"  {value:g} {source} = {result:.2f} {target}")


# Loop keeps the converter open until the user types 'back'.
def unit_converter():
    print("\n--- Unit Converter ---")
    while True:
        kind = input("Type (length, weight, temperature, or back): ").strip().lower()
        if kind == "back":
            print("  Leaving the Unit Converter.")
            return
        elif kind == "length":
            convert_length_or_weight(LENGTH_TO_METRES, "length")
        elif kind == "weight":
            convert_length_or_weight(WEIGHT_TO_KG, "weight")
        elif kind == "temperature":
            convert_temperature()
        else:
            print("  Please choose length, weight, temperature, or back.")


# ---------- Tool 2: Expense Tracker ----------

# The expenses list grows and shrinks while the program runs.
# Each expense is a dictionary with item, amount and category.
def expense_tracker():
    print("\n--- Expense Tracker ---")
    expenses = []

    while True:
        print("\n1. Add expense   2. View expenses   3. Summary by category")
        print("4. Remove last expense   5. Back")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            item = input("What did you buy? ").strip()
            if item == "":
                print("  The item name cannot be empty.")
                continue
            amount = ask_number("Amount: ")
            if amount <= 0:
                print("  The amount must be greater than zero.")
                continue
            category = input("Category (e.g. food, transport, fun): ").strip().title() or "Other"
            expenses.append({"item": item, "amount": amount, "category": category})
            flag = " (large expense)" if amount >= BIG_EXPENSE else ""
            print(f"  Added {item} for {amount:.2f}{flag}.")

        elif choice == "2":
            if len(expenses) == 0:
                print("  No expenses recorded yet.")
                continue
            for number, expense in enumerate(expenses, start=1):
                print(f"  {number}. {expense['item']:<20} {expense['amount']:>10.2f}  [{expense['category']}]")

        elif choice == "3":
            if len(expenses) == 0:
                print("  No expenses recorded yet.")
                continue
            # Build a dictionary of totals per category
            totals = {}
            for expense in expenses:
                category = expense["category"]
                totals[category] = totals.get(category, 0) + expense["amount"]
            grand_total = sum(totals.values())
            for category in sorted(totals):
                share = totals[category] / grand_total * 100
                print(f"  {category:<12} {totals[category]:>10.2f}  ({share:.0f}%)")
            print(f"  {'TOTAL':<12} {grand_total:>10.2f}")

        elif choice == "4":
            if len(expenses) == 0:
                print("  Nothing to remove.")
                continue
            removed = expenses.pop()
            print(f"  Removed {removed['item']}.")

        elif choice == "5":
            print("  Leaving the Expense Tracker.")
            return

        else:
            print("  Please choose a number from 1 to 5.")


# ---------- Tool 3: Password Checker ----------

# Checks the password against a set of rules, gives it a score out of 6,
# and suggests what to add. The password is not saved anywhere.
def password_checker():
    print("\n--- Password Checker ---")
    print("Your password is only checked here. It is never stored.")
    password = input("Enter a password to check (or press Enter to go back): ")
    if password == "":
        print("  Leaving the Password Checker.")
        return

    has_lower = has_upper = has_digit = has_symbol = False
    for character in password:
        if character.islower():
            has_lower = True
        elif character.isupper():
            has_upper = True
        elif character.isdigit():
            has_digit = True
        else:
            has_symbol = True

    rules = [
        (len(password) >= 8, "at least 8 characters"),
        (len(password) >= 12, "at least 12 characters"),
        (has_lower, "a lowercase letter"),
        (has_upper, "an uppercase letter"),
        (has_digit, "a number"),
        (has_symbol, "a symbol such as ! or #"),
    ]
    score = 0
    suggestions = []
    for passed, message in rules:
        if passed:
            score += 1
        else:
            suggestions.append(message)

    # Decide the rating. A very common password is always weak.
    if password.lower() in COMMON_PASSWORDS:
        rating = "Weak"
    elif score <= 2:
        rating = "Weak"
    elif score <= 4:
        rating = "Fair"
    elif score == 5:
        rating = "Good"
    else:
        rating = "Strong"

    print(f"\n  Score: {score} out of 6")
    print(f"  Rating: {rating}")
    if password.lower() in COMMON_PASSWORDS:
        print("  This is a very common password. Choose something unique.")
    if suggestions:
        print("  To improve it, add: " + "; ".join(suggestions) + ".")
    else:
        print("  Every rule is met. Nice work!")


# ---------- Tool 4: Flashcard Quiz ----------

# Asks one flashcard and returns True if the answer is correct.
def ask_card(card, number, total):
    print(f"\nQuestion {number} of {total}: {card['question']}")
    answer = input("Your answer (or 'quit' to stop): ").strip().lower()
    if answer == "quit":
        return None  # None means the user wants to stop
    if answer == card["answer"]:
        print("  Correct!")
        return True
    print(f"  Not quite. The answer is '{card['answer']}'.")
    return False


# Shuffles the cards, asks each one, and keeps a list of missed cards
# so the user can retry them at the end.
def flashcard_quiz():
    print("\n--- Flashcard Quiz ---")
    deck = list(FLASHCARDS)
    random.shuffle(deck)

    score = 0
    answered = 0
    missed = []  # grows while the quiz runs

    for number, card in enumerate(deck, start=1):
        result = ask_card(card, number, len(deck))
        if result is None:
            break
        answered += 1
        if result:
            score += 1
        else:
            missed.append(card)

    if answered == 0:
        print("  No questions answered.")
        return

    print(f"\nYou scored {score} out of {answered}.")

    if missed and input("Retry the cards you missed? (y/n): ").strip().lower() == "y":
        retry_deck = missed
        missed = []
        for number, card in enumerate(retry_deck, start=1):
            result = ask_card(card, number, len(retry_deck))
            if result is None:
                break
            if result:
                score += 1
            else:
                missed.append(card)
        if missed:
            print(f"Still {len(missed)} to review. Keep practising!")
        else:
            print("You got every retried card right. Excellent!")


# ---------- Main menu ----------

def show_welcome():
    print("==========================================")
    print("     Welcome to your Personal Toolkit!")
    print("==========================================")


def show_menu():
    print("\n==========================")
    print("   MY PERSONAL TOOLKIT")
    print("==========================")
    print("1. Unit Converter")
    print("2. Expense Tracker")
    print("3. Password Checker")
    print("4. Flashcard Quiz")
    print("5. Quit")
    print("==========================")


# Keeps showing the menu until the user chooses Quit.
def main():
    show_welcome()
    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            unit_converter()
        elif choice == "2":
            expense_tracker()
        elif choice == "3":
            password_checker()
        elif choice == "4":
            flashcard_quiz()
        elif choice == "5":
            print("\nThanks for using the Personal Toolkit. Goodbye!")
            break
        else:
            print(f"  Sorry, '{choice}' is not on the menu. Please choose 1 to 5.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nProgram stopped. Goodbye!")
