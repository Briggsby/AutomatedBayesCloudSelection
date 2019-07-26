exps <- read.csv("exps_results.csv")
vbench <- exps[exps$Deployer=="vbench",]
curl_test <- exps[exps$Deployer=="ping_testserver",]

vbench$single_concurrent <- vbench$Concurrent_Jobs == 1
plot(vbench$Best_instance~vbench$Concurrent_Jobs)

vbench$success <- ifelse(vbench$Multiple_Providers == "True", vbench$Best_instance=="c5.large", vbench$Best_instance=="n1-highcpu-2")

# Getting test type:
test_types <- vector(mode="character", length=nrow(vbench))
for (i in 1:nrow(vbench)) {
  if (vbench$Concurrent_Jobs[i] == 2) {
    test_types[i] <- "Multiple providers, 2 concurrent jobs"
  } else {
    if (vbench$Multiple_Providers[i] == "True") {
      if (vbench$single_concurrent[i]) {
        test_types[i] <- "Multiple providers, single job"
      } else {
        test_types[i] <- "Multiple providers, 3 concurrent jobs"
      }
    } else {
      if (vbench$single_concurrent[i]) {
        test_types[i] <- "Single provider, single job"
      } else {
        test_types[i] <- "Single provider, 3 concurrent jobs"
      }
    }
  }
}

vbench$test_type <- as.factor(test_types)

best_result_mean <- mean(vbench$Best_Result[vbench$Best_instance == "c5.large"])
best_result_mean.google <- mean(vbench$Best_Result[vbench$Best_instance=="n1-highcpu-2"])

vbench$best_result_relative <- ifelse(vbench$Multiple_Providers == "True",
                                      vbench$Best_Result/best_result_mean,
                                      vbench$Best_Result/best_result_mean.google)

library(ggplot2)
ggplot(vbench, aes(Best_instance)) +
  geom_bar(aes(fill=success)) + 
  scale_fill_manual(values=c("red4", "chartreuse4")) +
  labs(fill="Sucessful prediction", x="Best predicted instance", y="Count") +
  facet_grid(cols=vars(test_type))

ggplot(vbench, aes(test_type, -Best_Result, group=test_type)) +
  geom_boxplot()

ggplot(vbench, aes(test_type, best_result_relative)) +
  geom_boxplot()

library(ggplot2)
library(ggrepel)
job_path <- read.csv("spearmint_exps/0/job_path.csv")

normal.plot <- ggplot(job_path, aes(vCPUs, Value, group=1)) +
  geom_point(aes(shape=Category, color=Provider), size=4) +
  geom_label_repel(aes(label=Job_number), box.padding=0.25, hjust=-2, vjust=2) +
  geom_segment(aes(xend=c(tail(vCPUs, n=-1), NA), yend=c(tail(Value, n=-1), NA)), color="purple", 
               arrow=arrow(angle=20, length=unit(0.4, "cm"))) +
  labs(title="Path of a successful Bayesian Optimization search, 3 concurrent jobs") +
  ylim(c(-8.3, -1))

job_path.fail <- read.csv("spearmint_exps/1/job_path.csv")

fail.plot <- ggplot(job_path.fail, aes(vCPUs, Value, group=1)) +
  geom_point(aes(shape=Category, color=Provider), size=4) +
  geom_label_repel(aes(label=Job_number), box.padding=0.25, hjust=-2, vjust=2) +
  geom_segment(aes(xend=c(tail(vCPUs, n=-1), NA), yend=c(tail(Value, n=-1), NA)), color="purple", 
               arrow=arrow(angle=20, length=unit(0.4, "cm"))) +
  labs(title="Path of an incorrect Bayesian Optimization search, 3 concurrent jobs") +
  ylim(c(-8.3, -1))

job_path.single <- read.csv("spearmint_exps/40/job_path.csv")

sing.job.plot <- ggplot(job_path.single, aes(vCPUs, Value, group=1)) +
  geom_point(aes(shape=Category, color=Provider), size=4) +
  geom_label_repel(aes(label=Job_number), box.padding=0.25, hjust=-2, vjust=2) +
  geom_segment(aes(xend=c(tail(vCPUs, n=-1), NA), yend=c(tail(Value, n=-1), NA)), color="purple", 
               arrow=arrow(angle=20, length=unit(0.4, "cm"))) +
  labs(title="Path of a successful Bayesian Optimization search, 1 concurrent job") +
  ylim(c(-8.3, -1))

sing.job.plot


job_path.single.fail <- read.csv("spearmint_exps/43/job_path.csv")

sing.job.plot.fail <- ggplot(job_path.single.fail, aes(vCPUs, Value, group=1)) +
  geom_point(aes(shape=Category, color=Provider), size=4) +
  geom_label_repel(aes(label=Job_number), box.padding=0.25, hjust=-2, vjust=2) +
  geom_segment(aes(xend=c(tail(vCPUs, n=-1), NA), yend=c(tail(Value, n=-1), NA)), color="purple", 
               arrow=arrow(angle=20, length=unit(0.4, "cm"))) +
  labs(title="Path of an incorrect Bayesian Optimization search, 1 concurrent job") +
  ylim(c(-8.3, -1))

library(ggpubr)
ggarrange(normal.plot + rremove("legend"),
          fail.plot + rremove("legend"),
          sing.job.plot +rremove("legend"),
          sing.job.plot.fail,
          labels=c('A', 'B', 'C', "D"))
