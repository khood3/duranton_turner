setwd('C:/Users/hood_/Dropbox/urban economics sp24/problem sets/problem set 3/R')
load('dtData-1.RData')
library(lmtest)
library(sandwich)

##Data prep
dtDataUse <- subset(dtData, 
                    subset = !is.na(ln_km_IH_83)  & !is.na(ln_km_IH_93) & !is.na(ln_km_IH_03) & ln_km_IH_83 > 0  & ln_km_IH_93 > 0 & ln_km_IH_03 > 0, 
                    select = c('vmt_IH_83','vmt_IH_93','vmt_IH_03','ln_km_IH_83','ln_km_IH_93', 'ln_km_IH_03','pop80','pop90','pop00'))
#dtDataUse <- subset(dtData, 
#                    select = c('vmt_IH_83','vmt_IH_93','vmt_IH_03','ln_km_IH_83','ln_km_IH_93', 'ln_km_IH_03','pop80','pop90','pop00'))

##Question 1 (these are two alternative approaches)
a <- lapply(dtDataUse,mean,na.rm = TRUE)
summary(dtDataUse)

ols83 <- lm(log(dtDataUse$vmt_IH_83) ~ log(dtDataUse$ln_km_IH_83) + log(dtDataUse$pop80))
summary(ols83)

##Question 2:
ols83 <- lm(log(vmt_IH_83) ~ log(ln_km_IH_83) + log(pop80),data = dtDataUse)
coeftest(ols83, vcov = vcovHC(ols83, "HC1"))
ols93 <- lm(log(vmt_IH_93) ~ log(ln_km_IH_93) + log(pop90),data = dtDataUse)
coeftest(ols93, vcov = vcovHC(ols93, "HC1"))
ols03 <- lm(log(vmt_IH_03) ~ log(ln_km_IH_03) + log(pop00),data = dtDataUse)
coeftest(ols03, vcov = vcovHC(ols03, "HC1"))

##Question 3
dtDataUse$dVMT9303 <- log(dtDataUse$vmt_IH_03)-log(dtDataUse$vmt_IH_93)
dtDataUse$dLnKM9303 <- log(dtDataUse$ln_km_IH_03)-log(dtDataUse$ln_km_IH_93)
dtDataUse$dpop9303 <- log(dtDataUse$pop00)-log(dtDataUse$pop90)

dif9303 <- lm(dVMT9303 ~ dLnKM9303 + dpop9303,data = dtDataUse)
coeftest(dif9303, vcov = vcovHC(dif9303, "HC1"))

