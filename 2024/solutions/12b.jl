function load(file)
    stack(eachline(file); dims=1)
end

dirs = CartesianIndex.([(1, 0), (0, 1), (-1, 0), (0, -1)])

mask(x, d) = filter(inbounds(d), x .+ dirs)
inbounds(d, loc) = loc ∈ CartesianIndices(d)
inbounds(d) = loc -> inbounds(d, loc)

function region(loc, d)
    queue = [loc]
    out = Set([loc])
    while !isempty(queue)
        for c in mask(pop!(queue), d)
            if d[c] == d[loc] && c ∉ out
                push!(out, c)
                push!(queue, c)
            end
        end
    end

    return out
end

function regions(d)
    seen = Set()
    out = Set()

    for ix in CartesianIndices(d)
        ix ∈ seen && continue
        r = region(ix, d)
        push!(out, r)
        union!(seen, r)
    end

    out
end

function price(region)
    sides(region) * length(region)
end

function sides(region)
    out = 0

    for i in 1:4
        # Count as a side if it has e.g. an upper edge, but its right neighbor doesn't have an upper edge
        b = Set(x for x in region if x + dirs[i] ∉ region)
        out += sum((x + dirs[1+i%4]) ∉ b for x in b)
    end

    out
end

##################################

d = load("data/12.txt")

sum(price.(regions(d)))

