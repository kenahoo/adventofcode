
function load(file)
    # 27905293: 1 3 67 91 5 5 293
    out = []
    for l in eachline(file)
        m = match(r"(\d+): ([\d ]+)", l)
        push!(out, [parse(Int, m.captures[1]), Tuple(parse.(Int, split(m.captures[2])))])
    end
    out
end

d = load("data/7.txt")
d = load("/tmp/example")

ok(x::Int, y::NTuple{1}) = begin
    x == y[1]
end
function ok(x::Int, y::NTuple)
    # println("Checking $x, $y")
    z = y[end]
    y′ = y[1:(end-1)]
    (x - z > 0 && ok(x - z, y′)) || (x % z == 0 && ok(x ÷ z, y′))
end
ok(x::Vector{Any}) = ok(x[1], x[2])
##################################

print(sum(x[1] for x in d[ok.(d)]))
