function load(file)
    parse.(Int, stack(eachline(file); dims=1))
end

dirs = CartesianIndex.([(1, 0), (0, 1), (-1, 0), (0, -1)])

function combine(d, pos)
    reduce(∪, d[filter(inbounds(d), pos .+ dirs)])
end

inbounds(d, loc) = all(i -> 1 ≤ loc[i] ≤ size(d)[i], 1:ndims(d))
inbounds(d) = loc -> inbounds(d, loc)
##################################

d = load("data/10.txt")

locs = [Set(d[x] == 9 ? (x,) : []) for x in CartesianIndices(d)]
for i in 8:-1:0
    prev = locs
    locs = [d[x] == i ? combine(prev, x) : Set() for x in CartesianIndices(d)]
end

println(sum(length.(locs)))
