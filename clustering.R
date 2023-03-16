install.packages(naivebayes)

library(naivebayes)
library(plotly)
library(dplyr)
library(psych)
library(readxl)
library(tidyverse)
library(factoextra)
library(RColorBrewer)


agency_budgets <- na.omit(read_excel("agency_budgets.xlsx", 
                         col_types = c("skip", # Organization
                                       "text", # Country
                                       "skip", # Region
                                       "skip", # Annual Budget, self-est.
                                       "skip", # EuroConsult est., military+civil (2021)
                                       "skip", # Space in Africa est. (2020)
                                       "skip", # GDP
                                       "skip", # GDP/capita
                                       "numeric", # Budget/GDP %
                                       "numeric", # Budget/capita (USD)
                                       "skip", # Year of data
                                       "numeric", # Active sats.
                                       "skip", # Soviet former
                                       "skip", # ESA member
                                       "skip", # Source(s)
                                       "skip" # Comments
                         )))
agency_budgets <- agency_budgets %>% remove_rownames %>% column_to_rownames(var="Country")

#TO REMOVE NASA/others
removelist <- c("NASA*", "CNSA*", "Luxembourg Space Agency", "Roscosmos", "CNES", "Office of Space Affairs (Monaco)")
budgets_thinned <- agency_budgets[!(row.names(agency_budgets) %in% removelist),]

x <- agency_budgets$`Budget/GDP %`
y <- agency_budgets$`Budget/capita (USD)`
z <- agency_budgets$`Active satellites`
a <- agency_budgets$`GDP/capita`

pairs(agency_budgets[2:4])
scaled <- agency_budgets[1]
scaled$`Budget/GDP %` <- scale(x)
scaled$`Budget/capita (USD)` <- scale(y)
scaled$`Active satellites` <- scale(z)


distance = dist(scaled, method = "euclidean")
hc1 <- hclust(distance, method = "complete")
plot(hc1, cex = 0.6, hang = -1)

#simple PCA
  #Gentle Machine Learning
  #Dr. Ho's book under unsupervised
  #datageneration.org
  #Principal Component Analysis


SP <- plot_ly(x=log(x), y=log(y), z=log(z), 
              type="scatter3d", mode="markers", color=a)
SP

row.names(agency_budgets)
apply(agency_budgets, 2, mean)
apply(agency_budgets, 2, var)

#WITH NASA
pr.out=prcomp(agency_budgets, scale=TRUE)
#WITHOUT NASA/OTHERS
pr.out=prcomp(budgets_thinned, scale=TRUE)

names(pr.out)
pr.out$center
pr.out$scale
pr.out$rotation
dim(pr.out$x)

pr.out$rotation=-pr.out$rotation
pr.out$x=-pr.out$x
biplot(pr.out, scale=0)

pr.out$sdev
pr.var=pr.out$sdev^2
pr.var
pve=pr.var/sum(pr.var)
pve

plot(pve, xlab="Principal Component", ylab="Proportion of Variance Explained", ylim=c(0,1),type='b')

fviz(pr.out, "ind", geom = "auto", mean.point = TRUE, font.family = "Georgia")
fviz_pca_biplot(pr.out, font.family = "Georgia", col.var="firebrick1")



budget_cluster <- kmeans(agency_budgets, centers = 5,
                         iter.max = 10,
                         nstart = 25)
budget_cluster

budget.km <- eclust(agency_budgets, "kmeans", k = 8, nboot = 2)
thinned.km <- eclust(budgets_thinned, "kmeans", k = 4, nboot = 2)


#########################################################################
# At this point I realized I need to scale the data better: going to use 
# "maximum absolute scaling" (x/max(x))

budgets.logged <- agency_budgets
budgets.logged[, 1:3] <- log(budgets.logged[1:3], 2)

budgets.mas <- apply(budgets.logged, 2, function(x) x/max(x))
withoutNASA.mas <- budgets.mas[!(row.names(budgets.mas) %in% c("NASA", "CNSA")),]
thinned.mas <- budgets.mas[!(row.names(budgets.mas) %in% removelist),]

#full
pr.mas=prcomp(budgets.mas, scale=TRUE)
#thinned
pr.mas=prcomp(thinned.mas, scale=TRUE)
#removeNASAonly
pr.mas=prcomp(withoutNASA.mas, scale=TRUE)

fviz_pca_biplot(pr.mas, font.family = "Georgia", col.var="firebrick1")

budgets.mas.km <- eclust(budgets.mas, "kmeans", k = 4, nboot = 2)  
thinned.mas.km <- eclust(thinned.mas, "kmeans", k = 4, nboot = 2)  
withoutNASA.mas.km <- eclust(withoutNASA.mas, "kmeans", k = 3, nboot = 2)

# This isn't final, but it will at least allow me to weigh variables


#######################################################################
# NEXT STEP: take out GDP/capita, merge satellite totals
# averaging satellites operated/owned
threevar <- agency_budgets[, colnames(agency_budgets)[2:5]]
threevar$`Active satellites mean` <- 
  rowMeans(threevar[,c('Active satellites owned/operated', 
                       'Active satellites contracted')], na.rm=TRUE)
