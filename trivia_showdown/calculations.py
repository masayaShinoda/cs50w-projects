def calculate_total_score(correct_answers_count, incorrect_answers_count):
    correct_incorrect_ratio = round((correct_answers_count / incorrect_answers_count), 2)
    multiplier = 1000
    return int(correct_incorrect_ratio * multiplier)