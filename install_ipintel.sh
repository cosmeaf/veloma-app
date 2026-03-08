# install_ipintel.sh

set -e

BASE_DIR="/opt/ipintel"

mkdir -p $BASE_DIR
mkdir -p $BASE_DIR/engine
mkdir -p $BASE_DIR/cache
mkdir -p $BASE_DIR/stats
mkdir -p $BASE_DIR/logs
mkdir -p $BASE_DIR/update
mkdir -p $BASE_DIR/geoip
mkdir -p $BASE_DIR/tor
mkdir -p $BASE_DIR/proxy
mkdir -p $BASE_DIR/datacenter

touch $BASE_DIR/cache/ip_cache.json
touch $BASE_DIR/stats/counters.json
touch $BASE_DIR/logs/ipintel.log

chmod -R 755 $BASE_DIR

echo "IPINTEL base structure created"
