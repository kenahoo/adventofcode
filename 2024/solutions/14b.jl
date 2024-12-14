function load(file)
    stack(map(assemble, eachmatch(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"s, read(file, String))), dims=1)
end

function assemble(m::RegexMatch)
    parse.(Int, m.captures)
end

function go(d, n, dims)
    d2 = d[:, 1:2] + n .* d[:, 3:4]
    [mod.(d2[:, 1], dims[1]) mod.(d2[:, 2], dims[2])]
end

function count(d, dims)
    a = d[:, 1] .- dims[1] ÷ 2
    b = d[:, 2] .- dims[2] ÷ 2
    sum(a .> 0 .&& b .> 0) * sum(a .< 0 .&& b .> 0) * sum(a .> 0 .&& b .< 0) * sum(a .< 0 .&& b .< 0)
end

function look(d2, dims)
    M = fill('.', dims)
    for (i, j) in eachrow(d2)
        M[i+1, j+1] = '#'
    end
    print(join([join(r, "") for r in eachcol(M)], "\n"))
end

##################################

d = load("data/14.txt")
dims = (101, 103)

# Looked at the output, started noticing vertical & horizontal stripes:
# 7v, 53h, 108v, 156h, 209v, 259h, 310v, 362h, ...
#
# Those have a difference of v:101, h:103.
# Patterns would align when:
#  7 + 101x = 53 + 103y
#  101x = 53 - 7 + 103y
#  101x == 46 mod 103
#  (look up inverse of 101 mod 103 - it's 51)
#  x = 51*46 mod 103
#  x = 80
#  7 + 101*80 = 8087

for i in (8087-4):(8087+4)
    println(i)
    d2 = go(d, i, dims)
    look(d2, dims)
end

# I'll be damned, there's a tree
