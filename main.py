import random
import string
import time
import numpy as np
import matplotlib.pyplot as plt


def naive_string_matcher(text, pattern):
    len_pattern = len(pattern)
    len_text = len(text)
    result = [0] * len_text
    # всевозможные позиции начала нашей рамки
    for i in range(0, len_text - len_pattern + 1):
        s = 0
        # сравнение подстроки, которую ищем и текста внутри рамки со смещением i
        while s < len_pattern and text[i + s] == pattern[s]:
            s += 1
        # полное совпадение, значит, внутри рассматриваемой рамки оказался искомый паттерн
        if s == len_pattern:
            result[i + len_pattern - 1] = len_pattern
        else:
            result[i + len_pattern - 1] = 0
    return result


def KMP(pattern):
    # всегда 0
    pattern_length = len(pattern)
    result = [0] * pattern_length
    # инициалиация счетчиков
    i = 1
    j = 0
    # пока не закончился паттерн
    while i < pattern_length:
        # если совпало, значит, нашли совпадающий суффикс и префикс, увеличиваем счетчики и записываем полученное значение
        # в функцию-откатов
        if pattern[i] == pattern[j]:
            result[i] = j + 1
            i += 1
            j += 1
        # совпадения не было, при этом, до этого совпадений так же не было, так как j = 0
        elif j == 0:
            result[i] = 0
            i += 1
        # здесь мы добавили очередной элемент в префикс и суффикс и получилось так, что они не совпали. Нам не подошел префикс
        # Значит, надо взять
        # префикс и суффикс поменьше, но которые так же совпадают. А информация о таком хранится как раз в массиве,
        # который мы заполняем
        else:
            j = result[j - 1] # берем длину меньшего префикс-суффикса
    return result


def SFT_KMP(text, pattern):
    i = 0 # индекс по тексту
    l = 0 # индекс внутри шаблона
    len_text = len(text)
    len_pattern = len(pattern)
    f_pattern = KMP(pattern)
    result = [0] * len_text
    while i < len_text:
        if text[i] == pattern[l]:
            i += 1
            l += 1
            # нашли в тексте шаблон
            if l == len_pattern:
                result[i-1] = len_pattern
                l = 0
        # дошли до момента, когда нужно начать проверять шаблон с самого начала
        elif l == 0:
            i += 1
        else:
            # у нас не совпал символ, но вместо того, чтобы начать все с нуля проверять всю рамку
            # мы можем начать проверять с более выгодной позиции и быть уверенными,  что ничего не потеряли
            l = f_pattern[l - 1]
    return result


def gen_normal_word(len_word, valid_letters):
    result = ''
    for i in range(len_word):
        result += valid_letters[random.randint(0, len(valid_letters) - 1)]
    return result


def gen_repeated(k, word):
    result = ''
    for i in range(k):
        result += word
    return result


def first_experiment():
    k_array = np.array(list(range(1, 1001, 10)))
    T1_array = np.empty(100)
    T2_array = np.empty(100)
    i = 0
    for k in range(1, 1001, 10):
        print(k)
        text = 'ab' * 1000 * k
        pattern = 'ab' * k
        start_time = time.time()
        #naive_string_matcher(text, pattern)
        end_time = time.time()
        T1_array[i] = end_time - start_time
        start_time = time.time()
        SFT_KMP(text, pattern)
        end_time = time.time()
        T2_array[i] = end_time - start_time
        i += 1
    plt.plot(k_array, T1_array, label=r'$T_1(k) - Наивный$')
    plt.plot(k_array, T2_array, label=r'$T_2(k) - KMP$')
    plt.xlabel(r'$k$', fontsize=14)
    plt.ylabel(r'$T(k)$', fontsize=14)
    plt.legend(loc='best', fontsize=12)
    plt.show()


def second_experiment():
    m_array = np.array(list(range(1, 10**6, 10**4)))
    T1_array = np.array(list(range(1, 10**6, 10**4)))
    T2_array = np.array(list(range(1, 10**6, 10**4)))
    alphabet = 'ab'
    pattern = 'a'
    i = 0
    text = gen_normal_word(10 ** 6 + 1, alphabet)
    for m in range(1, 10**6, 10**4):
        pattern = 'a' * m
        start_time = time.time()
        #naive_string_matcher(text, pattern)
        end_time = time.time()
        T1_array[i] = end_time - start_time
        start_time = time.time()
        SFT_KMP(text, pattern)
        end_time = time.time()
        T2_array[i] = end_time - start_time
        i += 1
    plt.plot(m_array, T1_array, label=r'$T_1(k) - Наивный$')
    plt.plot(m_array, T2_array, label=r'$T_2(k) - KMP$')
    plt.xlabel(r'$k$', fontsize=14)
    plt.ylabel(r'$T(k)$', fontsize=14)
    plt.legend(loc='best', fontsize=12)
    plt.show()


