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
    return collect(out)
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
    perimeter = sum(sum(∉(region), ix .+ dirs) for ix in region)
    perimeter * length(region)
end

##################################

d = load("data/12.txt")

println(sum(price.(regions(d))))
