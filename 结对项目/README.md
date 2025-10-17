# 四则运算题目生成与判分程序

用法示例：

生成题目：

    python main.py -n 10 -r 10

批改题目：

    python main.py -e Exercises.txt -a Answers_user.txt

输出文件：`Exercises.txt`, `Answers.txt`, `Grade.txt`

说明与注意：

文件位置：程序会把 `Exercises.txt` / `Answers.txt` 写到当前工作目录（即运行时的目录），如果你希望固定输出到 `结对项目` 目录请告知我，我会添加 `--out-dir` 参数支持。
 
 输出目录：新增 `--out-dir` 或 `-o` 参数可以指定输出目录，例如：
 
      python main.py -n 20 -r 20 -o e:/tobysieam/结对项目/out_test
 
 规模：程序支持一次生成最多 10000 道题（受机器性能限制），可用 `perf_test.py` 进行性能基线测试。
