mutable struct State
    pos::Vector{Int64}
    dir::Vector{Int64}
end

function load(file)
    d = stack(eachline(file); dims=1)
    pos = findfirst(d .== '^')
    s = State([Tuple(pos)...], [-1, 0])
    d[s.pos...] = '.'
    d, s
end

rotate!(dir::Vector{Int}) = dir[1:2] = [0 1; -1 0] * dir

function iterate(d, s::State)
    newpos = s.pos + s.dir
    if !(1 ≤ newpos[1] ≤ size(d)[1] || 1 ≤ newpos[3] ≤ size(d)[2])  # Out
        return false
    end
    if d[newpos...] == '#'
        rotate!(s.dir)
        return true
    end
    s.pos = newpos
    return true
end
#######################

d, s = load("data/6.txt");

been = Set()
while true
    push!(been, s.pos)
    iterate(d, s) || break
end

println(length(been))
