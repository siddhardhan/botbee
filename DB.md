
https://learn.microsoft.com/en-us/azure/azure-sql/database/connect-query-python?view=azuresql

https://learn.microsoft.com/en-us/azure/azure-sql/database/single-database-create-quickstart?view=azuresql&tabs=azure-portal


```
CREATE TABLE Users (
    EMAIL_ID varchar(255) NOT NULL,
    ROLE varchar(25) NOT NULL,
    EXPERIENCE varchar(15) NOT NULL,
    LEVEL varchar(15) NOT NULL,
    PRIMARY KEY (EMAIL_ID)
);

INSERT INTO [dbo].[Users] VALUES ('a@a.com', 'Administrator', '6-12 months', 'Associate')

SELECT * FROM [dbo].[Users] WHERE EMAIL_ID='a@a.com'
```