backup_dataframe <- function(df, filename, inc=50000){
  require(xlsx)
  
  length <- nrow(df)
  row_cursor <- 1
  file_cursor <- 1
  
  for(i in seq(1, length, by=inc)){

    if(i+inc-1<length){
      # write.xlsx2(x=df[i:(i+inc-1),], 
      #             file=paste(filename, "_", file_cursor, ".xlsx", sep=""),
      #             row.names=F)
      write.csv2(x=df[i:(i+inc-1),], 
                  file=paste(filename, "_", file_cursor, ".csv", sep=""),
                  row.names=F)
    }
    
    else if(i+inc-1>=length){
      # write.xlsx2(x=df[i:length,], 
      #             file=paste(filename, "_", file_cursor, ".xlsx", sep=""),
      #             row.names=F)
      write.csv2(x=df[i:(i+inc-1),], 
                 file=paste(filename, "_", file_cursor, ".csv", sep=""),
                 row.names=F)
    }
    
    file_cursor <- file_cursor + 1
    
  }
  
}


# test_df <- data.frame(
#   col1 = 1:45,
#   col2 = 2:46,
#   col3 = 3:47
# )
# 
# backup_dataframe(test_df, "../thisisatest")

#backup_dataframe(data.text.official.covid.all %>% mutate(date.time=paste(date.time)), "DF_Backup/covidtwitter_2_3_22_backup")
