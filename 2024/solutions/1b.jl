using DelimitedFiles
using StatsBase

m = readdlm("data/1.txt", Int)

counts = countmap(m[:, 2])
s = sum(i * get(counts, i, 0) for i in m[:, 1])

println(s)
