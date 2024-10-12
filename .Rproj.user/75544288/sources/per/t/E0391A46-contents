library('haven')
library('dplyr')

fn <- read_sav('resources/fake_news.sav')
head(fn)

names(fn)

# Corrected column selection
fn <- select(fn, -starts_with('Recipient'))

names(fn[,1:20])

fn[, 'AFFECTIVE_POLARIZATION']

variable_labels <- sapply(fn, function(x) attr(x, "label"))
variable_table <- data.frame(Column_Name = names(variable_labels), Variable_Label = variable_labels)
print(variable_table)
write.csv(variable_table, "resources/questions.csv", row.names = FALSE)
