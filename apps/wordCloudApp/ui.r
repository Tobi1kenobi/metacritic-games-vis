fluidPage(
  # Application title
  titlePanel("Word Cloud of loaded adjectivs in game reviews"),

  sidebarLayout(
    # Sidebar with a slider and selection inputs
    sidebarPanel(
      selectInput("selection", "Choose a game:",
                  choices = metafile$nameAndConsole),
#      actionButton(input = "update", "Change game"),
      hr(),
#      selectInput('scoreType', 'Review Type',c('Critic', 'User')),
      awesomeRadio(inputId = "scoreType",
        label = "Score", choices = c("Critic","User"), selected = "Critic"),
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