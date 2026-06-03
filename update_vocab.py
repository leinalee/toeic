#!/usr/bin/env python3
"""
TOEIC 단어 매일 자동 업데이트 스크립트

매일 실행하면 wordbank_master.json에서 아직 추가되지 않은 단어 10개를
vocabulary.json에 자동으로 추가합니다.

사용법:
  python3 update_vocab.py          # 기본 10개 추가
  python3 update_vocab.py --count 5  # 5개 추가
  python3 update_vocab.py --status   # 현재 상태 확인
"""

import json
import os
import sys
import random
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VOCAB_FILE = os.path.join(SCRIPT_DIR, "data", "vocabulary.json")
MASTER_FILE = os.path.join(SCRIPT_DIR, "data", "wordbank_master.json")
LOG_FILE = os.path.join(SCRIPT_DIR, "data", "update_log.json")

DEFAULT_COUNT = 10


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_log():
    if os.path.exists(LOG_FILE):
        return load_json(LOG_FILE)
    return {"updates": []}


def save_log(log):
    save_json(LOG_FILE, log)


def get_status():
    vocab = load_json(VOCAB_FILE)
    master = load_json(MASTER_FILE)

    vocab_ids = {q["id"] for q in vocab["questions"]}
    master_ids = {q["id"] for q in master["questions"]}
    remaining = master_ids - vocab_ids

    print(f"📖 현재 단어장: {len(vocab['questions'])}개")
    print(f"📦 마스터 단어은행: {len(master['questions'])}개")
    print(f"✅ 이미 추가된 단어: {len(master_ids & vocab_ids)}개")
    print(f"⏳ 남은 새 단어: {len(remaining)}개")

    if remaining:
        days_left = len(remaining) // DEFAULT_COUNT
        print(f"📅 하루 {DEFAULT_COUNT}개씩 약 {days_left}일 분량")
    else:
        print("⚠️  마스터 단어은행의 모든 단어가 추가되었습니다.")

    log = load_log()
    if log["updates"]:
        last = log["updates"][-1]
        print(f"\n🕐 마지막 업데이트: {last['date']} ({last['count']}개 추가)")


def update_vocab(count=DEFAULT_COUNT):
    vocab = load_json(VOCAB_FILE)
    master = load_json(MASTER_FILE)

    vocab_ids = {q["id"] for q in vocab["questions"]}
    new_words = [q for q in master["questions"] if q["id"] not in vocab_ids]

    if not new_words:
        print("⚠️  추가할 새 단어가 없습니다. 마스터 단어은행을 보충해 주세요.")
        return 0

    # 랜덤으로 선택 (다양한 난이도/유형 섞이도록)
    random.shuffle(new_words)
    to_add = new_words[:count]

    vocab["questions"].extend(to_add)
    save_json(VOCAB_FILE, vocab)

    # 로그 기록
    log = load_log()
    added_words = [w["english"] for w in to_add]
    log["updates"].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "count": len(to_add),
        "words": added_words
    })
    save_log(log)

    print(f"✅ {len(to_add)}개 새 단어가 추가되었습니다!")
    print(f"📖 전체 단어장: {len(vocab['questions'])}개")
    print()
    print("추가된 단어:")
    for w in to_add:
        print(f"  • {w['english']} — {w['korean']} ({w['partOfSpeech']})")

    remaining = len(new_words) - len(to_add)
    print(f"\n⏳ 남은 새 단어: {remaining}개")

    return len(to_add)


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--status" in args:
        get_status()
    elif "--count" in args:
        idx = args.index("--count")
        if idx + 1 < len(args):
            count = int(args[idx + 1])
        else:
            count = DEFAULT_COUNT
        update_vocab(count)
    else:
        update_vocab()
