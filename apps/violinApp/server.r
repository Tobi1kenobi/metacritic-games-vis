shinyServer(function(input, output, session) {

  output$trendPlot <- renderPlotly({

    if (length(input$name) == 0) {
      print("Please select at least one game")
    } else {



      df <- metafile[metafile$game == input$name, ]

      p <- df %>%
        plot_ly(type = 'violin') %>%
        add_trace(
          x = ~game[df$type == 'critic'],
          y = ~score[df$type == 'critic'],
          legendgroup = 'Critic score',
          scalegroup = 'Critic score',
          name = 'Critic score',
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
          x = ~game[df$type == 'user'],
          y = ~score[df$type == 'user']*10,
          legendgroup = 'User score',
          scalegroup = 'User score',
          name = 'User score',
          side = 'positive',
          box = list(
            visible = T
          ),
          bandwidth = 1,
          jitter = 0,
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
#          violinmode = 'overlay'
        )
      p
    }

  })
})