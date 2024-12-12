function load(file)
    parse.(BigInt, split(readline(file)))
end

function blowup(d::Integer, n)
    n == 0 && return 1
    d == 0 && return blowup(one(d), n - 1)
    ndigits = length(digits(d))
    iseven(ndigits) && return blowup([d ÷ 10^(ndigits ÷ 2), d % 10^(ndigits ÷ 2)], n - 1)  # Let it cache
    return blowup([d * 2024], n - 1)
end

function blowup(d::Integer, n, cache)
    return get!(cache, (d, n)) do
        blowup(d, n)
    end
end

cache = Dict()
blowup(d::Vector{<:Integer}, n) = sum(blowup(d, n, cache) for d in d)
##################################

d = load("data/11.txt")

println(blowup(d, 75))