threevar <- select(threevar, - c('Active satellites owned/operated', 
                                 'Active satellites contracted'))

threevar.logged <- threevar
threevar.logged[, 1:2] <- log(threevar.logged[1:2], 2)

threevar.mas <- apply(threevar.logged, 2, function(x) x/max(x))
withoutNASA.mas <- threevar.mas[!(row.names(threevar.mas) %in% c("NASA*", "CNSA*")),]
thinned.mas <- threevar.mas[!(row.names(threevar.mas) %in% removelist),]

#full
pr.mas=prcomp(threevar.mas, scale=TRUE)
#thinned
pr.mas=prcomp(thinned.mas, scale=TRUE)
#removeNASAonly
pr.mas=prcomp(withoutNASA.mas, scale=TRUE)

fviz_pca_biplot(pr.mas, font.family = "Georgia", col.var="firebrick1")

threevar.mas.km <- eclust(threevar.mas, "kmeans", k = 5, nboot = 2)  
thinned.mas.km <- eclust(thinned.mas, "kmeans", k = 3, nboot = 2)  
withoutNASA.mas.km <- eclust(withoutNASA.mas, "kmeans", k = 4, nboot = 2)


##########################################################################
# Then I realized the "mean" wasn't a proper way.
# I redid my python cleaning process to introduce a single involvement metric
# per satellite, regardless contracted, owned or operated. Simple involvement

df <- na.omit(read_excel("agency_budgets.xlsx", 
                         col_types = c("skip", # Organization
                                       "text", # Country
                                       "text", # Region [SKIP WHEN ANALYZE]
                                       "skip", # Annual Budget, self-est.
                                       "skip", # EuroConsult est., military+civil (2021)
                                       "skip", # Space in Africa est. (2020)
                                       "skip", # GDP
                                       "skip", # GDP/capita
                                       "numeric", # Budget/GDP %
                                       "numeric", # Budget/capita (USD)
                                       "skip", # Year of data
                                       "numeric", # Active sats.
                                       "skip", # Soviet former
                                       "skip", # ESA member
                                       "skip", # Source(s)
                                       "skip" # Comments
                                       )))
df <- df %>% remove_rownames %>% column_to_rownames(var="Country")

#TO REMOVE NASA/others
removelist <- c("United States", "China", "Luxembourg", "Russia", "France", "Monaco", "United Kingdom", "Germany")

df[1:2] <- log(df[1:2], 2) # logging data

df[1:3] <- apply(df[1:3], 2, function(x) x/max(x))
df0 <- df[!(row.names(df) %in% c("United States", "China")),]
df00 <- df[!(row.names(df) %in% removelist),]

#full
pr = prcomp(df, scale=TRUE)
#thin
pr0 = prcomp(df0, scale=TRUE)
#thinner
pr00 = prcomp(df00, scale=TRUE)


fviz_pca_biplot(pr, font.family = "Georgia", col.var="firebrick1")
fviz_pca_biplot(pr0, font.family = "Georgia", col.var="firebrick1")
fviz_pca_biplot(pr00, font.family = "Georgia", col.var="firebrick1")

df.km <- eclust(df, "kmeans", k = 5, nboot = 2)  
df0.km <- eclust(df0, "kmeans", k = 4, nboot = 2)  
df00.km <- eclust(df00, "kmeans", k = 2, nboot = 2)

#making 3d plot
fig <- plot_ly(df, x = ~`Budget/GDP %`, y = ~`Budget/capita (USD)`, 
               z = ~`Active sats.`, color = ~Region, 
               #text = ~paste('Country: ', ~Country),
               colors = c("#6cc6cc", "#435fd1", "#d1a836", "#0a7d36", "#8595d6", 
                                   "#daa2e8", "#e64040", "#8f7965", "#59392b")) %>%
  add_markers(size = 50)

fig <- fig %>% layout(# title = '',
                      scene = list(xaxis = list(# title = '',
                                                gridcolor = 'rgb(255, 255, 255)',
                                                # range = c(2.003297660701705, 5.191505530708712),
                                                type = 'log',
                                                zerolinewidth = 1,
                                                ticklen = 5,
                                                gridwidth = 2),
                                   yaxis = list(# title = 'Life Expectancy (years)',
                                                gridcolor = 'rgb(255, 255, 255)',
                                                # range = c(36.12621671352166, 91.72921793264332),
                                                type = 'log',
                                                zerolinewidth = 1,
                                                ticklen = 5,
                                                gridwith = 2),
                                   zaxis = list(#title = 'Population',
                                                gridcolor = 'rgb(255, 255, 255)',
                                                type = 'log',
                                                zerolinewidth = 1,
                                                ticklen = 5,
                                                gridwith = 2)),
                      paper_bgcolor = 'rgb(243, 243, 243)',
                      plot_bgcolor = 'rgb(243, 243, 243)')

fig
