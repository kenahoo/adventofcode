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


##################################

d = load("data/14.txt")
dims = [101, 103]

d2 = go(d, 100, dims)
println(count(d2, dims))
