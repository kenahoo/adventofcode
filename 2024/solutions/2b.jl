using DelimitedFiles
using InvertedIndices: Not

safe(x) = all(x .∈ Ref((1, 2, 3))) || all(x .∈ Ref((-1, -2, -3)))

mostly_safe(x) = safe(diff(x)) || any(i -> safe(diff(x[Not(i)])), eachindex(x))

total = 0
for line in eachline("data/2.txt")
    m = map(x -> parse(Int, x), split(line))
    total += mostly_safe(m)
end

println(total)
