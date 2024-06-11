from flask import redirect, render_template, request, url_for, flash
from beautyHaven import db, app, photos
from .models import Brand, Category,Product
from .forms import AddProducts
import secrets

@app.route('/addbrand', methods=['GET','POST'])
def addbrand():
    if request.method == "POST":
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'the brand {getbrand} added')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html')

@app.route('/addcategory', methods=['GET','POST'])
def addcategory():
    if request.method == "POST":
        getcategory = request.form.get('category')
        category = Category(name=getcategory)
        db.session.add(category)
        flash(f'the category {getcategory} added')
        db.session.commit()
        return redirect(url_for('addcategory'))
    return render_template('products/addcategory.html')

@app.route('/addproduct', methods=['GET','POST'])
def addproduct():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = AddProducts()
    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        quantity = form.quantity.data
        description = form.description.data
        brand_id = request.form.get('brand')
        category_id = request.form.get('category')

        # Generate unique filenames
        img1 = photos.save(form.img1.data, name=secrets.token_hex(10) + ".")
        img2 = photos.save(form.img2.data, name=secrets.token_hex(10) + ".")
        img3 = photos.save(form.img3.data, name=secrets.token_hex(10) + ".")

        # Create product instance
        addpro = Product(
            name=name, 
            price=price, 
            discount=discount, 
            stock=quantity, 
            description=description, 
            brand_id=brand_id, 
            category_id=category_id, 
            image_1=img1, 
            image_2=img2, 
            image_3=img3
        )
        db.session.add(addpro)
        db.session.commit()
        flash('The product was added successfully.')
        return redirect(url_for('addproduct'))

    return render_template('products/addproduct.html', form=form, brands=brands, categories=categories)