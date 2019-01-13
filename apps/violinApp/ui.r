shinyUI(fluidPage(

  # Application title
  titlePanel("Distribution of game scores"),

  sidebarPanel(
    # Select Justices name here
    selectizeInput("name",
                   label = "Choose a game:",
                   choices = unique(metafile$game),
                   multiple = T,
                   options = list(maxItems = 5, placeholder = 'Select a name'),
                   selected = c('BioShock (PC)', 'BioShock 2 (PC)')),
    # Term plot
    plotOutput("termPlot", height = 20)
  ),

  # Show a plot of the generated distribution
  mainPanel(
    plotlyOutput("trendPlot")
  )
)
)
