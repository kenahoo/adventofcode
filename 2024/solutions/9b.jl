using StatsBase

function load(file)
    [parse(Int, x) for x in readline(file)]
end

function to_map(x)
    s = []
    for i in 1:(length(x)÷2)
        push!(s, (i - 1, x[2i-1]), (-1, x[2i]))
    end
    push!(s, (length(x) ÷ 2, x[end]))
end

function go(x, i)
    # Lots of inefficiencies & waste in here
    ipos = findfirst(a -> a[1] == i, x)
    pos = findfirst(a -> a[1] === -1 && a[2] >= x[ipos][2], x)
    pos === nothing && return
    pos >= ipos && return

    margin = x[pos][2] - x[ipos][2]
    x[pos] = x[ipos]
    x[ipos] = (-1, x[ipos][2])
    if margin > 0
        insert!(x, pos + 1, (-1, margin))
    end
end

unzip(a) = map(x -> getfield.(a, x), [1, 2])
checksum(x) = sum(x .* (eachindex(x) .- 1))
function checksum2(x)
    y = inverse_rle(unzip(x)...)
    y[y.==-1] .= 0
    checksum(y)
end
##################################

d = load("data/9.txt")
v = to_map(d)

i = v[end][1]
while i > 0
    go(v, i)
    i -= 1
end

print(checksum2(v))