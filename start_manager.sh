#!/usr/bin/env bash

set -euo pipefail
sudo truncate -s 0 /var/log/veloma/*.log 2>/dev/null || true
# =========================
# CONFIGURAÇÃO
# =========================

APP_DIR="/opt/veloma-app"
VENV_DIR="$APP_DIR/venv"

LOG_DIR="/var/log/veloma"

DJANGO_PORT=7000
DJANGO_BIND="0.0.0.0:$DJANGO_PORT"

REDIS_HOST="127.0.0.1"
REDIS_PORT="6380"

export DJANGO_SETTINGS_MODULE="core.settings"
export PATH="$VENV_DIR/bin:$PATH"

# =========================
# LOG FILES
# =========================

MANAGER_LOG="$LOG_DIR/manager.log"
DJANGO_LOG="$LOG_DIR/django.log"
CELERY_WORKER_LOG="$LOG_DIR/celery_worker.log"
CELERY_BEAT_LOG="$LOG_DIR/celery_beat.log"
ERROR_LOG="$LOG_DIR/error.log"
AUTH_LOG="$LOG_DIR/auth.log"

# =========================
# PROCESS PATTERNS
# =========================

DJANGO_PATTERN="manage.py runserver 0.0.0.0:$DJANGO_PORT"
CELERY_WORKER_PATTERN="celery -A core.celery worker"
CELERY_BEAT_PATTERN="celery -A core.celery beat"

# =========================
# COLORS
# =========================

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# =========================
# LOG FUNCTIONS
# =========================

log(){ echo -e "[$(date '+%F %T')] $*" | tee -a "$MANAGER_LOG"; }
ok(){ echo -e "${GREEN}$*${NC}" | tee -a "$MANAGER_LOG"; }
warn(){ echo -e "${YELLOW}$*${NC}" | tee -a "$MANAGER_LOG"; }
err(){ echo -e "${RED}$*${NC}" | tee -a "$MANAGER_LOG"; }

# =========================
# PREPARAR LOGS
# =========================

prepare_logs(){

    mkdir -p "$LOG_DIR"

    touch \
    "$MANAGER_LOG" \
    "$DJANGO_LOG" \
    "$CELERY_WORKER_LOG" \
    "$CELERY_BEAT_LOG" \
    "$ERROR_LOG" \
    "$AUTH_LOG"

    chmod 664 "$LOG_DIR"/*.log

}

# =========================
# ATIVAR VENV
# =========================

activate_venv(){

    if [[ ! -f "$VENV_DIR/bin/activate" ]]; then
        err "Virtualenv não encontrado em $VENV_DIR"
        exit 1
    fi

    source "$VENV_DIR/bin/activate"

}

# =========================
# CHECK REDIS
# =========================

check_redis(){

    if command -v redis-cli >/dev/null 2>&1; then

        if redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" ping | grep -q PONG; then
            ok "Redis OK"
        else
            warn "Redis não respondeu"
        fi

    else

        warn "redis-cli não instalado"

    fi

}

# =========================
# PROCESS HELPERS
# =========================

running(){
    pgrep -f "$1" >/dev/null 2>&1
}

stop_pattern(){

    local pattern="$1"
    local name="$2"

    if running "$pattern"; then

        log "Parando $name"

        pkill -f "$pattern"

        sleep 2

    else

        log "$name já estava parado"

    fi

}

# =========================
# START DJANGO
# =========================

start_django(){

    if running "$DJANGO_PATTERN"; then
        warn "Django já está rodando"
        return
    fi

    log "Iniciando Django..."

    nohup python manage.py runserver "$DJANGO_BIND" >> "$DJANGO_LOG" 2>&1 &

    sleep 2

    running "$DJANGO_PATTERN" && ok "Django iniciado"

}

# =========================
# START CELERY WORKER
# =========================

start_worker(){

    if running "$CELERY_WORKER_PATTERN"; then
        warn "Celery Worker já está rodando"
        return
    fi

    log "Iniciando Celery Worker..."

    celery -A core.celery worker \
    -Q emails,celery \
    --loglevel=INFO \
    --logfile="$CELERY_WORKER_LOG" \
    --detach \
    --concurrency=2 \
    --prefetch-multiplier=4

    sleep 2

    running "$CELERY_WORKER_PATTERN" && ok "Celery Worker iniciado"

}

# =========================
# START CELERY BEAT
# =========================

start_beat(){

    if running "$CELERY_BEAT_PATTERN"; then
        warn "Celery Beat já está rodando"
        return
    fi

    log "Iniciando Celery Beat..."

    celery -A core.celery beat \
    --loglevel=INFO \
    --logfile="$CELERY_BEAT_LOG" \
    --detach

    sleep 2

    running "$CELERY_BEAT_PATTERN" && ok "Celery Beat iniciado"

}

# =========================
# START
# =========================

start(){

    cd "$APP_DIR"

    prepare_logs
    activate_venv
    check_redis

    start_django
    start_worker
    start_beat

}

# =========================
# STOP
# =========================

stop(){

    stop_pattern "$DJANGO_PATTERN" "Django"
    stop_pattern "$CELERY_WORKER_PATTERN" "Celery Worker"
    stop_pattern "$CELERY_BEAT_PATTERN" "Celery Beat"

}

# =========================
# STATUS
# =========================

status(){

    echo "-----------------------------------"

    running "$DJANGO_PATTERN" && ok "Django: rodando" || err "Django: parado"

    running "$CELERY_WORKER_PATTERN" && ok "Worker: rodando" || err "Worker: parado"

    running "$CELERY_BEAT_PATTERN" && ok "Beat: rodando" || err "Beat: parado"

    echo "-----------------------------------"

}

# =========================
# RESTART
# =========================

restart(){

    stop
    sleep 2
    start

}

# =========================
# MAIN
# =========================

case "${1:-}" in

start)
    start
    ;;

stop)
    stop
    ;;

restart)
    restart
    ;;

status)
    status
    ;;

*)
    echo "Uso: $0 {start|stop|restart|status}"
    exit 1
    ;;

esac