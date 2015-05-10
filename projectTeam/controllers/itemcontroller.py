# -*- coding: UTF-8 -*- 
from flask import Module,render_template,request,jsonify,g
from projectTeam.controllers.filters import login_filter
from projectTeam.services import itemservice
from projectTeam.models import Project

item = Module(__name__)
item.before_request(login_filter)

@item.route('/Item')
def index():
    return render_template('Item/List.html')
# 
@item.route('/Item/Create')
def create_item():
    return render_template('Item/Create.html')
@item.route('/CreateThemeItem',methods=['POST'])
def createNew_themeitem(): 
    itemservice.create_ThemeItem(request.json['ThemeItemName'],g.user_id)
    return jsonify(created=True)
@item.route('/CreateItem',methods=['POST'])
def createNew_item():
    SunItemfirst=request.json['Item']
    ThemeItemId= SunItemfirst['ThemeItemId']
    SunItemName= SunItemfirst['SunItemName']
    Description= SunItemfirst['Description']
    itemservice.create(ThemeItemId,SunItemName,Description,g.user_id)  
    
    try:
        SunItemList=request.json['SunItem']
        SunItemNameList= SunItemList['SunItemName']
        DescriptionList= SunItemList['Description']
        for i in range(0,len(SunItemNameList)):
            itemservice.create(ThemeItemId,SunItemNameList[i],DescriptionList[i],g.user_id)      
    except KeyError,e: 
        print "no sunitemlist"    
    return jsonify(created=True)

@item.route('/Item/Detail/<int:themeitem_id>')
def detailItem(themeitem_id):

    SunItem_list = itemservice.query_ThemeItem()

    return render_template('Item/Detail.html',ThemeItemId=themeitem_id,SunItemList=SunItem_list)


@item.route('/QueryThemeItem',methods=['POST'])
def query_ThemeItem():
    
    data = itemservice.query_ThemeItem()
    ThemeItem_list = []
    for i in data:
        ThemeItem_list.append({'ThemeItemId':i.ThemeItemId,'ThemeItemName':i.ThemeItemName})
    return jsonify(data=ThemeItem_list)

@item.route('/QueryItem',methods=['POST'])
def query_Item():
    item_list =[] 
    themeitemid=request.json['ThemeItemId']
    itemlist = itemservice.get(themeitemid)
    for i in itemlist:
        item_list.append({'SunItemName':i.SunItemName,'Description':i.Description})
    return jsonify(data=item_list)
# @requirement.route('/Requirement/Update',methods=['POST'])
# def update():
#     requirement_id = request.json['RequirementId']
#     requirement_name = request.json['RequirementName']
#     version =  request.json['Versions']
#     Description = request.json['Description']
#     status = request.json['Status']
#     requirementservice.update(requirement_id, requirement_name, version, status, Description, g.user_id)                
#     return jsonify(updated=True)


if __name__ == '__main__':  
    item.run(host="0.0.0.0",port=8080, debug=True) 
