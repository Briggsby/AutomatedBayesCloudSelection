first.num <- function(vals) {
  vals <- strsplit(vals, " ")
  vals <- lapply(vals, function(x) x[1])
  vals <- unlist(vals)
  return(as.numeric(vals))
}

first.no.num <- function(vals) {
  vals <- strsplit(vals, " ")
  vals <- lapply(vals, function(x) x[1])
  vals <- unlist(vals)
  return(as.factor(vals))
}

general_purpose <- c("A1", "T3", "T3A", "T2", "M5", "M5A", "M4", "M1", "M2", "M3", "M4", "M5AD", "T1")
compute_optimized <-  c("C5", "C5N", "C4", "C1", "C3", "Cluster")
memory_optimized <- c("R5", "R5A", "R4", "X1E", "X1", "UTB1", "Z1D", "cr1", "R3", "R5AD", "R5D")
accelerated_computing <- c("P3", "P2", "G3", "F1", "G2", "G3S", "P3DN")
storage_optimized <- c("I3", "I3EN", "D2", "H1", "hs1", "I2")

get.category <- function(vals) {
  categories <- c()
  for (val in vals) {
    if (val %in% general_purpose) {
      categories <- append(categories, "General")
    } else if (val %in% compute_optimized) {
      categories <- append(categories, "Compute")
    } else if (val %in% memory_optimized) {
      categories <- append(categories, "Memory")
    } else if (val %in% accelerated_computing) {
      categories <- append(categories, "Accelerated")
    } else if (val %in% storage_optimized) {
      categories <- append(categories, "Storage")
    } else {
      categories <- append(categories, NA)
    }
  }
  return(categories)
}


raw.dataset <- read_csv("Amazon EC2 Instance Comparison.csv")
dataset <- raw.dataset
dataset$Memory <- first.num(dataset$Memory)
dataset$`Compute Units (ECU)` <- first.num(dataset$`Compute Units (ECU)`)
dataset$vCPUs <- first.num(dataset$vCPUs)
dataset$`ECU per vCPU` <- first.num(dataset$`ECU per vCPU`)
dataset$Storage <- first.num(dataset$`Instance Storage`)

dataset$Burstable <- is.na(dataset$`ECU per vCPU`)

dataset$`Model Type` <- first.no.num(dataset$Name)
dataset$`Model Type` <- as.factor(gsub("U-\\d+TB1", "UTB1", dataset$`Model Type`))
levels(dataset$`Model Type`)[levels(dataset$`Model Type`)=="General"] <- "P2"
dataset$`Model Type` <- as.factor(apply(dataset, 1, function(x) ifelse(x["Model Type"] == "High", strsplit(x["API Name"], "\\.")[[1]], x["Model Type"])))
dataset$Category <- get.category(dataset$`Model Type`)
dataset$StorageType <- as.factor(apply(dataset,1, function(x) ifelse(is.na(x["Storage"]), "EBS", ifelse(grepl("SSD", x["Instance Storage"]), "SSD", "HDD"))))

dataset[,31:52] <- apply(dataset[,31:52], 2, function(col) as.numeric(regmatches(unlist(col), gregexpr("\\d+\\.\\d+", unlist(col)))))

write_csv(dataset, "cleaned_ec2_info.csv")
