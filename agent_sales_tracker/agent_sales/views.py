from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'agent_sales/index.html')

def pie_chart(request):
    #agents are labels
    labels = []
    data = []

    url = 'https://3066461-12-0-9f7b29.runbot49.odoo.com'
    db = '3066461-12-0-9f7b29-all'
    username = 'admin'
    password = 'admin'

    import xmlrpc.client
    import json

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid =common.authenticate(db,username,password, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    #need to add condition to check wheather user is a sales agent or not ['is_sales_agent', '=', True]
    agentid = models.execute_kw(db, uid, password,
        'res.users', 'search',[[]])

    salesagent = models.execute_kw(db, uid, password,
        'res.users', 'read',
        [agentid], {'fields': ['id', 'name']})

    for agent in salesagent:
        json_data = []
        for item in agentid:
            ordercount = models.execute_kw(db, uid, password,
            'sale.order', 'search_count',
            [[['user_id', '=', item]]])

            orderdetail = models.execute_kw(db, uid, password,
            'sale.order', 'search_read',
            [[['user_id', '=', item]]],
            {'fields': ['id', 'name','user_id']})
            if ordercount:
                json_data.append(({
                            'agent':orderdetail[0]['user_id'][1],
                            'count':ordercount,
            							}))

    for item in json_data:
        labels.append(item['agent'])
        data.append(item['count'])


    return render(request, 'agent_sales/pie_chart.html',{'labels': labels,
                                                'data': data,})
