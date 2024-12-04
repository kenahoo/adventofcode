const TARGET = ['X', 'M', 'A', 'S']

# https://discourse.julialang.org/t/nested-iteration-in-comprehension/123437/2
load(file) = stack(eachline(file); dims=1)

function check(d, x, y)
    xl = maximum(x) - minimum(x)
    yl = maximum(y) - minimum(y)

    sum(
        [d[a...] for a in zip(i .+ x, j .+ y)] ∈ (TARGET, reverse(TARGET))
        for i in 1:(size(d, 1)-xl), j in 1:(size(d, 2)-yl)
    )
end

stay = repeat([0], length(TARGET))
forward = eachindex(TARGET) .- 1
backward = reverse(forward)


across(d) = check(d, stay, forward)
down(d) = check(d, forward, stay)
diag1(d) = check(d, forward, forward)
diag2(d) = check(d, forward, backward)


data = load("data/4.txt");
total = across(data) + down(data) + diag1(data) + diag2(data)
println(total)
