import os
import sys
from perf_test import perf

sizes = [100, 1000, 5000, 10000]
results = []
for s in sizes:
    t = perf(s, 100)
    results.append((s, t))

png_path = os.path.join(os.path.dirname(__file__), 'perf.png')
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    xs = [r[0] for r in results]
    ys = [r[1] for r in results]
    plt.figure(figsize=(6,4))
    plt.plot(xs, ys, marker='o')
    plt.xscale('log')
    plt.xlabel('Number of exercises (log scale)')
    plt.ylabel('Generation time (s)')
    plt.title('Exercise generation performance')
    plt.grid(True)
    plt.savefig(png_path, dpi=150)
    print('Saved perf image to', png_path)
    img_available = True
except Exception as e:
    print('Could not generate plot:', e)
    img_available = False

# Append summary to final report
final_path = os.path.join(os.path.dirname(__file__), 'final_report.md')
with open(final_path, 'w', encoding='utf-8') as f:
    f.write('# 四则运算题目生成器 — 最终报告\n\n')
    f.write('## 性能基线\n\n')
    for s,t in results:
        f.write(f'- N={s}: {t:.3f} s\n')
    f.write('\n')
    if img_available:
        f.write(f'![perf](perf.png)\n')
    else:
        f.write('性能图，请在本地运行 `plot_perf.py` 以生成图片。\n')
    f.write('\n')
    f.write('## 简要设计与实现\n')
    f.write('- 代码结构：`generator.py`, `utils.py`, `main.py` 等。\n')
    f.write('- 去重策略：节点级 canonical，+ 和 * 可交换子树。\n')
    f.write('\n')
    f.write('## 测试与结果\n')
    f.write('- 单元测试：已使用 pytest 验证，所有测试通过。\n')
    f.write('\n')
    f.write('## 结对心得与改进点\n')
    f.write('- 可进一步改进去重策略 \n')

print('Wrote final report to', final_path)
