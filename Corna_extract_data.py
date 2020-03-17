#!/usr/bin/env python
# coding: utf-8

# In[262]:


import datetime
import json
import requests
import ast
import pandas as pd
import re
import geojson




url = "https://services5.arcgis.com/dlrDjz89gx9qyfev/arcgis/rest/services/Corona_Exposure_View/FeatureServer/0/query"

querystring = {"f":"json","where":"1=1","returnGeometry":"true","spatialRel":"esriSpatialRelIntersects","geometryType":"esriGeometryEnvelope","outFields":"*"}

payload = ""
headers = {
    'Accept': "application/jsonx",
    'cache-control': "no-cache",
    'Postman-Token': "18ac27ab-e0b0-4579-b81e-fd82d914acc5"
    }

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)


data = response.json()




d=[]
for i in data['features']:
    row = {**i['attributes'], **i['geometry']}
    d.append(row)
    
df= pd.DataFrame(d)




def POItype(s):
    if re.search("קפה", s):
        return ("בית קפה")
    elif  re.search("קלפי", s):
        return ("קלפי")
    elif  re.search("ישרוטל|מלון", s):
        return ("בית מלון")
    elif  re.search("בית הכנסת|בית כנסת", s):
        return ("בית כנסת")
    elif  re.search("כללית |מרפאה |מוקד|מרפאת|קופת ", s):
        return ("מרפאה")
    elif  re.search("באגט|גריל |מקדונלדס |פיצה|מסעדה |מסעדת", s):
        return ("מסעדה")
    elif  re.search("ויקטורי |2000|מכלת |ברכול |רמי לוי|אושר עד|סופרמרקט|סופר |שופר סל", s):
        return ("סופרמרקט")
    elif  re.search("מרכז רפואי|מרכז הרפואי|ביח|שיבא|בלינסון|בית חולים|בית החולים", s):
        return ("בית חולים")
    elif  re.search("בית הספר|ישיבה |בית ספר", s):
        return ("בית ספר")
    elif  re.search("קניון", s):
        return ("קניון")
    elif  re.search("בנק", s):
        return ("בנק")
    elif  re.search("בזאר |מקס|מספרה|מקסטוק|ביג|חנות", s):
        return ("מסחר")
    elif  re.search("סינמה סיטי|קולנוע", s):
        return ("קולנוע")
    elif  re.search("אצטדיון ", s):
        return ("אצטדיון")
    elif  re.search("כנסית |כנסיה|כנסיית|מוריסטן", s):
        return ("מבנה דת נוצרי")
    elif  re.search("תיאטרון ", s):
        return ("תיאטרון")
    elif  re.search("יד ושם|הרודיון|קיסריה|מנהרות הכותל|הורודיון|קאסר|מצדה", s):
        return ("אתר תיירות")
    elif  re.search("מכללת |אוניברסיטת", s):
        return ("אוניברסיטה")
    elif  re.search("אולמי |מועדון |אולם", s):
        return ("אירועים")





df["type"]=df.apply(lambda x: POItype(x.Place), axis=1)





def data2geojson(df):
    features = []
    insert_features = lambda X: features.append(
            geojson.Feature(geometry=geojson.Point((X["x"],X["y"],)),
                            properties=dict(name=X["Name"],Place=X["Place"],Comments=X["Comments"],type=X["type"])))
    df.apply(insert_features, axis=1)
    with open(r"data\israel_coronatracker.geojson", 'w', encoding='utf8') as fp:
        geojson.dump(geojson.FeatureCollection(features), fp, sort_keys=True, ensure_ascii=False)



data2geojson(df)

