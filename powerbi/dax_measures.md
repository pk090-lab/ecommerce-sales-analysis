# Power BI DAX Measures

Assume the imported table is named `Sales`. Create these measures using **Modeling → New measure**.

```dax
Total Revenue =
SUM ( Sales[revenue] )

Total Orders =
DISTINCTCOUNT ( Sales[invoice_no] )

Units Sold =
SUM ( Sales[quantity] )

Known Customers =
CALCULATE (
    DISTINCTCOUNT ( Sales[customer_id] ),
    FILTER ( Sales, NOT ISBLANK ( Sales[customer_id] ) )
)

Average Order Value =
DIVIDE ( [Total Revenue], [Total Orders] )

Revenue per Known Customer =
DIVIDE ( [Total Revenue], [Known Customers] )

Revenue per Unit =
DIVIDE ( [Total Revenue], [Units Sold] )

Repeat Customers =
COUNTROWS (
    FILTER (
        VALUES ( Sales[customer_id] ),
        NOT ISBLANK ( Sales[customer_id] )
            && CALCULATE ( DISTINCTCOUNT ( Sales[invoice_no] ) ) > 1
    )
)

Repeat Customer Rate =
DIVIDE ( [Repeat Customers], [Known Customers] )
```

## Date table (recommended)

Create a date table to support time intelligence:

```dax
Date =
CALENDAR (
    MIN ( Sales[InvoiceDate_Date] ),
    MAX ( Sales[InvoiceDate_Date] )
)
```

Before using this, create a date-only column in Power Query or DAX. For example:

```dax
InvoiceDate_Date =
DATE (
    YEAR ( Sales[invoice_date] ),
    MONTH ( Sales[invoice_date] ),
    DAY ( Sales[invoice_date] )
)
```

Then create a relationship from `Date[Date]` to `Sales[InvoiceDate_Date]` and mark `Date` as the date table.

```dax
Revenue Previous Month =
CALCULATE ( [Total Revenue], DATEADD ( 'Date'[Date], -1, MONTH ) )

Revenue MoM Change % =
DIVIDE (
    [Total Revenue] - [Revenue Previous Month],
    [Revenue Previous Month]
)

Revenue YTD =
TOTALYTD ( [Total Revenue], 'Date'[Date] )
```

Format revenue and AOV as currency, and rate measures as percentages.

**Important:** The source dataset does not contain product cost, so do not label revenue as profit or calculate a profit margin.
