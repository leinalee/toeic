#!/bin/bash
PORT=8000
DIR="$(cd "$(dirname "$0")" && pwd)"
PIDFILE="$DIR/.server.pid"

case "$1" in
  start)
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
      echo "이미 실행 중입니다 (PID: $(cat "$PIDFILE"))"
      echo "http://localhost:$PORT"
      exit 0
    fi
    cd "$DIR"
    nohup python3 server.py > "$DIR/data/server.log" 2>&1 &
    echo $! > "$PIDFILE"
    sleep 1
    if kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
      IP=$(hostname -I 2>/dev/null | awk '{print $1}')
      echo "TOEIC 900 서버 시작! (PID: $(cat "$PIDFILE"))"
      echo "  PC:     http://localhost:$PORT"
      [ -n "$IP" ] && echo "  iPad:   http://$IP:$PORT"
    else
      echo "서버 시작 실패. 로그 확인: $DIR/data/server.log"
      rm -f "$PIDFILE"
      exit 1
    fi
    ;;
  stop)
    if [ -f "$PIDFILE" ]; then
      kill "$(cat "$PIDFILE")" 2>/dev/null
      rm -f "$PIDFILE"
      echo "서버 종료됨"
    else
      echo "실행 중인 서버가 없습니다"
    fi
    ;;
  restart)
    "$0" stop
    sleep 1
    "$0" start
    ;;
  status)
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
      echo "실행 중 (PID: $(cat "$PIDFILE"))"
      echo "http://localhost:$PORT"
    else
      echo "중지됨"
      rm -f "$PIDFILE" 2>/dev/null
    fi
    ;;
  *)
    echo "사용법: ./dev.sh {start|stop|restart|status}"
    exit 1
    ;;
esac
