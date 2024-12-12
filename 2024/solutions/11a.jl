function load(file)
    parse.(BigInt, split(readline(file)))
end

function step(d::Integer)
    d == 0 && return [one(d)]
    ndigits = length(digits(d))
    iseven(ndigits) && return [d ÷ 10^(ndigits ÷ 2), d % 10^(ndigits ÷ 2)]
    return [d * 2024]
end

step(d::Vector{<:Integer}) = vcat(step.(d)...)
##################################

d = load("data/11.txt")

for i in 1:25
    d = step(d)
end

println(length(d))
