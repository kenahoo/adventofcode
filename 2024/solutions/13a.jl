using LinearAlgebra

function load(file)
    map(assemble, eachmatch(r"A: X.(\d+), Y.(\d+).*?B: X.(\d+), Y.(\d+).*?Prize: X=(\d+), Y=(\d+)"s, read(file, String)))
end

function assemble(m::RegexMatch)
    c = parse.(Int, m.captures)
    [c[1] c[3]; c[2] c[4]], [c[5], c[6]]
end

function solve(M, b)
    try
        return Int.(round.(M \ b, digits=5)) ⋅ [3, 1]
    catch e
        e isa InexactError && return 0
        rethrow(e)
    end
end

##################################

d = load("data/13.txt")

println(sum(solve(x...) for x in d))
