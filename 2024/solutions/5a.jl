
matches(re, x) = !isnothing(match(re, x))


function load(file)
    lines = readlines(file)
    rules = Set(x for x in lines if matches(r"\d+\|\d+", x))
    pages = filter(x -> matches(r"^\d+(,\d+)*$", x), lines) .|>
            (x -> parse.(Int, split(x, ",")))
    (rules, pages)
end



rules, pages = load("data/5.txt")

my_isless(x, y) = "$x|$y" ∈ rules

total = 0
for page in pages
    p2 = sort(page, lt=my_isless)
    if page == p2
        total += p2[1+end÷2]
    end
end

println(total)
