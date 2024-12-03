using DelimitedFiles

safe(x) = all(x .∈ Ref((1, 2, 3))) || all(x .∈ Ref((-1, -2, -3)))

total = 0
for line in eachline("data/2.txt")
    m = map(x -> parse(Int, x), split(line))
    total += safe(diff(m))
end

println(total)
