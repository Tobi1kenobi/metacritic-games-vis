library(rsconnect)
library(shiny)
library(shinyWidgets)
library(tidyverse)
library(memoise)
library(tm)
library(wordcloud)

fluidPage(
  # Application title
  titlePanel("Word cloud of loaded adjectives in game reviews"),

  sidebarLayout(
    # Sidebar with a slider and selection inputs
    sidebarPanel(
      selectInput("selection", "Choose a game:",
      	choices = metafile$nameAndConsole,
      	selected = 'Into the Breach (PC)'),

#      actionButton(input = "update", "Change game"),
      hr(),
#      selectInput('scoreType', 'Review Type',c('Critic', 'User')),
      awesomeRadio(inputId = "scoreType",
        label = "Generated based on:", choices = c("Critic reviews","User reviews"), selected = "Critic reviews"),
      hr(),
      sliderInput("max",
                  "Maximum Number of Words:",
                  min = 1,  max = 100,  value = 25)
    ),

    # Show Word Cloud
    mainPanel(
      htmlOutput('selected_var'),
      plotOutput("plot", height = '600px', width = '110%')

    )
  )
)