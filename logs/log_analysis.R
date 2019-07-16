library(ggplot2)

logs <- read.csv("vbench_results.csv")
logs$instance <- as.factor(logs$instance)
instance_types <- levels(logs$instance)

remove_square_brackets <- function(string, edge_length=1) {
  return(substr(string, 1+edge_length, nchar(string)-(edge_length)))
}

logs$cpu <- vapply(as.character(logs$cpu), function(x) return(strtoi(remove_square_brackets(x))), c(1))

## Score

means = c()
sds = c()

for (i in instance_types) {
  print(i)
  print(paste("Mean:", mean(logs[logs$instance==i,]$score)))
  means <- c(means, mean(logs[logs$instance==i,]$score))
  print(paste("SD:", sd(logs[logs$instance==i,]$score)))
  sds <- c(sds, sd(logs[logs$instance==i,]$score))
}

ggplot(logs, aes(score, color=as.factor(cpu))) +
  geom_freqpoly(aes(y=..density..), alpha=0.7) +
  facet_grid(rows=vars(provider), cols=vars(type))

ggplot(logs, aes(x=cpu, y=score, shape=provider, color=type)) + geom_point(size=3)


### Score/price
means = c()
sds = c()

for (i in instance_types) {
  print(i)
  print(paste("Mean:", mean(logs[logs$instance==i,]$value)))
  means <- c(means, mean(logs[logs$instance==i,]$value))
  print(paste("SD:", sd(logs[logs$instance==i,]$value)))
  sds <- c(sds, sd(logs[logs$instance==i,]$value))
}

ggplot(logs, aes(value, color=as.factor(cpu))) +
  geom_freqpoly(aes(y=..density..), alpha=0.7) +
  facet_grid(rows=vars(provider), cols=vars(type))

ggplot(logs, aes(x=cpu, y=value, shape=provider, color=type)) + geom_point(size=3)

