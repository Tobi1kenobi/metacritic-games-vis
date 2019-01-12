function(input, output, session) {
  # Define a reactive expression for the document term matrix

  terms <- reactive({
    # Change when the "update" button is pressed...
#    input$update
    input$selection
    input$scoreType
    # ...but not for anything else
    isolate({
      withProgress({
        setProgress(message = "Processing corpus...")
        getTermMatrix(input$selection, input$scoreType)
      })
    })
  })

  # Make the wordcloud drawing predictable during a session
  wordcloud_rep <- repeatable(comparison.cloud)

  dinMor <- reactive({

    input$scoreType

    isolate({
      getScore(input$selection, input$scoreType)
      })
    })

    output$selected_var <- renderText({
      dinMor()
      })

  output$plot <- renderPlot({
    v <- terms()
#    wordcloud_rep(v, random.order=FALSE, scale=c(3.5, 0.35),
    wordcloud_rep(v, random.order=FALSE, scale=c(4, 0.4),
      colors = c("#aa44a0", "#7ec635", "#ffb500"), title.size=2.0,
      max.words=input$max, match.colors = FALSE, title.bg.colors = 'white')
  })
}

#colors = c("#ce5eff", "#5eff5e", "#ffb500")
#c("#cc0eb9", "#66e500", "#ffb500")