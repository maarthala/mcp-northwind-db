# mcp-northwind-db
A demo MCP server  to integrate with sqlite3 northwind database.


# How it works

Python Version : `Python 3.12.4`

Clone this repo

from `<repo-root>` run


````
pip install .
````

open `.vscode/mcp.json` and click on `start` on the mcp server config.


open visual code "open chat" editor

Select Agent in the chat editor

ask  context based on the northwind db data. Following tables are used in the context
- invoices
- orders
- order totals
- customers
- products

# Sample questions

```
find the invoice details using order 10249 and associated product information along with order total.
``` 

```
phone number of Bottom-Dollar
```


```
list available countries
```

```
count number of customers present in each country ?
```

```
what products are in order 10249
```
