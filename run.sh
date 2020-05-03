python preschedule.py
mv data/*.txt SchedJulia/data/
cd SchedJulia
julia schedjulia.jl
cp data/*.txt ../data/
git reset --hard
