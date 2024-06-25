from flask import redirect, render_template, request, session, url_for, flash,current_app
from beautyHaven import db, app, photos
from beautyHaven.products.models import Product

def magerDict(dict1, dict2):
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        dict1.update(dict2)
        return dict1
    return False



@app.route('/addCart', methods=['POST'])
def addCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        product = Product.query.filter_by(id=product_id).first()
        if product_id and quantity and request.method == "POST":
            DectItems = {product_id:{'name': product.name, 'price':product.price, 'discount':product.discount,'quantity':quantity, 'image':product.image_1}}
       
        if 'shoppingcart' in session:
            if product_id in session['shoppingcart']:
                session['shoppingcart'][product_id]['quantity'] += quantity
                print('Product quantity updated.', 'success')
            else:
                session['shoppingcart'] = magerDict(session['shoppingcart'], DectItems)
                flash('Product added to cart.', 'success')
        else:
            session['shoppingcart'] = DectItems
            print('Product added to cart.', 'success')
        
        return redirect(request.referrer)
    
    except Exception as e:
        flash(f'Error adding product to cart: {e}', 'danger')
        return redirect(request.referrer)
    except Exception as e:
        flash(f'Error adding product to cart: {e}', 'danger')
        return redirect(request.referrer)
    


@app.route('/carts')
def getcart():
    if 'shoppingcart' not in session:
        flash('Your shopping cart is empty.', 'warning')
        return redirect(url_for('index'))

    shoppingcart = session['shoppingcart']
    subtotal = 0
    grandtotal = 0
    cart_items = []

    for key, product in shoppingcart.items():  # Use items() to correctly iterate
        price = float(product['price'])
        quantity = int(product['quantity'])
        discount = (product['discount'] / 100) * price
        total_price_per_product = (price - discount) * quantity
        subtotal += total_price_per_product
        cart_items.append({
            'name': product['name'],
            'price': price,
            'quantity': quantity,
            'discount': discount,
            'total': total_price_per_product,
            'image': product['image']
        })
    grandtotal = subtotal 

    return render_template('products/carts.html', cart_items=cart_items, subtotal=subtotal, grandtotal=grandtotal)
