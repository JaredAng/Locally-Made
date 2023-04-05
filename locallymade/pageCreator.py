from dash import dcc,html,dash_table
import dash_bootstrap_components as dbc
import sqlite3 as sql
import dataGenerator as dataGen
import callbacks as call
from dash.dependencies import Input

main_layout = '''<!DOCTYPE html>
			<html>
				<head>
					{%metas%}
					<title>Locally Made</title>
					{%css%}
				</head>
				<body>
					{%app_entry%}
					<footer>
						{%config%}
						{%scripts%}
						{%renderer%}
					</footer>
					
				</body>
			</html>
		'''

pages=["Home","My Cart","Return Policy","Logout"]
navlinks=[]
items = []
username = ""

##Layouts
def createCard(data):
    return dbc.Col(
        dbc.Card(children=[   
            dbc.CardImg(src=data[4], top=True),
            dbc.CardBody([
                html.H4(data[1], className="card-title"),
                html.P(
                    data[2],
                    className="card-text",
                ),html.Hr(),
                dbc.Row(children=[
                    dbc.Col(dbc.Label(f"{data[3]:.02f} php",className = "card-title",id=f"price_{data[0]}")),
                    dbc.Col(dbc.Input(placeholder = "0", type='number',id=f"qty_{data[0]}", min=0)),
                    dbc.Col(dbc.Button("Add to Cart", color="primary", id=f"addtoCart_{data[0]}")),
                ]),
                
            ]),
        ],
        style={"width": "18rem"},
    )
)

def createCartCard(data):
    return dbc.Col(
        dbc.Card(children=[   
            dbc.CardImg(src=data[-1], top=True),
            dbc.CardBody([
                html.H4(data[1], className="card-title"),
                html.Hr(),
                dbc.Row(children=[
                    dbc.Col(dbc.Label(f"Price:{data[4]:.02f} php")),
                    dbc.Col(dbc.Label(f"Qty: {data[3]}" )),
                    dbc.Col(dbc.Label(f"Total: {data[-3]:.02f} php")),
                    
                ]),
                
            ]),
        ],
        style={"width": "18rem"},
        )
    ) 
    
def catalog(page):
    cards = []
    global username
    print(username)
    if page == "home":
        data = dataGen.getCard_Catdata()
        for item in data:
            cards.append(createCard(item))
    elif page == "cart":
        data = dataGen.getCard_Cartdata()
        for item in data:
            cards.append(createCartCard(item))
    
    return cards
    

for i in pages:
    navlinks.append(dbc.NavLink(i.upper(),href=f"/locallymade/{i.replace(' ', '').lower()}/", id=i.replace(' ', '').lower())) 

navbar = dbc.NavbarSimple(
        children=navlinks,
        id="navbar",
        brand="Locally Made",
        brand_href=f"/locallymade/home/",
        color="rgb(255,255,255)",
        dark=False,sticky="top"
)


home_page = dbc.Container(id="home_page",children=[
    html.Br(),
    dbc.Row([
        dbc.InputGroup([
            dbc.Row([
                dbc.Col(dbc.Input(placeholder="Search Item", id="Sitem")),
                dbc.Col(dbc.Input(placeholder="Item Price (max)", id="SPriceMax",type="number")),
                dbc.Col(dbc.Input(placeholder="Item Price (min)", id="SPriceMin",type="number")),
                dbc.Col(dbc.Button("Search",id="searchBtn"))
            ])
            
        ])
    ]),
    html.Br(),
    dbc.Row(children=catalog("home"),id="catalog")
])

signup_page = dbc.Card(id="signup_page",children=[
    dbc.CardHeader(html.H2("Signup")),
    dbc.CardBody(
        dbc.Form(children=[
            dbc.Row(
                dbc.Col([
                    dbc.FormText("Username"),
                    dbc.Input(id="unameSign", type = "text")
                ])
            ),
            dbc.Row(
                dbc.Col([
                    dbc.FormText("Email"),
                    dbc.Input(id="emailSign", type = "email")
                ])
            ),
            dbc.Row(
                dbc.Col([
                    dbc.FormText("Password"),
                    dbc.Input(id="pwdSign1", type = "text")
                ])
            )
        ]),
    ),
    dbc.CardFooter(
            dbc.Row([
                dbc.Col(
                    dbc.ButtonGroup(children=[
                        dbc.Button("Signup", type="link", id="signupBtn"),
                        dbc.Button("Login", type="link", href="/locallymade/")
                    ])
                )
            ])
    )
])

login_page = dbc.Card(id="login_page",children=[
    dbc.CardHeader(html.H2("Login")),
    dbc.CardBody(
        dbc.Form(children=[
            dbc.Row([
                dbc.Col(dbc.Input(id="uname", placeholder = "Username", type = "text")),
                dbc.Col(dbc.Input(id="pwd", placeholder = "Password", type = "password")),
        ]),
           html.Br(), 
            dbc.Row([
                dbc.Col(dbc.ButtonGroup(children=[
                    dbc.Button("Login", type="submit", id="loginBtn"),
                    dbc.Button("Signup", color = "link", href="/locallymade/signup")
                ]))
            ]),
        ])
    )
])

mycart_page = dbc.Container(children=[
    html.Br(),
    dbc.Row([
        dbc.InputGroup([
            dbc.Row([
                dbc.Col(dbc.Input(placeholder="Search Item", id="Sitem")),
                dbc.Col(dbc.Input(placeholder="Item Price (max)", id="SPriceMax",type="number")),
                dbc.Col(dbc.Input(placeholder="Item Price (min)", id="SPriceMin",type="number")),
                dbc.Col(dbc.Button("Search",id="searchBtn"))
            ])
            
        ])
    ]),
    html.Br(),
    dbc.Row(children=catalog("cart"),id="Cartcatalog")
], id="cart")

returnpolicy_page = dbc.Container(id="returnpolicy_page",children=[
    html.Br(),
    dbc.ModalTitle("Refund Policy for Physical Products"),
    dbc.Card(
        dbc.CardBody(
            html.P("""
                   Thanks for purchasing our products sold from Locally Made Website.
In order to be eligible for a refund, you have to return the product within 30 calendar days of your purchase. The product must be in the same condition that you receive it and undamaged in any way.
After we receive your item, our team of professionals will inspect it and process your refund. The money will be refunded to the original payment method you've used during the purchase. For credit card payments it may take 5 to 10 business days for a refund to show up on your credit card statement.
If the product is damaged in any way, or you have initiated the return after 30 calendar days have passed, you will not be eligible for a refund. 
If anything is unclear or you have more questions feel free to contact our customer support team.""", className='card-text'
        
    )))
])
