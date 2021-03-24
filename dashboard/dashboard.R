library(shinydashboard)

ui <- dashboardPage(
  dashboardHeader(title = "Basic dashboard"),
  dashboardSidebar(),
  dashboardBody(
    # Boxes need to be put in a row (or column)
    fluidRow(
      box(plotOutput("plot1", height = 250)),
      
      box(
        title = "Controls",
        sliderInput("slider", "Number of observations:", 1, 100, 50),
        numericInput("refresh", h3("Numeric input"), value = 4)   
      )
    )
  )
)

server <- function(input, output, session) {
  #set.seed(122)
  
  x = 4
  
  histdata <- reactivePoll(x*1000, session,
    checkFunc = function() {
      rnorm(1)
    },
    valueFunc = function() {
      rnorm(500)
    }
  )
  
  output$plot1 <- renderPlot({
    data <- histdata()[seq_len(input$slider)]
    x <- input$refresh
    hist(data)
  })

}

shinyApp(ui, server)