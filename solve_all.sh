for ((i = 1 ; i < 13 ; i++)); do
    echo "Day $i:"
    python solve.py "d$i" p1
    python solve.py "d$i" p2
done
