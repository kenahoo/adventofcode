function load(file)
    [parse(Int, x) for x in readline(file)]
end

function to_map(x)
    s = Int[]
    for i in 1:(length(x)÷2)
        append!(s, repeat([i - 1], x[2i-1]), repeat([-1], x[2i]))
    end
    append!(s, repeat([length(x) ÷ 2], x[end]))
end

function go(x)
    if x[end] == -1
        pop!(x)
        return true
    end
    pos = findfirst(==(-1), x)
    pos === nothing && return false
    x[pos] = pop!(x)
    return true
end

checksum(x) = sum(x .* (eachindex(x) .- 1))
##################################

d = load("data/9.txt")
d = load("/tmp/example")
v = to_map(d)

while true
    go(v) || break
end

print(checksum(v))