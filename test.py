import sys
import codecs
import json
import jsonschema

def generateError(): ## Генерирум файл ошибки и заканчиваем работу
    jsonDummy = json.loads(""" { "error": { "message": "Входные файлы некорректны" } } """)
    with open('error.json', 'wb') as f:
        json.dump(jsonDummy, codecs.getwriter('utf-8')(f), ensure_ascii=False,indent=4)
        sys.exit()
  
def getValuesFromFile(id):  ## Берем value из .json файла
 with open(valueFile,'rb') as vf:  
    try:
        d = json.load(vf)
    except ValueError:
        generateError()
    for val in d['values']:
        if int(val['id']) == id:   
            return val['value']

def getValueFromNextLevel(json,id):  ## Берем value из title
    for key in json['values']:
        if int(key['id']) == id:
            return key['title']

def checkValue(json,id):   ## Определяем откуда брать value
    temp = getValuesFromFile(id)
    if 'value' in json:
        if not (temp is None):
            if 'values' in json:
                nextLevelTitle = getValueFromNextLevel(json,temp)
                if not (nextLevelTitle is None):
                    json['value'] = nextLevelTitle
                    return
                else:
                    return  
        json['value'] = temp


def parseTestcase(jsonFile): ## Парсинг всех id в json
    checkValue(jsonFile,jsonFile['id'])
    if 'values' in jsonFile:        
        for key in jsonFile['values']:
            parseTestcase(key)
    if 'params' in jsonFile:
        for key in jsonFile['params']:
            parseTestcase(key)


if '.json' in sys.argv[1] and '.json' in sys.argv[2] :  ## Смотрим на входящие файлы
    valueFile = sys.argv[1]
    testcaseFile = sys.argv[2]
else:
    print('Invalid input files. Exapmle: test.py filewithValues.json testcasefile.json')
    sys.exit()
with open(testcaseFile,'rb') as f:   ## Принимаем файл теста
    try:
        d = json.load(f)
    except ValueError:
        generateError()
    for key in d['params']:
        parseTestcase(key)
    with open('data.json', 'wb') as f:
        json.dump(d, codecs.getwriter('utf-8')(f), ensure_ascii=False,indent=4)


