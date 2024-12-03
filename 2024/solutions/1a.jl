using DelimitedFiles

m = readdlm("data/1.txt", Int)

l = sort(m[:, 1])
r = sort(m[:, 2])

println(sum(abs.(l .- r)))
