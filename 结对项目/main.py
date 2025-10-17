#!/usr/bin/env python3
"""
主程序：命令行接口，支持生成题目和批改答案。
"""
import argparse
import sys
import os
from generator import Generator
from utils import parse_exercises_file, parse_answers_file, grade


def main(argv=None):
    parser = argparse.ArgumentParser(description='四则运算题目生成与判分')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-n', type=int, help='生成题目数量')
    group.add_argument('-e', type=str, help='指定题目文件以进行判分')
    parser.add_argument('-r', type=int, help='数值范围(必须在生成模式下指定)', default=None)
    parser.add_argument('-a', type=str, help='答案文件(用于判分模式)')
    parser.add_argument('--out-dir', '-o', dest='out_dir', help='输出目录（默认当前目录）')

    args = parser.parse_args(argv)

    out_dir = args.out_dir or os.getcwd()
    os.makedirs(out_dir, exist_ok=True)

    if args.n is not None:
        # 生成模式
        if args.r is None:
            parser.error('生成模式 (-n) 必须同时指定 -r 参数')
        if args.n < 1 or args.n > 10000:
            parser.error('-n 必须在 1..10000 之间')
        g = Generator(max_value=args.r)
        exercises, answers = g.generate(args.n)
        ex_path = os.path.join(out_dir, 'Exercises.txt')
        ans_path = os.path.join(out_dir, 'Answers.txt')
        with open(ex_path, 'w', encoding='utf-8') as f:
            for e in exercises:
                f.write(e + '\n')
        with open(ans_path, 'w', encoding='utf-8') as f:
            for a in answers:
                f.write(a + '\n')
        print(f'已生成 {len(exercises)} 道题目: {ex_path}, {ans_path}')
        return

    # 判分模式
    if args.e:
        if not args.a:
            parser.error('判分模式需要同时指定 -a <answerfile>')
        exercises = parse_exercises_file(args.e)
        user_answers = parse_answers_file(args.a)
        correct, wrong = grade(exercises, user_answers)
        grade_path = os.path.join(out_dir, 'Grade.txt')
        with open(grade_path, 'w', encoding='utf-8') as f:
            f.write(f'Correct: {len(correct)} ')
            f.write('(' + ', '.join(str(i) for i in correct) + ')\n\n')
            f.write(f'Wrong: {len(wrong)} ')
            f.write('(' + ', '.join(str(i) for i in wrong) + ')\n')
        print(f'已输出 {grade_path}')



if __name__ == '__main__':
    main()
