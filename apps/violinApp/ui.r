library(shiny)
library(plotly)

shinyUI(fluidPage(

  # Application title
  titlePanel("Test title"),

  sidebarPanel(
    h3("Ideal Points Estimation"),
    # Select Justices name here
    selectizeInput("name",
                   label = "Game Name(s) of Interest",
                   choices = unique(metaresults$name),
                   multiple = T,
                   options = list(maxItems = 5, placeholder = 'Select a name'),
                   selected = "The Last of Us"),
    # Term plot
    plotOutput("termPlot", height = 200),
    helpText('generic help text')
  ),

  # Show a plot of the generated distribution
  mainPanel(
    plotlyOutput("trendPlot")
  )
)
)
