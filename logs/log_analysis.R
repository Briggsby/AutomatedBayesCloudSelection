library(ggplot2)

logs <- read.csv("vbench_results.csv")
logs$instance <- as.factor(logs$instance)
instance_types <- levels(logs$instance)

remove_square_brackets <- function(string, edge_length=1) {
  return(substr(string, 1+edge_length, nchar(string)-(edge_length)))
}

logs$cpu <- vapply(as.character(logs$cpu), function(x) return(strtoi(remove_square_brackets(x))), c(1))
google_logs = logs[logs$provider == "['google']",]
aws_logs = logs[logs$provider == "['aws']",]
levels(logs$provider) <- c("Amazon EC2", "Google Compute Engine")

# logs$score <- logs$throughput

ns <- c()
norms <- c()
## Score
score_means = c()
score_sds = c()
score_relsds = c()
### Score/price
value_means = c()
value_sds = c()
value_relsds = c()

for (i in instance_types) {
  print(i)
  ns <- c(ns, nrow(logs[logs$instance==i,]))
  s_mean <- mean(logs[logs$instance==i,]$score)
  s_sd <- sd(logs[logs$instance==i,]$score)
  print(paste("Mean:", s_mean))
  score_means <- c(score_means, s_mean)
  print(paste("SD:", s_sd))
  print(paste("n:", nrow(logs[logs$instance==i,])))
  score_sds <- c(score_sds, s_sd)
  score_relsds <- c(score_relsds, s_sd/s_mean)
  qqnorm(logs[logs$instance==i,]$score, main=i)
  norm <- shapiro.test(logs[logs$instance==i,]$score)
  print(norm)
  norms <- c(norms, norm$p.value)
  v_mean <- mean(logs[logs$instance==i,]$value)
  v_sd <- sd(logs[logs$instance==i,]$value)
  print(paste("Mean:", v_mean))
  value_means <- c(value_means, v_mean)
  print(paste("SD:", v_sd))
  value_sds <- c(value_sds, v_sd)
  value_relsds <- c(value_relsds, v_sd/v_mean)
}

names(ns) <- instance_types
names(norms) <- instance_types
names(score_means) <- instance_types
names(score_sds) <- instance_types
names(score_relsds) <- instance_types 

names(value_means) <- instance_types
names(value_sds) <- instance_types
names(value_relsds) <- instance_types 

library(dplyr)
logs.summ <- logs %>% group_by(instance) %>%
  summarise(cpu=names(table(cpu)[which.max(table(cpu))]),
            type=names(table(type)[which.max(table(type))]),
            provider=names(table(provider)[which.max(table(provider))]),
            n = n(),
            mean_score =mean(score),
            sd_score = sd(score),
            relsd_score = sd_score/mean_score,
            mean_val = mean(value))
            

mod <- lm(score ~ instance, data=logs)
aov <- aov(mod)
TukeyHSD(aov)

mod2 <- lm(score ~ as.factor(cpu)*provider*type, logs)
aov2 <- aov(mod2)
TukeyHSD(aov2)

mod.value <- lm(value ~ instance, data=logs)
aov.value <- aov(mod.value)
TukeyHSD(aov.value)

mod.value2 <- lm(value ~ as.factor(cpu)*provider*type, logs)
aov.value2 <- aov(mod.value2)
TukeyHSD(aov.value2)

ggplot(logs, aes(score)) +
  geom_histogram() +
  facet_wrap(~instance)

v.scores <- ggplot(logs, aes(as.factor(cpu), score, color=provider)) +
  geom_boxplot() + 
  xlab("vCPU #") + ylab("vBench Score") +
  labs(title="vBench scores for different cloud configurations", color="Provider") +
  facet_grid(cols=vars(type))

ggplot(logs, aes(as.factor(cpu), score)) +
  geom_boxplot() + 
  facet_grid(rows=vars(provider), cols=vars(type), scales="free_y")

ggplot(google_logs, aes(as.factor(cpu), score)) +
  geom_boxplot() + 
  facet_grid(cols=vars(type))
ggplot(aws_logs, aes(as.factor(cpu), score)) +
  geom_boxplot() + 
  facet_grid(cols=vars(type))

ggplot(logs, aes(score, color=as.factor(cpu))) +
  geom_freqpoly(aes(y=..density..), alpha=0.7) +
  labs(title="Distributions of vBench scores for different instance configurations", 
       x="Score", y = "Density", color="vCPUs") +
  facet_grid(rows=vars(provider), cols=vars(type))

ggplot(logs, aes(score, fill=as.factor(cpu))) +
  geom_histogram(aes(y=..density..), alpha=0.7, position="identity") +
  facet_grid(rows=vars(provider), cols=vars(type))

ggplot(logs, aes(x=cpu, y=score, shape=provider, color=type)) + geom_point(size=3)


v.vals <- ggplot(logs, aes(as.factor(cpu), value, color=provider)) +
  geom_boxplot() + 
  xlab("vCPU #") + ylab("Score/Price") +
  labs(title="Objective function result (vBench score / price per hour) \nfor different cloud configurations",
       color="Provider") +
  facet_grid(cols=vars(type), scales="free_y")

library(ggpubr)
ggarrange(v.scores + rremove("legend"),
          v.vals + rremove("legend"),
          cowplot::get_legend(v.vals),
          labels = c("A", "B"),
          nrow=1, widths=c(3, 3, 1))

ggplot(logs, aes(as.factor(cpu), value)) +
  geom_boxplot() + 
  facet_grid(rows=vars(provider), cols=vars(type), scales="free_y")

ggplot(google_logs, aes(as.factor(cpu), value)) +
  geom_boxplot() + 
  facet_grid(cols=vars(type))

ggplot(aws_logs, aes(as.factor(cpu), value)) +
  geom_boxplot() + 
  facet_grid(cols=vars(type))


ggplot(logs, aes(value, color=as.factor(cpu))) +
  geom_freqpoly(aes(y=..density..), alpha=0.7) +
  facet_grid(rows=vars(provider), cols=vars(type))

ggplot(logs, aes(value, color=as.factor(cpu))) +
  geom_histogram(aes(y=..density..), alpha=0.7) +
  facet_grid(rows=vars(provider), cols=vars(type))

ggplot(logs, aes(x=cpu, y=value, shape=provider, color=type)) + geom_point(size=3)

