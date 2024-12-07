using AutoHashEquals

@auto_hash_equals mutable struct State
    pos::Vector{Int64}
    dir::Vector{Int64}
end
Base.copy(s::State) = State(copy(s.pos), copy(s.dir))

function load(file)
    d = stack(eachline(file); dims=1)
    pos = findfirst(d .== '^')
    s = State([Tuple(pos)...], [-1, 0])
    d[s.pos...] = '.'
    d, s
end



rotate(dir::Vector{Int}) = [0 1; -1 0] * dir
inbounds(d, pos) = 1 ≤ pos[1] ≤ size(d)[1] && 1 ≤ pos[2] ≤ size(d)[2]

function iterate(d, s::State)
    newpos = s.pos + s.dir
    inbounds(d, newpos) || return false  # Rat has escaped
    if d[newpos...] == '#'
        s.dir = rotate(s.dir)
        return true
    end
    s.pos = newpos
    return true
end

function would_loop(d, s::State, been_spots)
    d = copy(d)
    newpos = s.pos + s.dir
    newpos ∈ been_spots && return false
    inbounds(d, newpos) || return false
    d[newpos...] = '#'

    s = State(s.pos, rotate(s.dir))
    seen_states = Set{State}()
    while true
        if s ∈ seen_states
            return true
        end
        push!(seen_states, copy(s))
        iterate(d, s) || break
    end
    return false
end
#################

d, s = load("data/6.txt");

been_spots = Set()
loop_spots = Set()
while true
    push!(been_spots, copy(s.pos))
    if would_loop(d, s, been_spots)
        push!(loop_spots, s.pos + s.dir)
    end
    iterate(d, s) || break
end

println(length(loop_spots))
