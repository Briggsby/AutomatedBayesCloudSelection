exps <- read.csv("exps_results.csv")
vbench <- exps[exps$Deployer=="vbench",]
curl_test <- exps[exps$Deployer=="ping_testserver",]

vbench$single_concurrent <- vbench$Concurrent_Jobs == 1
plot(vbench$Best_instance~vbench$Concurrent_Jobs)

vbench$test_type <- ifelse(vbench$single_concurrent, "Single Job", ifelse(vbench$Multiple_Providers == 'True', "Multiple jobs and providers", "Single Provider"))


library(ggplot2)
ggplot(vbench, aes(Best_instance)) +
  geom_bar() +
  facet_grid(cols=vars(test_type))

