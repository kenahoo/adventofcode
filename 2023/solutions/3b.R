library(dplyr)

d <- scan('3.txt', what=character(), sep=NULL)
n <- length(d)

dmat <- d %>%
  lapply(function(x) unlist(strsplit(x, ''))) %>%
  do.call(rbind, .)

locs <- gregexec("\\d+", d, perl=TRUE)
rmatches <- regmatches(d, locs)

matches <- data.frame()
for (i in seq_along(d)) {
  if (locs[[i]][1]==-1)
    next
  for (j in seq_along(locs[[i]])) {
    pos <- locs[[i]][j]
    len <- attr(locs[[i]], 'match.length')[j]
    
    mask_i <- max(i-1, 1):min(i+1, n)
    mask_j <- max(pos-1, 1):min(pos+len, n)
    
    star_locs <- which(dmat=="*"
                       & row(dmat) %in% mask_i
                       & col(dmat) %in% mask_j, TRUE) %>% as.data.frame()
    
    if (nrow(star_locs) > 0) {
      matches <- rbind(matches, star_locs %>% mutate(num=as.numeric(rmatches[[i]][j])))
    }
  }
}

matches <- matches %>%
  arrange(row, col) %>% 
  mutate(id=paste(row, col))
counts <- table(matches$id)
matches <- matches %>% 
  mutate(count=counts[id]) %>% 
  filter(count==2)

with(matches,
     print(
       sum(num[seq_along(num)%%2==0] * num[seq_along(num)%%2==1])
     ))
print(sum(matches))

