from dash.exceptions import PreventUpdate
from dash.dependencies import Input,Output,State
import pageCreator as pages
from dash import dcc,html,dash_table
import dash_bootstrap_components as dbc,dash
import dataGenerator as sql, traceback

global username
username,path,path2= 'a',f'/locallymade/home/',f'/locallymade/mycart/'

def get_username():
    return username

def callbacks(app):
    ### Pages Callback###
    @app.callback(
        [Output('body', 'children', allow_duplicate=True),Output("home",'href'),Output("mycart",'href')], 
        [Input('url', 'pathname')],
        prevent_initial_call=True
    )## output(id,what to touch) input(from, data)
    def display_page(pathname):
        global username 
        username = pathname.split('/')[-1]
        pages.username = username
        path=f'/locallymade/home/{username}'
        path2=f'/locallymade/mycart/{username}'
        if pathname=='/' or pathname == '/locallymade/' or "logout" in pathname:
            return pages.login_page,'/locallymade/','/locallymade/'
        if '/locallymade/home/' in pathname:
            return pages.home_page, path, path2
        elif '/locallymade/login' in pathname:
            return pages.login_page,'/locallymade/','/locallymade/'
        elif '/locallymade/signup' in pathname:
            return pages.signup_page,'/locallymade/signup','/locallymade/signup'
        elif '/locallymade/mycart/' in pathname:
            return pages.mycart_page, path, path2
        elif '/locallymade/about/' in pathname:
            return pages.about_page, path, path2
        elif '/locallymade/returnpolicy/' in pathname:
            return pages.returnpolicy_page, path, path2
        else:
            return 'Error 404: Page not Found...'
    ### Pages Callback###        
    
    @app.callback(
        Output("url", "pathname", allow_duplicate=True),
        [Input("loginBtn", "n_clicks"),Input("uname", "value"),Input("pwd", "value")],
        prevent_initial_call=True
    )
    def login(btn, uname, pwd):
        inputs = dash.callback_context
        if inputs.triggered[0]['prop_id'] == '.' and btn == None:
            raise PreventUpdate()
        elif inputs.triggered[0]['prop_id'] == 'loginBtn.n_clicks' and btn!=0:
            if uname!='' and pwd !='':
                if sql.get_login(uname, pwd) != None:
                    username = uname
                    return f"/locallymade/home/{uname}"
            return f"/"
        else:
            raise PreventUpdate()
                
    
    @app.callback(
        [Output('url', 'pathname', allow_duplicate=True),Output('body', 'children')],
        [Input("signupBtn", "n_clicks"),Input("pwdSign1", "value"),
         Input("unameSign", "value"),Input("emailSign", "value")],
        prevent_initial_call=True
    )
    def signup(btn,pwd1,uname,email):
        inputs=dash.callback_context
        data = ''
        if inputs.triggered[0]['prop_id'] == '.' and btn == None:
            raise PreventUpdate()
        elif inputs.triggered[0]['prop_id'] == 'signupBtn.n_clicks':
            if pwd1!='' and uname !='' and email !='':                
                ssq = f"insert into usrTbl (uname,upwd,email) values (\"{uname}\",\"{pwd1}\",\"{email}\");"
                data = f"/locallymade/home/{uname}"
                username=uname
                sql.insertData("usrTbl", "uname,upwd,email" ,f"\"{uname}\",\"{pwd1}\",\"{email}\"")
            return data,pages.home_page
        else:
            raise PreventUpdate()
    
    @app.callback(
            [Output("catalog", 'children')],
            [Input('searchBtn', 'n_clicks'),Input('Sitem','value'),
             Input('SPriceMax','value'),Input('SPriceMin','value')])
    def searchItem(clicks,item,maxP,minP):
        inputs=dash.callback_context
        cards=[]
        if inputs.triggered[0]['prop_id'] == '.' and clicks == None and item == None and maxP == None and minP == None :
            raise PreventUpdate()
        elif inputs.triggered[0]['prop_id'] == 'searchBtn.n_clicks':
            if maxP == None and minP == None: 
                data = sql.getCard_data(f" select * from catalogTbl where itemName like \"%{item}%\";")
            elif item == None and minP == None: 
                data = sql.getCard_data(f" select * from catalogTbl where itemPrice<={maxP};")
            elif item == None and maxP == None: 
                data = sql.getCard_data(f" select * from catalogTbl where itemPrice<={minP};")
            elif item == None: 
                data = sql.getCard_data(f" select * from catalogTbl where itemPrice>={minP} and itemPrice<={maxP};")
            else:
                data = sql.getCard_data(f" select * from catalogTbl where itemName like \"%{item}%\" or itemPrice>={minP} and itemPrice<={maxP};")
            for item in data:
                cards.append(pages.createCard(item))
            return [cards]
        else:
            raise PreventUpdate()
    
    @app.callback(Output('url','pathname'),
                  [Input("url",'pathname'),
                   Input("qty_1","value"),Input("addtoCart_1","n_clicks"),
                   Input("qty_2","value"),Input("addtoCart_2","n_clicks"),
                   Input("qty_3","value"),Input("addtoCart_3","n_clicks"),
                   Input("qty_4","value"),Input("addtoCart_4","n_clicks"),
                   Input("qty_5","value"),Input("addtoCart_5","n_clicks"),
                   Input("qty_6","value"),Input("addtoCart_6","n_clicks"),
                   Input("qty_7","value"),Input("addtoCart_7","n_clicks"),
                   Input("qty_8","value"),Input("addtoCart_8","n_clicks")])
    
    def insertCart(url, qty, btn, qty2,btn2,qty3,btn3,qty4,btn4,qty5,btn5,qty6,btn6,qty7,btn7,qty8,btn8):
        global username
        inputs = dash.callback_context
        price,total = 0,0
        if inputs.triggered[0]['prop_id'] == '.' and price!= None and qty == 0 and btn == 0:
            raise PreventUpdate()
        elif inputs.triggered[0]['prop_id'] == 'addtoCart_1.n_clicks' and btn != None and qty != None:
            price = sql.getCard_data("select * from catalogTbl where itemID = 1;")[0]
            total = price[3]*qty
            sql.insertData("cartTbl", "itemID, uname,itemName, itemPrice,itemQty,itemTotal", f"1,\"{username}\",\"{price[1]}\",{price[3]},{qty2},{total}")
            return url
        elif inputs.triggered[0]['prop_id'] == 'addtoCart_2.n_clicks' and btn2 != None and qty2 != None:
            price = sql.getCard_data("select * from catalogTbl where itemID = 2;")[0]
            total = price[3]*qty2
            sql.insertData("cartTbl", "itemID, uname,itemName, itemPrice,itemQty,itemTotal", f"2,\"{username}\",\"{price[1]}\",{price[3]},{qty3},{total}")
            return url
        elif inputs.triggered[0]['prop_id'] == 'addtoCart_3.n_clicks' and btn3 != None and qty3 != None:
            price = sql.getCard_data("select * from catalogTbl where itemID = 3;")[0]
            total = price[3]*qty3
            sql.insertData("cartTbl", "itemID, uname,itemName, itemPrice,itemQty,itemTotal", f"3,\"{username}\",\"{price[1]}\",{price[3]},{qty3},{total}")
            return url
        elif inputs.triggered[0]['prop_id'] == 'addtoCart_4.n_clicks' and btn4 != None and qty4 != None:
            price = sql.getCard_data("select * from catalogTbl where itemID = 4;")[0]
            total = price[3]*qty4
            sql.insertData("cartTbl", "itemID, uname,itemName, itemPrice,itemQty,itemTotal", f"4,\"{username}\",\"{price[1]}\",{price[3]},{qty4},{total}")
            return url
        elif inputs.triggered[0]['prop_id'] == 'addtoCart_5.n_clicks' and btn5 != None and qty5 != None:
            price = sql.getCard_data("select * from catalogTbl where itemID = 5;")[0]
            total = price[3]*qty5
            sql.insertData("cartTbl", "itemID, uname,itemName, itemPrice,itemQty,itemTotal", f"5,\"{username}\",\"{price[1]}\",{price[3]},{qty5},{total}")
            return url
        elif inputs.triggered[0]['prop_id'] == 'addtoCart_6.n_clicks' and btn6 != None and qty6 != None:
            price = sql.getCard_data("select * from catalogTbl where itemID = 6;")[0]
            total = price[3]*qty6
            sql.insertData("cartTbl", "itemID, uname,itemName, itemPrice,itemQty,itemTotal", f"6,\"{username}\",\"{price[1]}\",{price[3]},{qty6},{total}")
            return url
        elif inputs.triggered[0]['prop_id'] == 'addtoCart_7.n_clicks' and btn7 != None and qty7 != None:
            price = sql.getCard_data("select * from catalogTbl where itemID = 7;")[0]
            total = price[3]*qty7
            sql.insertData("cartTbl", "itemID, uname,itemName, itemPrice,itemQty,itemTotal", f"7,\"{username}\",\"{price[1]}\",{price[3]},{qty7},{total}")
            return url
        elif inputs.triggered[0]['prop_id'] == 'addtoCart_8.n_clicks' and btn8 != None and qty8 != None:
            price = sql.getCard_data("select * from catalogTbl where itemID = 8;")[0]
            total = price[3]*qty8
            sql.insertData("cartTbl", "itemID, uname,itemName, itemPrice,itemQty,itemTotal", f"8,\"{username}\",\"{price[1]}\",{price[3]},{qty8},{total}")
            return url
        else:
            raise PreventUpdate()
    