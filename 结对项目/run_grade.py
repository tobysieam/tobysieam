from utils import parse_exercises_file, parse_answers_file, grade, eval_expr, normalize_answer_str, parse_fraction

ex = parse_exercises_file('e:/tobysieam/Exercises.txt')
ans = parse_answers_file('e:/tobysieam/Answers.txt')

correct, wrong = grade(ex, ans)
print('correct:', correct)
print('wrong:', wrong)
for i in wrong:
	e = ex[i-1]
	u = ans[i-1]
	real = eval_expr(e)
	real_s = normalize_answer_str(str(real.numerator)+'/'+str(real.denominator) if real.denominator!=1 else str(real.numerator))
	try:
		user_fr = parse_fraction(u)
		user_s = normalize_answer_str(str(user_fr.numerator)+'/'+str(user_fr.denominator) if user_fr.denominator!=1 else str(user_fr.numerator))
	except Exception as err:
		user_s = 'ERR:'+str(err)
	print(i, e, '=> real:', real_s, ' user:', u, ' normalized user:', user_s)
