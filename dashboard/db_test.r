#install.packages("RMariaDB")
#install.packages("shinydashboard")
#install.packages("config")
#install.packages("odbc")

library(DBI)

conn_args <- config::get("dataconnection")
con <- dbConnect(
  odbc::odbc(),
  Driver = conn_args$driver,
  Server = conn_args$server,
  UID    = conn_args$uid,
  PWD    = conn_args$pwd,
  Port   = conn_args$port,
  Database = conn_args$database
)

res <- dbSendQuery(con, "SELECT * FROM event")
while(!dbHasCompleted(res)){
  chunk <- dbFetch(res, n = 5)
  print(chunk)
}
dbClearResult(res)
dbDisconnect(con)
