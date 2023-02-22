a = [[]]
s1 = []
s2 = []


# מחזירה את קירוב השינויים בין שתי המחרוזות
def EditDistance(check, correct):
    s1 = check
    s2 = correct
    # הגדרת גודל המטריצה + 1 כדי שיוכל להתחיל ממספר 1 והמיקום 0 ישאר מאופס
    a = [[0 for x in range(len(check) + 1)] for y in range(len(correct) + 1)]

    # יצירת המטריצה והכנסת קירוב השינויים
    # אתחול עמודה ושורה ראשונים
    for i in range(len(s2) + 1):
        a[i][0] = i
    for j in range(len(s1) + 1):
        a[0][j] = j
    # ריצה על כל המטריצה והכנסת מרחק השינויים לפי החישוב של תכנון דינאמי
    for i in range(1, len(s2) + 1):
        for j in range(1, len(s1) + 1):
            insertion = a[i][j - 1] + 1
            deletion = a[i - 1][j] + 1
            match = a[i - 1][j - 1]
            mismatch = a[i - 1][j - 1] + 1
            if s1[j - 1] == s2[i - 1]:
                a[i][j] = min(insertion, min(deletion, match))
            else:
                a[i][j] = min(insertion, min(deletion, mismatch))
    return a, a[len(a) - 1][len(a[0]) - 1]


s_check = []
s_correct = []


# פונקציה שמחשבת דרך חזור במטריצה
# מקבלת את אורך שתי המחרוזות

def FinalResult(i, j, check, correct, a):
    s_correct.clear()
    s_check.clear()
    if i == 0 and j == 0:
        return
    if i > 0 and a[i][j] == (a[i - 1][j] + 1):
        FinalResult(i - 1, j, check, correct, a)
        s_correct.append(correct[i - 1])
        s_check.append("-")
    else:
        if j > 0 and a[i][j] == (a[i][j - 1] + 1):
            FinalResult(i, j - 1, check, correct, a)
            s_correct.append("-")
            s_check.append(check[j - 1])
        else:
            FinalResult(i - 1, j - 1, check, correct, a)
            s_correct.append(correct[i - 1])
            s_check.append(check[j - 1])
    return s_check, s_correct


def checkIfAreNotInStuckList(letter1, letter2):
    listletters = [['א', 'ל'], ['י', 'נ'], ['ש', 'נ'],['נ','כ'], ['ע', 'ל'], ['ו', 'א'], ['ב', 'ך'], ['כ', 'ת'], ['נ', 'ת']]

    for i in range(len(listletters)):
        if (letter1 == listletters[i][0] and letter2 == listletters[i][1]) or letter1 == 'ל':
            return False
    return True


# the entire function to Proofreading the mezuza
def Checkline(num_of_line, letters_for_check, correct_letters, path_to_result_file):
    result_file = open(path_to_result_file, 'a', encoding='utf-8')
    result_file.write('The Results:\n\n')
    mat, min_of_mistakes = EditDistance(letters_for_check, correct_letters)
    s_check, s_correct = FinalResult(len(correct_letters), len(letters_for_check), letters_for_check, correct_letters,
                                     mat)
    if min_of_mistakes == 0:
        return
    result_file.write(f"{num_of_line}:\n")
    for i in range(len(s_check)):
        if s_check[i] == s_correct[i]:
            continue
        if s_check[i] != s_correct[i] and s_check[i] != '-' and s_correct[i] != '-':
            if s_check[i] == 'other':
                if checkIfAreNotInStuckList(s_correct[i], s_correct[i + 1]):
                    result_file.write(
                        f"   letter {i + 1}: the letters are probably stuck together instead of {s_correct[i + 1]} {s_correct[i]} \n")
                i = i + 2
                continue
            else:
                result_file.write(
                    f"   letter {i + 1}: you wrote {s_check[i]} instead of {s_correct[i]} \n")  # את האות הלא נכונה ללא סיבה נראית לעין
        if (s_check[i] == '-' and s_check[i - 1] != 'other'):
            result_file.write(f"   letter {i + 1}: you missed out the letter {s_correct[i]} \n")
        if (s_correct[i] == '-'):
            result_file.write(f"   letter {i + 1}: you wrote the letter {s_check[i]} its spare letter \n")

    result_file.close()


def MainChecker(mezuza_name, dic):
    from Mezuza import Mezuza
    m = Mezuza()
    for line, list in dic.items():
        Checkline(line, list, m.correct_mezuza[line], fr"images/results/{mezuza_name}.txt")
    result_file = open(fr"images/results/{mezuza_name}.txt", 'a', encoding='utf-8')
    result_file.write('\n\nNot sure the letters are separated: All the letters that come after ל')
    result_file.close()
    return fr"images/results/{mezuza_name}.txt"
