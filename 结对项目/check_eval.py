from utils import parse_exercises_file, parse_answers_file, eval_expr, normalize_answer_str

ex = parse_exercises_file('e:/tobysieam/Exercises.txt')
ans = parse_answers_file('e:/tobysieam/Answers.txt')

for i,(e,a) in enumerate(zip(ex,ans),start=1):
    try:
        val = eval_expr(e)
        real = normalize_answer_str(str(val.numerator)+'/'+str(val.denominator) if val.denominator!=1 else str(val.numerator))
    except Exception as err:
        real = 'ERR:'+str(err)
    status = 'OK' if real == a else 'MISMATCH'
    print(f'{i}. {e} => computed: {real}  expected: {a}   {status}')
