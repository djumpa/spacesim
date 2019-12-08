trap "exit" INT TERM ERR
trap "kill 0" EXIT

./build/bin/fc &
#./someProcessB &

wait