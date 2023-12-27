library(magrittr)

d <- scan('3.txt', what=character(), sep=NULL)
n <- length(d)

dmat <- d %>%
  lapply(function(x) unlist(strsplit(x, ''))) %>%
  do.call(rbind, .)

is_sym <- apply(dmat, 2, function(x) grepl("[^0-9.]", x))
is_star <- apply(dmat, 2, `==`, "*")

# is_digit <- apply(d, 2, function(x) grepl("[0-9]", x))

# 
# d <- scan('3.txt', what=character(), sep=NULL)
# 
# d <- scan('3.txt', what=character(), sep=NULL) %>% 
#   paste0(collapse='')
n <- sqrt(nchar(d))
# 
# locs <- gregexec("\\d\\d\\d", d, perl=TRUE)[[1]] %>% c
# 
# good <- function(loc) {
#   mask <- data.frame(x=loc[1]-1,
#                      y=loc[2]+0:3)
#   
#   mask <- c()
#   if (loc > n)
#     mask <- c(mask, loc - n + 0:3)
#   if (loc < n*(n-1))
#     mask <- c(mask, loc + n + 0:3)
#   if (loc % n > 1)
#     mask <- c(mask, loc - 1)
#   if (loc % n < n-2)
#     mask <- c(mask, )
#     mask <- c(loc - n, loc - 1, loc + 1, loc + n)
# }

locs <- gregexec("\\d+", d, perl=TRUE)
rmatches <- regmatches(d, locs)

matches <- c()
for (i in seq_along(d)) {
  for (j in seq_along(locs[[i]])) {
    pos <- locs[[i]][j]
    len <- attr(locs[[i]], 'match.length')[j]
    mask_i <- max(i-1, 1):min(i+1, n)
    mask_j <- max(pos-1, 1):min(pos+len, n)
    # print(dmat[mask_i, mask_j])
    # print(any(is_sym[mask_i, mask_j]))
# if (substr(d[i], j, j+2) == "761") browser()
    if(any(is_sym[mask_i, mask_j]))
      matches <- c(matches, as.numeric(rmatches[[i]][j]))
  }
}

print(sum(matches))


# matches <- sapply(locs[sapply(good, locs)], function(x) substr(d, x, x+2))
# matches %>% as.numeric %>% sum %>% print

