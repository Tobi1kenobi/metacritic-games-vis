shinyServer(function(input, output, session) {

  output$trendPlot <- renderPlotly({

    if (length(input$name) == 0) {
      print("Please select at least one game")
    } else {
      df <- metaresults[metaresults$name == input$name, ]
      

      p <- df %>%
        plot_ly(type = 'violin') %>%
        add_trace(
          x = ~name[df$type == 'meta'],
          y = ~score[df$type == 'meta'],
          legendgroup = 'Metascore',
          scalegroup = 'Metascore',
          name = 'Metascore',
          side = 'negative',
          box = list(
            visible = T
          ),
          meanline = list(
            visible = T
          ),
          line = list(
            color = 'blue'
          )
        ) %>%
        add_trace(
          x = ~name[df$type == 'user'],
          y = ~score[df$type == 'user'],
          legendgroup = 'Userscore',
          scalegroup = 'Userscore',
          name = 'Userscore',
          side = 'positive',
          box = list(
            visible = T
          ),
          meanline = list(
            visible = T
          ),
          line = list(
            color = 'green'
          )
        ) %>% 
        layout(
          xaxis = list(
              title = ""  
          ),
          yaxis = list(
            title = "",
            zeroline = F
          ),
          violingap = 0,
          violingroupgap = 0,
          violinmode = 'overlay'
        )
      p





#      ggplot(df_trend, aes(x = name, y = userscore, color = name)) +
#        geom_violin() +
#        labs(x = "metascore", y = "Userscore", title = "Ideal Points for din mor") +
#        scale_colour_hue("clarity", l = 70, c = 150) + ggthemes::theme_few()

    }

  })
})
