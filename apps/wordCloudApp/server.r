function(input, output, session) {
  # Define a reactive expression for the document term matrix

  eventReactive(
    input$user,
    text <- str_replace_all(line$`user adjectives`, ',', ' ')
    )
  eventReactive(
    input$critic,
    text <- str_replace_all(line$`critic adjectives`, ',', ' ')
    )


  terms <- reactive({
    # Change when the "update" button is pressed...
    input$update
    # ...but not for anything else
    isolate({
      withProgress({
        setProgress(message = "Processing corpus...")
        getTermMatrix(input$selection)
      })
    })
  })

  # Make the wordcloud drawing predictable during a session
  wordcloud_rep <- repeatable(wordcloud)

  output$plot <- renderPlot({
    v <- terms()
    wordcloud_rep(names(v), v, scale=c(5, 0.5),
                  min.freq = input$freq, max.words=input$max,
                  colors=brewer.pal(8, "Accent"))
  })
}