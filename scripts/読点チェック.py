#!/usr/bin/env python3
"""本文ファイルの読点数と、読点が三つ以上ある文を表示する。

使い方: python3 scripts/読点チェック.py 本文/第1章_サンプル.md [最大表示数]
地の文、台詞(「」『』)、内心(（）)に分けて数える。
台詞と内心の息の読点は残してよい作品が多いので、判定はプロジェクトの
文体ガイドに合わせて行うこと。このスクリプトは数えるだけである。
"""
import sys


def kind(line):
    s = line.strip()
    if s.startswith("「") or s.startswith("『"):
        return "台詞"
    if s.startswith("（"):
        return "内心"
    return "地の文"


def sentences(line):
    # 句点、感嘆符、疑問符の後ろで文を区切る(括弧内は区切らない)
    out, buf, depth = [], "", 0
    for ch in line:
        buf += ch
        if ch in "「『（":
            depth += 1
        elif ch in "」』）":
            depth = max(0, depth - 1)
        if depth == 0 and ch in "。！？":
            out.append(buf)
            buf = ""
    if buf.strip():
        out.append(buf)
    return out


def main():
    path = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    total = 0
    over = {"地の文": [], "台詞": [], "内心": []}
    counts = {"地の文": 0, "台詞": 0, "内心": 0}
    for no, line in enumerate(open(path, encoding="utf-8"), 1):
        line = line.rstrip("\n")
        if not line.strip() or no == 1:
            continue
        k = kind(line)
        for s in sentences(line):
            n = s.count("、")
            total += n
            counts[k] += n
            if n >= 3:
                over[k].append((no, n, s.strip()))
    print(f"{path}: 読点 {total} (地の文 {counts['地の文']} / 台詞 {counts['台詞']} / 内心 {counts['内心']})")
    for k in ("地の文", "台詞", "内心"):
        print(f"読点が三つ以上の{k}: {len(over[k])} 文")
    shown = 0
    for k in ("地の文", "台詞", "内心"):
        for no, n, s in over[k]:
            if shown >= limit:
                break
            print(f"  [{k}] {no}行 読点{n}: {s[:80]}")
            shown += 1


if __name__ == "__main__":
    main()
