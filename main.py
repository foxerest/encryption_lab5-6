import random


def generate_table(alphabet, m, n):
    table = [[0 for _ in range(n)] for _ in range(m)]
    for letter in alphabet:
        while True:
            random_i = random.randint(0, m - 1)
            random_j = random.randint(0, n - 1)
            if table[random_i][random_j] == 0:
                table[random_i][random_j] = letter
                break
    return table


def encrypt(text, table):
    length_is_even = True
    len_text = len(text)
    encrypted_text = ""
    if len_text % 2 != 0:
        len_text -= 1
        length_is_even = False
    for i in range(0, len_text-1, 2):
        first_letter = text[i]
        second_letter = text[i+1]
        first_letter_i, first_letter_j, second_letter_i, second_letter_j = [None] * 4
        for row_index in range(len(table)):
            row = table[row_index]
            if first_letter in row:
                first_letter_i = row_index
                first_letter_j = row.index(first_letter)
            if second_letter in row:
                second_letter_i = row_index
                second_letter_j = row.index(second_letter)
        if ((first_letter_i is None) or (first_letter_j is None) or
                (second_letter_i is None) or (second_letter_j is None)):
            return encrypted_text, False
        if (first_letter_i == second_letter_i) or (first_letter == second_letter):
            if first_letter_j == len(table[0]) - 1:
                first_letter_j = 0
            else:
                first_letter_j += 1
            if second_letter_j == len(table[0]) - 1:
                second_letter_j = 0
            else:
                second_letter_j += 1
        elif first_letter_j == second_letter_j:
            if first_letter_i == len(table) - 1:
                first_letter_i = 0
            else:
                first_letter_i += 1
            if second_letter_i == len(table) - 1:
                second_letter_i = 0
            else:
                second_letter_i += 1
        else:
            first_letter_i, second_letter_i = second_letter_i, first_letter_i
        encrypted_text += table[first_letter_i][first_letter_j] + table[second_letter_i][second_letter_j]
    if length_is_even is False:
        encrypted_text += text[len_text]
    return encrypted_text, True


def decrypt(text, table):
    length_is_even = True
    len_text = len(text)
    decrypted_text = ""
    if len_text % 2 != 0:
        len_text -= 1
        length_is_even = False
    for i in range(0, len_text - 1, 2):
        first_letter = text[i]
        second_letter = text[i + 1]
        first_letter_i, first_letter_j, second_letter_i, second_letter_j = [None] * 4
        for row_index in range(len(table)):
            row = table[row_index]
            if first_letter in row:
                first_letter_i = row_index
                first_letter_j = row.index(first_letter)
            if second_letter in row:
                second_letter_i = row_index
                second_letter_j = row.index(second_letter)
        if ((first_letter_i is None) or (first_letter_j is None) or
                (second_letter_i is None) or (second_letter_j is None)):
            return decrypted_text, False
        if (first_letter_i == second_letter_i) or (first_letter == second_letter):
            if first_letter_j == 0:
                first_letter_j = len(table[0]) - 1
            else:
                first_letter_j -= 1
            if second_letter_j == 0:
                second_letter_j = len(table[0]) - 1
            else:
                second_letter_j -= 1
        elif first_letter_j == second_letter_j:
            if first_letter_i == 0:
                first_letter_i = len(table) - 1
            else:
                first_letter_i -= 1
            if second_letter_i == 0:
                second_letter_i = len(table) - 1
            else:
                second_letter_i -= 1
        else:
            first_letter_i, second_letter_i = second_letter_i, first_letter_i
        decrypted_text += table[first_letter_i][first_letter_j] + table[second_letter_i][second_letter_j]
    if length_is_even is False:
        decrypted_text += text[len_text]
    return decrypted_text, True


def read_input_file(file_name):
    result = ""
    with open(file_name, "r", encoding="utf-8") as f:
        while True:
            line = f.readline()
            if not line:
                break
            result += line
    return result


def write_output_file(file_name, text):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(text)
    f.close()


def main():
    encrypted_file_name = "encrypted_text.txt"
    decrypted_file_name = "decrypted_text.txt"
    uk_alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
    table = generate_table(uk_alphabet, 3, 11)

    original_text = input("Введіть текст, який будемо шифрувати: ").lower().strip()
    encrypted_text, encryption_success = encrypt(original_text, table)

    print("\nКлюч-таблиця для реалізації шифру Плейфера:")
    for row in table:
        for letter in row:
            print(letter, end=" ")
        print("")

    print("\nОригінальний текст:", original_text)
    if encryption_success:
        write_output_file(encrypted_file_name, encrypted_text)
        print("Зашифрований текст:", encrypted_text)

        decrypted_text, decryption_success = decrypt(encrypted_text, table)

        if decryption_success:
            write_output_file(decrypted_file_name, decrypted_text)
            print("Дешифрований текст:", decrypted_text)
        else:
            print("Дешифрування неможливе.\nЗашифрований текст містить не тільки літери українського алфавіту")
    else:
        print("Допускається ввід лише літер українського алфавіту")


if __name__ == "__main__":
    main()