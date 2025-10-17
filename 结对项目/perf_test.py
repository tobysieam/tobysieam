import time
from generator import Generator

def perf(n=1000, r=100):
    g = Generator(max_value=r)
    t0 = time.time()
    ex, ans = g.generate(n)
    t1 = time.time()
    elapsed = t1 - t0
    print(f'Generated {len(ex)} exercises in {elapsed:.3f} seconds')
    # append to report
    with open('report.md', 'a', encoding='utf-8') as f:
        f.write(f"\nPerf: Generated {len(ex)} in {elapsed:.3f}s\n")
    return elapsed

if __name__ == '__main__':
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    r = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    perf(n, r)
