exps <- read.csv("exps_results.csv")

exps$single_concurrent <- exps$Concurrent_Jobs == 1

exps$success <- ifelse(exps$Multiple_Providers == "True", exps$Best_instance=="c5.large", exps$Best_instance=="n1-highcpu-2")
exps$success <- ifelse(exps$Deployer == "ping_testserver", (exps$Best_instance == "c5.large" | exps$Best_instance == "m5.large"), exps$success)
# Getting test type:
test_types <- vector(mode="character", length=nrow(exps))
for (i in 1:nrow(exps)) {
  if (exps$Deployer[i] == "ping_testserver") {
    test_types[i] <- "Ping test, 1 concurrent job, multiple providers"
  }
  else if (exps$Concurrent_Jobs[i] == 2) {
    test_types[i] <- "Multiple providers, 2 concurrent jobs"
  } else {
    if (exps$Multiple_Providers[i] == "True") {
      if (exps$single_concurrent[i]) {
        test_types[i] <- "Multiple providers, single job"
      } else {
        test_types[i] <- "Multiple providers, 3 concurrent jobs"
      }
    } else {
      if (exps$single_concurrent[i]) {
        test_types[i] <- "Single provider, single job"
      } else {
        test_types[i] <- "Single provider, 3 concurrent jobs"
      }
    }
  }
}

# SHOULD ALSO DO TIME TAKEN USING THE TIMESTAMPS!!!

exps$test_type <- factor(test_types, levels=c("Single provider, single job",
                          "Single provider, 3 concurrent jobs",
                          "Multiple providers, single job",
                          "Multiple providers, 2 concurrent jobs",
                          "Multiple providers, 3 concurrent jobs",
                          "Ping test, 1 concurrent job, multiple providers"))

best_result_mean <- mean(exps$Best_Result[exps$Best_instance == "c5.large" & exps$Deployer == "vbench"])
best_result_mean.google <- mean(exps$Best_Result[exps$Best_instance=="n1-highcpu-2" & exps$Deployer == "vbench"])
best_result_mean.curltest <- mean(exps$Best_Result[exps$Deployer == "ping_testserver"])

exps$Best_Result_Relative <- ifelse(exps$Multiple_Providers == "True",
                                      exps$Best_Result/best_result_mean,
                                      exps$Best_Result/best_result_mean.google)
exps$Best_Result_Relative <- ifelse(exps$Deployer == "ping_testserver",
                                      exps$Best_Result/best_result_mean.curltest,
                                      exps$Best_Result_Relative)


library(dplyr)
library(ggplot2)
ggplot(exps, aes(Best_instance)) +
  geom_bar(aes(fill=success)) + 
  scale_fill_manual(values=c("red4", "chartreuse4")) +
  labs(fill="Sucessful prediction", x="Best predicted instance", y="Count") +
  facet_wrap(~test_type)

ggplot(exps, aes(test_type, -Best_Result, group=test_type)) +
  geom_boxplot() +
  stat_summary(fun.y=mean, colour="darkblue", geom="point", 
               shape=18, size=3)

results.plot <- ggplot(exps, aes(test_type, Best_Result_Relative, group=test_type, fill=test_type)) +
  geom_boxplot() +
  stat_summary(fun.y=mean, colour="darkblue", geom="point", 
               shape=18, size=3) +
  theme(axis.title.x = element_blank(), axis.text.x = element_blank()) +
  labs(y = "Best returned result as a proportion \nof mean from potential best machine", fill = "Test Type",
       title = "Boxplots of best values returned \nfor different Bayesian Optimization searches")

time.plot <- ggplot(exps, aes(test_type, Time, group=test_type, fill=test_type)) +
  geom_boxplot() +
  stat_summary(fun.y=mean, colour="darkblue", geom="point", 
               shape=18, size=3) +
  coord_cartesian(ylim=c(0, 2000)) +
  theme(axis.title.x = element_blank(), axis.text.x = element_blank()) +
  labs(y = "Time in seconds between \nstart of first and last job", fill = "Test Type",
       title = "Boxplots of time taken for different \nBayesian Optimization searches")
# One outlier removed where time was > 4000 for 3 concurrent jobs

exps$cost_scale = scale(exps$Cost, 0)

cost.plot <- ggplot(exps, aes(test_type, cost_scale, group=test_type, fill=test_type)) +
  geom_boxplot() +
  stat_summary(fun.y=mean, colour="darkblue", geom="point", 
               shape=18, size=3) +
  theme(axis.title.x = element_blank(), axis.text.x = element_blank()) +
  labs(y = "Relative estimated search cost", fill = "Test Type",
       title = "Boxplots of relative search cost for \ndifferent Bayesian Optimization searches")

exps.summ <- exps %>% group_by(test_type) %>% summarise(mean_rel_result = mean(Best_Result_Relative),
                                                        sd_rel_result = sd(Best_Result_Relative),
                                                        n_samples = n(),
                                                        ci95 = qt(0.975,df=n_samples-1)*sd_rel_result/sqrt(n_samples))

library(ggpubr)
ggarrange(results.plot + rremove("legend"),
          time.plot + rremove("legend"),
          cost.plot +rremove("legend"),
          cowplot::get_legend(results.plot),
          labels=c('A', 'B', 'C'))

vbench <- exps[exps$Deployer=="vbench",]
curl_test <- exps[exps$Deployer=="ping_testserver",]


time.mod <- 


ggplot(exps.summ, aes(test_type, mean_rel_result)) +
  geom_col() +
  geom_errorbar(aes(ymin=mean_rel_result-ci95, ymax=mean_rel_result+ci95))

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
