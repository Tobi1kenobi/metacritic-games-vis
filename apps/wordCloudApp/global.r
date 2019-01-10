metafile <- read_delim('../../Data/critic_and_users_adjective_only.csv', delim = ',',col_types = cols(.default = "c")) %>% 
  mutate(nameAndConsole = paste(name, ' (' ,console, ')', sep = '')) %>% 
  select(nameAndConsole, `critic adjectives`, `user adjectives`)

getTermMatrix <- memoise(function(game) {

	line <- metafile[metafile$nameAndConsole == game, ]

	text <- str_replace_all(line$`user adjectives`, ',', ' ')

	myCorpus = Corpus(VectorSource(text))
	myCorpus = tm_map(myCorpus, content_transformer(tolower))
	myCorpus = tm_map(myCorpus, removePunctuation)
	myCorpus = tm_map(myCorpus, removeNumbers)
	myCorpus = tm_map(myCorpus, removeWords,
		c(stopwords("SMART"), "thy", "thou", "thee", "the", "and", "but"))

	myDTM = TermDocumentMatrix(myCorpus,
		control = list(minWordLength = 1))
  
	m = as.matrix(myDTM)
  
	sort(rowSums(m), decreasing = TRUE)
})