library(ggplot2)

# import dataset from csv
df <- read.csv("models/continuedLearningall-mpnet-base-v1-2023-01-04_15-58-07/eval/binary_classification_evaluation_mrpc-dev_results copy.csv", header = TRUE, sep = ",")


# remove row where steps is -1
df <- df[df$steps != -1, ]

df$steps <- ifelse(df$epoch == 1, df$steps + 230, df$steps)


# plot learning curve
ggplot(df, aes(x = steps, y = cossim_f1)) +
    geom_line() +
    geom_point() +
    labs(x = "Iteration", y = "F1 Score") +
    theme_bw() +
    theme(text = element_text(size = 20)) +
    theme(plot.title = element_text(hjust = 0.5)) +
    ggtitle("Learning curve over two epochs \n(evaluation every ten samples)")

# show plot
ggsave("learningCurve.png", width = 10, height = 6)