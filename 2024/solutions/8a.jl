
function load(file)
    stack(eachline(file); dims=1)
end

inbounds(d, loc) = (1 ≤ loc[1] ≤ size(d)[1]) && (1 ≤ loc[2] ≤ size(d)[2])
##################################

d = load("data/8.txt")

nodes = Set()
for c in unique(d)
    c == '.' && continue
    ixs = findall(==(c), d)
    for (p, q) in Iterators.product(ixs, ixs)
        p == q && continue
        inbounds(d, p + (p - q)) && push!(nodes, p + (p - q))
    end
end

for p in nodes
    d[p] = '#'
end


print(length(nodes))