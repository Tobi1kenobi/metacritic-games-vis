shinyServer(function(input, output, session) {

  output$trendPlot <- renderPlotly({

    if (length(input$name) == 0) {
      print("Please select at least one game")
    } else {



      df <- metafile[metafile$game == input$name, ] %>%
      	filter(score <= 100)

      p <- df %>%
        plot_ly(type = 'violin') %>%
        add_trace(
          x = ~game[df$type == 'critic'],
          y = ~score[df$type == 'critic'],
          legendgroup = 'Critic score',
          scalegroup = 'Critic score',
          name = 'Critic score',
          side = 'negative',
          scalemode = 'count',
          hoveron = 'kde',
          bandwidth = 10,
          jitter = .1,
          spanmode = 'manual',
          span = list(c(0,100)),
          box = list(
            visible = T,
            width = .5
          ),
          points = 'all',
          pointpos = -.5,
          meanline = list(
            visible = T
          ),
          line = list(
            color = '#ffd263',
            outliercolor = '#ff0000'
          ),
          marker = list(
          	color = '#8e7537',
          	outliercolor = '#ff0000',
          	opacity = 0.25
          )
        ) %>%
        add_trace(
          x = ~game[df$type == 'user'],
          y = ~score[df$type == 'user']*10,
          legendgroup = 'User score',
          scalegroup = 'User score',
          name = 'User score',
          side = 'positive',
          scalemode = 'count',
          hoveron = 'kde',
          spanmode = 'manual',
          span = list(c(0,100)),
          points = 'all',
          box = list(
            visible = T,
            width = .5
          ),
          pointpos = .5,
          bandwidth = 10,
          jitter = .1,
          meanline = list(
            visible = T
          ),
          line = list(
            color = '#62d5ff',
            outliercolor = '#ff0000'
          ),
          marker = list(
          	color = '#408eaa',
          	outliercolor = '#ff0000',
          	opacity = 0.25
          )
        ) %>% 
        layout(
          xaxis = list(
              title = ""  
          ),
          yaxis = list(
            title = "",
            zeroline = F,
            range = c(0,120)
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