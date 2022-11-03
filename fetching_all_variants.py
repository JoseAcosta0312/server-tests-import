from flask import Flask,jsonify,request,Response
from products_file import products, products_persist
from os import remove
import json

app = Flask(__name__)
    
def find_product_by_id(id_product):
    index = 0
    for product in products:
        is_product = product['product']['id']
        if is_product == int(id_product):
            return {"variants" : product['product']['variants'], "index" : index}
        index += 1
    return Response(response='NOT FOUND',status=404) 

@app.route("/<id_product>/variants",methods=['GET'])
def get_all_variants_for_product(id_product):
    return jsonify(find_product_by_id(id_product)['variants'])

@app.route("/<id_product>/<sku_variant>",methods=['PUT'])
def update_variant(id_product,sku_variant):
    variants = find_product_by_id(int(id_product))
    data = request.json
    for variant in variants['variants']:
        index_variant = 0
        if variant['sku'] == sku_variant:
            new_variant = {
                'id': variant['id'],
                'position': data['position'] if 'position' in data  else variant['position'],
                'price' : data['price'] if 'price' in data else variant['price'],
                'sku' : variant['sku'],
                'barcode' : data['barcode'] if 'sku' in data else variant['barcode'],
                'stock' : data['stock'] if 'stock' in data else variant['stock'],
                'stock_unlimited' : data['stock_unlimited'] if 'stock_unlimited' in data else variant['stock_unlimited'],
                'weight' : data['weight'] if 'weight' in data else variant['weight'],
                'options' : [
                    {
                        "product_option_id": variant['options'][0]['product_option_id'],
                        "product_option_value_id": variant['options'][0]['product_option_value_id'],
                        "name": "Color",
                        "value": data['options'][0]['value'] if 'value' in data['options'][0] else variant['options'][0]['value'],
                        "custom": data['options'][0]['custom'] if 'custom' in data['options'][0] else variant['options'][0]['custom'],
                        "product_option_position": data['options'][0]['product_option_position'] if 'product_option_position' in data['options'][0] else variant['options'][0]['product_option_position'],
                        "product_value_position": data['options'][0]['product_value_position'] if 'product_value_position' in data['options'][0] else variant['options'][0]['product_value_position']
                    },
                    {
                        "product_option_id": variant['options'][1]['product_option_id'],
                        "product_option_value_id": variant['options'][1]['product_option_value_id'],
                        "name": 'Tipo de Entrega',
                        "value": data['options'][1]['value'] if 'value' in variant['options'][1] else variant['options'][1]['value'],
                        "custom": data['options'][1]['custom'] if 'custom' in variant['options'][1] else variant['options'][1]['custom'],
                        "product_option_position": data['options'][1]['product_option_position'] if 'product_option_position' in variant['options'][1] else variant['options'][1]['product_option_position'],
                        "product_value_position": data['options'][1]['product_value_position'] if 'product_value_position' in variant['options'][1] else variant['options'][1]['product_value_position']
                    }
                ],
                "image": {
                    "id": variant['image']['id'],
                    "position": variant['image']['position'],
                    "url": variant['image']['url']
                },
                "discount": data['discount'] if 'discount' in data  else variant['discount']
            }
            products[variants['index']]['product']['variants'][index_variant] = new_variant
            remove('products.json')
            with open('products.json','w') as json_file:
                json.dump(products,json_file)   
            return products[variants['index']]['product']['variants'][index_variant]
        index_variant += 1 
            
    return Response(response='NOT FOUND',status=404) 

@app.route('/reset',methods=['GET'])
def reset_products(): 
    remove('products.json')
    with open('products.json','w') as json_file:
        json.dump(json.loads(json.dumps(products_persist)),json_file)
    return jsonify({'message':'json reseteado'})

@app.route("/<id_product>/<sku_variant>",methods=['GET'])
def single_variant(id_product,sku_variant):
    product = find_product_by_id(id_product)
    for variant in product['variants']:
        if variant['sku'] == sku_variant:
            return variant
    return Response(response='NOT FOUND',status=404)  
    

app.run(debug=True)