def third_experiment():
    pattern = 'aaaaa'
    h_array = np.array(list(range(1, 10**6 + 1, 10**4)))
    T1_array = np.array(list(range(1, 10**6 + 1, 10**4)))
    T2_array = np.array(list(range(1, 10**6 + 1, 10**4)))
    i = 0
    for h in range(1,10**6 + 1, 10**4):
        print(h)
        text = 'aaaaab' * h
        start_time = time.time()
        naive_string_matcher(text, pattern)
        end_time = time.time()
        T1_array[i] = end_time - start_time
        start_time = time.time()
        SFT_KMP(text, pattern)
        end_time = time.time()
        T2_array[i] = end_time - start_time
        i += 1
    plt.plot(h_array, T1_array, label=r'$T_1(k) - Наивный$')
    plt.plot(h_array, T2_array, label=r'$T_2(k) - KMP$')
    plt.xlabel(r'$k$', fontsize=14)
    plt.ylabel(r'$T(k)$', fontsize=14)
    plt.legend(loc='best', fontsize=12)
    plt.show()


def print_main_menu():
    print('Главное меню')
    print('1) Задать размер алфавита и сам алфавит')
    print('2) Задать текст')
    print('3) Задать шаблон для поиска')
    print('4) Сгенерировать текст с помощью')
    print('5) Сгенерировать шаблон')
    print('6) Сгенерировать повторяющийся текст')
    print('7) Сгенерировать повторяющийся шаблон')
    print('8) Исполнить алгоритм для заданных слов')
    print('9) Вывести текст и шаблон поиска')
    print('0) Выход')


def main():
    T1 = 0
    T2 = 0
    count_letters = 0
    alphabet = string.ascii_lowercase
    text = ''
    pattern = ''
    print_main_menu()

    while False:
        choice = int(input('Ваш выбор:'))
        if choice == 1:
            count_letters = int(input('Введите число букв в алфавите: '))
            alphabet = input('Введите символы алфавита: ')
        elif choice == 2:
            text = input('Введите текст: ')
            print('Текст {} успешно сформирован'.format(text))
        elif choice == 3:
            pattern = input('Введите шаблон: ')
            print('Шаблон {} успешно сформирован'.format(pattern))
        elif choice == 4:
            len_word = int(input('Введите длину слова'))
            valid_letters = input('Введите допустимые буквы алфавита: ')
            text = gen_normal_word(len_word, valid_letters)
            print('Текст успешно сгенерирован')
        elif choice == 5:
            len_word = int(input('Введите длину шаблона'))
            valid_letters = input('Введите допустимые буквы алфавита: ')
            pattern = gen_normal_word(len_word, valid_letters)
            print('Шаблон успешно сгенерирован')
        elif choice == 6:
            word = input('Введите слово')
            k = int(input('Введите число повторений слова {} '.format(word)))
            text = gen_repeated(k, word)
            print('Повторяющийся текст успешно сгенерирован')
        elif choice == 7:
            word = input('Введите шаблон для поиска')
            k = int(input('Введите число повторений шаблона {} '.format(word)))
            pattern = gen_repeated(k, word)
            print('Повторяющийся шаблон успешно сгенерирован')
        elif choice == 8:
            start_time = time.time()
            naive_string_matcher(text, pattern)
            end_time = time.time()
            T1 = end_time - start_time
            print('Время работы наивного {}'.format(T1))
            start_time = time.time()
            SFT_KMP(text, pattern)
            end_time = time.time()
            T2 = end_time - start_time
            print('Время работы Кнута-Морриса-Пратта {}'.format(T2))
        elif choice == 9:
            print('Текст: ' + text)
            print('Шаблон: ' + pattern)
        elif choice == 0:
            print('К эспериментам')
            break
        else:
            print('Нет такой команды')

    third_experiment()

if __name__ == '__main__':
    main()