# shell.py]
import supp

while True:
    text = input('supp > ')
    result, error = supp.run(text)

    if error:
        print(f"Error: {error}")
    else:
        for token in result:  # Fix: Use result instead of tokens
            print(token)
