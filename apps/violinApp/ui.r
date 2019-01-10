library(shiny)
library(plotly)
library(tidyverse)
library(ggplot2)

shinyUI(fluidPage(

  # Application title
  titlePanel("Tesdt title"),

  sidebarPanel(
    h3("Ideal Points Estimation"),
    # Select Justices name here
    selectizeInput("name",
                   label = "Game Name(s) of Interest",
                   choices = unique(metafile$game),
                   multiple = T,
                   options = list(maxItems = 5, placeholder = 'Select a name'),
                   selected = "God of War (PS4)"),
    # Term plot
    plotOutput("termPlot", height = 20),
    helpText('generic help text')
  ),

  # Show a plot of the generated distribution
  mainPanel(
    plotlyOutput("trendPlot")
  )
)
)
