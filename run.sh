trap "exit" INT TERM ERR
trap "kill 0" EXIT

./build/bin/fc &
./build/bin/sim &

wait