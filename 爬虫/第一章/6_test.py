import openpyxl
import json
import codecs


if __name__ == '__main__':
    # 打开工作簿
    wb = openpyxl.load_workbook('latlng.xlsx')

    # 选择工作表，默认选择第一个工作表
    ws = wb.active

    # 读取数据
    data = []
    for row in ws.iter_rows(values_only=True):
        # print(row.index((0,)))
        data.append(row)

    result = []
    # 打印数据 区号唯一区分
    for row in data[3:]:
        if row[6] is None:
            continue
        tem_full_name = str(row[4])
        ele = [item for item in result if item['full_name'] in tem_full_name]
        if ele:
            #下辖区县
            child_city_dict = {
                'area_id': row[0],
                'area_name': row[2],
                'area_lng': row[8],
                'area_lat': row[9],
                'area_full_name': row[4]
            }
            ele[0]['areas'].append(child_city_dict)
        else:
            tem_data = {
                'id': row[0],
                'city': row[2],
                'lng': row[8],
                'lat': row[9],
                'city_code': row[6],
                'full_name': row[4],
                'areas': []
            }
            result.append(tem_data)



    # 将JSON字符串列表写入文件
    # fp = codecs.open('output.json', 'a+', 'utf-8')
    # fp.write(json.dumps(result,ensure_ascii=False))
    # fp.close()
    # with open('output.json', 'w') as f:
    #     json.dump(result,f,ensure_ascii=False)


    # 关闭工作簿
    wb.close()
    user_input = input('请输入')
    print(user_input)
    res = [item for item in result if user_input in item['city']]
    print(res)
