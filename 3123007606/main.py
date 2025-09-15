import sys
from checker import calc_similarity
from utils import read_file, write_file

def main():
    if len(sys.argv) != 4:
        print("用法: python main.py [原文文件] [抄袭版论文的文件] [答案文件]")
        sys.exit(1)
    orig_path, plag_path, ans_path = sys.argv[1:4]
    try:
        orig = read_file(orig_path)
        plag = read_file(plag_path)
        similarity = calc_similarity(orig, plag)
        result = f"{similarity:.2f}"
        write_file(ans_path, result)
    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(2)

if __name__ == "__main__":
    main()
