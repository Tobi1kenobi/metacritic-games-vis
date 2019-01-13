metafile <- read_delim('../../Data/critic_and_users_adjective_only.csv', delim = ',',col_types = cols(.default = "c")) %>% 
	mutate(nameAndConsole = paste(name, ' (' ,console, ')', sep = '')) %>% 
	select(nameAndConsole, "Critic" = `critic adjectives`, 'User' = `user adjectives`, metascore, userscore)

metafile2 <- read_delim('../../Data/extra_details_complete.csv', delim = ',',col_types = cols(.default = "c")) %>%
	mutate(nameAndConsole = paste(name, ' (' ,console, ')', sep = '')) %>% 
	select(nameAndConsole, developer)

negWords <- scan('../../Data/negative_adjectives.txt', what = '', sep = '\n')
posWords <- scan('../../Data/positive_adjectives.txt', what = '', sep = '\n')

getScore <- memoise(function(game, type){

	line <- metafile[metafile$nameAndConsole == game, ]

	if (type == 'Critic'){
		scoreType <- paste('<b>Average critic score: ', line[,'metascore'],'</b>')
	} else {
		scoreType <- paste('<b>Average user score: ', line[,'userscore'],'</b>')
	}
})

getTermMatrix <- memoise(function(game, type) {

	line <- metafile[metafile$nameAndConsole == game, ]
	dev <- metafile2[metafile2$nameAndConsole == game, ]$developer

	adjecs <- unlist(line[,type])
	
	crit_words <- unlist(strsplit(adjecs, ','))
	crit_words_neg <- paste(crit_words[crit_words %in% negWords], collapse = ' ')
	crit_words_pos <- paste(crit_words[crit_words %in% posWords], collapse = ' ')
	crit_words_neu <- paste(crit_words[crit_words %ni% c(negWords, posWords)], collapse = ' ')
	crit_words_all <- c(crit_words_neg, crit_words_pos, crit_words_neu)

	bannedWords <- tolower(paste(unlist(game), unlist(dev), 'not'))
	bannedWords <- unlist(strsplit(bannedWords, ' '))

	corpus = Corpus(VectorSource(crit_words_all))
	corpus = tm_map(corpus, removeWords, bannedWords)
	tdm = TermDocumentMatrix(corpus)
	colnames(tdm) = c('Negative','Positive','Neutral')
	tdm = as.matrix(tdm)
})