library(shiny)
library(tidyverse)
library(plotly)

shinyServer(function(input, output, session) {

  output$trendPlot <- renderPlotly({

    if (length(input$name) == 0) {
      print("Please select at least one game")
    } else {



      df <- metafile[metafile$game == input$name, ] %>%
      	filter(score <= 100) %>% 
      	add_row(game = input$name, score = 100, type = 'critic') %>% 
      	add_row(game = input$name, score = 0, type = 'critic') %>% 
      	add_row(game = input$name, score = 10, type = 'user') %>% 
      	add_row(game = input$name, score = 0, type = 'user')

      p <- df %>%
        plot_ly(type = 'violin') %>%
        add_trace(
          x = ~game[df$type == 'critic'],
          y = ~score[df$type == 'critic'],
          legendgroup = 'Critic score',
          scalegroup = 'Critic score',
          name = 'Critic score',
          side = 'negative',
          scalemode = 'width',
          hoveron = 'points',
          bandwidth = 10,
          jitter = .1,
          spanmode =  'hard',
          box = list(
            visible = T,
            width = .5
          ),
          points = 'outliers',
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
          scalemode = 'width',
          hoveron = 'points',
          spanmode = 'hard',
          points = 'outliers',
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
        config(displayModeBar = F) %>% 
        layout(
          xaxis = list(
              title = ""  
          ),
          yaxis = list(
            title = "",
            zeroline = F,
            range = c(-10,119)
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