fluidPage(
  # Application title
  titlePanel("Word Cloud"),

  sidebarLayout(
    # Sidebar with a slider and selection inputs
    sidebarPanel(
      selectInput("selection", "Choose a game:",
                  choices = metafile$nameAndConsole),
      actionButton("update", "Change game"),
      hr(),
      actionButton("critic", "Critic reviews"),
      actionButton("user", "User reviews"),
      hr(),

      sliderInput("freq",
                  "Minimum Frequency:",
                  min = 1,  max = 50, value = 15),
      sliderInput("max",
                  "Maximum Number of Words:",
                  min = 1,  max = 300,  value = 100)
    ),

    # Show Word Cloud
    mainPanel(
      plotOutput("plot"),
      width = 18,
      height = 180
    )
  )
)