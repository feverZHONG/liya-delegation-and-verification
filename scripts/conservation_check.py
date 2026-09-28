#!/usr/bin/env python3
"""搬家守恒复核：原文每一行都必须还活着（落点目录里任一 .md）。

用于「搬家 / 拆薄 / 重格式 / 多单元重切」型任务的验收：
  子代理（或自己）说「一字未丢」不算——拿**原始备份**逐行找回才算。

用法：
  python3 conservation_check.py <新落点目录> <原始备份.md> [--min 40]

判据：
  ① 备份里长度 > min 的每一行，必须**逐字**出现在落点目录下所有 .md 里（含 SKILL.md 等）；
  ② 丢失行逐条打印——0 丢失才算过；缺行就回备份把它搬进对应文件；
  ③ 顺带报体积/行数对比、落点 md 数、最大文件（大得离谱提示该再分档）。
退出码：0=0 丢失 / 1=有丢失 / 2=用法错。

注意：它只管「内容丢没丢」，不管格式——格式另外跑 mdcheck 一类体检。
"""
import glob
import os
import sys


def main():
    argv = sys.argv[1:]
    min_len = 40
    if "--min" in argv:
        i = argv.index("--min")
        min_len = int(argv[i + 1])
        del argv[i:i + 2]
    if len(argv) < 2:
        print(__doc__)
        return 2
    dest_dir, bak = argv[0].rstrip("/"), argv[1]
    orig = open(bak, encoding="utf-8").read().split("\n")
    dest_paths = sorted(glob.glob(dest_dir + "/**/*.md", recursive=True))
    dest = "".join(open(p, encoding="utf-8").read() for p in dest_paths)

    long_lines = [l for l in orig if len(l.strip()) > min_len]
    missing = [l for l in long_lines if l.strip() not in dest]
    ob = os.path.getsize(bak)
    db = sum(os.path.getsize(p) for p in dest_paths)
    biggest = max(dest_paths, key=os.path.getsize) if dest_paths else None

    print(f"原文件: {bak}  {ob/1024:.1f}KB / {len(orig)} 行")
    print(f"落点  : {dest_dir}  {len(dest_paths)} 个 md / {db/1024:.1f}KB")
    if biggest:
        print(f"  最大档: {os.path.relpath(biggest, dest_dir)} "
              f"{os.path.getsize(biggest)/1024:.1f}KB")
    print(f"原 >{min_len} 字行: {len(long_lines)}   丢失: {len(missing)}")
    for m in missing[:20]:
        print("  x " + m.strip()[:110])
    if missing:
        print("  -> 有丢失：这几行没搬到落点，回备份补进去")
        return 1
    print("  -> 0 丢失 OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
