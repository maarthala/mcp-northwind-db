from mcp.server.fastmcp import FastMCP
import sqlite3
import os
import argparse

parser = argparse.ArgumentParser(description="My CLI App")
parser.add_argument('--db', type=str, help='add sqlite3 db path')
args = parser.parse_args()

class db():
    def __init__(self, db_path=None):

        db_path = args.db
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def total_expense(self, country=None):
        cur = self.conn.cursor()
        if country:
            cur.execute("SELECT SUM(Freight) as total FROM Invoices WHERE Country = ?", (country,))
        else:
            cur.execute("SELECT SUM(Freight) as total FROM Invoices")
        row = cur.fetchone()
        return row["total"] if row["total"] is not None else 0

    def list_countries(self):
        cur = self.conn.cursor()
        cur.execute("select distinct Country from Invoices")
        return [row["Country"] for row in cur.fetchall()]
    
    def find_matching_customer(self, name=None):
        cur = self.conn.cursor()
        if name:
            cur.execute("SELECT CustomerID,CompanyName, Address, Phone, Country FROM Customers WHERE CompanyName LIKE ?", (f"%{name}%",))
        else:
            cur.execute("SELECT CustomerID,CompanyName, Address, Phone, Country FROM Customers")
        return [
            {
            "CustomerID": row["CustomerID"],
            "CompanyName": row["CompanyName"],
            "Address": row["Address"],
            "Phone": row["Phone"],
            "Country" : row["Country"]
            }
            for row in cur.fetchall()
        ]

    def invoice_by_id(self, id=None):
        cur = self.conn.cursor()
        if id:
            id = int(id)
            cur.execute("SELECT CustomerID, CustomerName, Address, City, Country, OrderDate, ProductID FROM Invoices WHERE OrderID =  ?", (id,))
            return [
                {
                    "CustomerID": row["CustomerID"],
                    "CustomerName": row["CustomerName"],
                    "Address": row["Address"],
                    "City": row["City"],
                    "Country": row["Country"],
                    "OrderDate": row["OrderDate"],
                    "ProductID": row["ProductID"]
                }
                for row in cur.fetchall()
            ]
        return []

    def product_details(self, id=None):
        cur = self.conn.cursor()
        id = int(id)
        if id:
            cur.execute("SELECT ProductID, ProductName, SupplierID FROM Products WHERE ProductID =  ?", (id,))
            return [
                {
                    "ProductID": row["ProductID"],
                    "ProductName": row["ProductName"],
                    "SupplierID": row["SupplierID"]
                }
                for row in cur.fetchall()
            ]
        return []

    def order_subtotals(self, id=None):
        cur = self.conn.cursor()
        id = int(id)
        if id:
            cur.execute("SELECT Subtotal FROM 'Order Subtotals' WHERE OrderID =  ?", (id,))
            return [
                {
                    "OrderID": id,
                    "Subtotal": row["Subtotal"]
                }
                for row in cur.fetchall()
            ]
        return []
    
    def test_mcp(self):
        return os.getcwd()


mcp = FastMCP("northwind mcp")

@mcp.resource("resource://sqlite3")
def db_resource():
    return db()

@mcp.tool(description="test mcp")
def test_mcp():
    db_instance = db_resource()
    return db_instance.test_mcp()


@mcp.tool(description="find total expense or total expense by category")
def total_expense(country: str = None):
    db_instance = db_resource()
    """
    Find total expense or total expense by country
    :param country: country to filter by
    :param db: db resource (injected automatically)
    :return: total expense or total expense by country
    """
    return db_instance.total_expense(country)

@mcp.tool(description="find available countries")
def list_countries():
    db_instance = db_resource()
    """
    Find total expense by country
    :param db: db resource (injected automatically)
    :return: list of countries
    """
    return db_instance.list_countries()

@mcp.tool(description="find customer details")
def find_customers(name: str = None):
    db_instance = db_resource()
    """
    Find customer details
    :param db: db resource (injected automatically)
    :return: list of customers
    """
    return db_instance.find_matching_customer(name)


@mcp.tool(description="find order  details by id")
def find_invoice_by_id(id: str = None):
    db_instance = db_resource()
    """
    Find invoice  details by id
    :param OrderID: OrderID to filter by
    :param db: db resource (injected automatically)
    :return: summary of the invoice, if none return reply with  polite message
    """
    return db_instance.invoice_by_id(id)

@mcp.tool(description="find product  details by id")
def find_product_by_id(id: str = None):
    db_instance = db_resource()
    """
    Find product  details by id
    :param ProductID: ProductID to filter by
    :param db: db resource (injected automatically)
    :return: list of products with ProductID, ProductName, SupplierID
    """
    return db_instance.product_details(id)

@mcp.tool(description="find order subtotal by orderId")
def find_order_subtotal(id: str = None):
    db_instance = db_resource()
    """
    Find order  details by OrderId
    :param OrderID: OrderID to filter by
    :param db: db resource (injected automatically)
    :return: order  with OrderId, Subtotal
    """
    return db_instance.order_subtotals(id)

def runmcp():
    """Entry point for the MCP server when run as a script."""
    mcp.run()  # Default: uses STDIO transport

