exps <- read.csv("exps_results.csv")
vbench <- exps[exps$Deployer=="vbench",]
curl_test <- exps[exps$Deployer=="ping_testserver",]

vbench$single_concurrent <- exps$Concurrent_Jobs == 1
plot(vbench$Best_instance~vbench$Concurrent_Jobs)


library(ggplot2)
ggplot(vbench, aes(Best_instance)) +
  geom_bar() +
  facet_grid(rows=vars(single_concurrent),
             cols=vars(Multiple_Providers))

