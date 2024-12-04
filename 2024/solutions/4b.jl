const TARGET = ['M', 'A', 'S']

# https://discourse.julialang.org/t/nested-iteration-in-comprehension/123437/2
load(file) = stack(eachline(file); dims=1)

function check(d, x, y)
    xl = maximum(x) - minimum(x)
    yl = maximum(y) - minimum(y)

    [
        [d[a...] for a in zip(i .+ x, j .+ y)] ∈ (TARGET, reverse(TARGET))
        for i in 1:(size(d, 1)-xl), j in 1:(size(d, 2)-yl)
    ]
end

forward = eachindex(TARGET) .- 1
backward = reverse(forward)

diag1(d) = check(d, forward, forward)
diag2(d) = check(d, forward, backward)


data = load("data/4.txt");
total = sum(diag1(data) .& diag2(data))
println(total)
