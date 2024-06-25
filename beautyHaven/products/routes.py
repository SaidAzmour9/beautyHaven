from flask import redirect, render_template, request, session, url_for, flash,current_app
from beautyHaven import db, app, photos
from .models import Brand, Category,Product
from beautyHaven.admin.routes import products
from .forms import AddProducts
import secrets, os


def firstfour(name, word_limit=5):
    words = name.split()
    if len(words) > word_limit:
        return ' '.join(words[:word_limit]) + '...'
    return name

def firstten(description, word_limit=8):
    words = description.split()
    if len(words) > word_limit:
        return ' '.join(words[:word_limit]) + '...'
    return description

def firstaa(description, word_limit=50):
    words = description.split()
    if len(words) > word_limit:
        return ' '.join(words[:word_limit]) + '...'
    return description

@app.route('/')
def home():
    categorys = Category.query.join(Product,(Category.id == Product.category_id)).all()
    brands = Brand.query.join(Product,(Brand.id == Product.brand_id)).all()
    products = Product.query.filter(Product.stock > 0).order_by(Product.id.desc()).limit(6).all()
    return render_template('products/index.html', products=products, firstten=firstten, firstfour=firstfour,categorys=categorys,brands=brands)

@app.route('/addbrand', methods=['GET','POST'])
def addbrand():
    if 'email' not in session:
        flash('Please login first')
        return redirect('login')
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
    if 'email' not in session:
        flash('Please login first')
        return redirect('login')
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
    if 'email' not in session:
        flash('Please login first')
        return redirect('login')
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

@app.route('/updatebrand/<int:id>',methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash('Please login first')
        return redirect('login')
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == 'POST':
        updatebrand.name = brand
        flash('your brand name updated seccesfuly')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html',updatebrand=updatebrand)

@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(brand)
        db.session.commit()
        return redirect(url_for('brands'))

@app.route('/deletecategory/<int:id>', methods=['POST'])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
        return redirect(url_for('categorys'))

@app.route('/updatecat/<int:id>',methods=['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash('Please login first')
        return redirect('login')
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == 'POST':
        updatecat.name = category
        flash('your category name updated seccesfuly')
        db.session.commit()
        return redirect(url_for('categorys'))
    return render_template('products/updatecat.html',updatecat=updatecat)


@app.route('/updateproduct/<int:id>', methods=['GET','POST'])
def updatepro(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    brand = request.form.get('brand')
    category = request.form.get('category')
    product = Product.query.get_or_404(id)
    form = AddProducts(request.form)
    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.description = form.description.data
        product.stock = form.quantity.data
        product.brand_id = brand
        product.category_id = category
        product.discount = form.discount.data
    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.description = form.description.data
        product.stock = form.quantity.data
        product.brand_id = request.form.get('brand')
        product.category_id = request.form.get('category')
        product.discount = form.discount.data
        if 'img1' in request.files and request.files['img1'].filename != '':
            if product.image_1 and product.image_1 != 'default_product.jpg':
                try:
                    os.unlink(os.path.join(current_app.root_path, 'uploads/images/' + product.image_1))
                except FileNotFoundError:
                    pass
            img1_file = request.files['img1']
            img1_filename = secrets.token_hex(10) + "." + img1_file.filename.rsplit('.', 1)[1].lower()
            img1_path = photos.save(img1_file, name=img1_filename)
            product.image_1 = img1_path

        if 'img2' in request.files and request.files['img2'].filename != '':
            if product.image_2 and product.image_2 != 'default_product.jpg':
                try:
                    os.unlink(os.path.join(current_app.root_path, 'uploads/images/' + product.image_2))
                except FileNotFoundError:
                    pass
            img2_file = request.files['img2']
            img2_filename = secrets.token_hex(10) + "." + img2_file.filename.rsplit('.', 1)[1].lower()
            img2_path = photos.save(img2_file, name=img2_filename)
            product.image_2 = img2_path

        if 'img3' in request.files and request.files['img3'].filename != '':
            if product.image_3 and product.image_3 != 'default_product.jpg':
                try:
                    os.unlink(os.path.join(current_app.root_path, 'uploads/images/' + product.image_3))
                except FileNotFoundError:
                    pass
            img3_file = request.files['img3']
            img3_filename = secrets.token_hex(10) + "." + img3_file.filename.rsplit('.', 1)[1].lower()
            img3_path = photos.save(img3_file, name=img3_filename)
            product.image_3 = img3_path

        db.session.commit()
        flash('Product updated successfully.')
        return redirect(url_for('products'))
    form.name.data = product.name
    form.price.data = product.price
    form.description.data = product.description
    form.quantity.data = product.stock
    form.discount.data = product.discount
    return render_template('products/updateproduct.html', form=form, product=product, categories=categories, brands=brands)


@app.route('/deleteproduct/<int:id>',methods=['GET','POST'])
def deleteproduct(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        if product.image_1 and product.image_1 != 'default_product.jpg':
            try:
                os.unlink(os.path.join(current_app.root_path, 'uploads/images/' + product.image_1))
            except FileNotFoundError:
                pass
        
        if product.image_2 and product.image_2 != 'default_product.jpg':
            try:
                os.unlink(os.path.join(current_app.root_path, 'uploads/images/' + product.image_2))
            except FileNotFoundError:
                pass
        
        if product.image_3 and product.image_3 != 'default_product.jpg':
            try:
                os.unlink(os.path.join(current_app.root_path, 'uploads/images/' + product.image_3))
            except FileNotFoundError:
                pass


        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('products'))


@app.route('/brand/<int:id>', methods=['GET','POST'])
def get_brand(id):
    categorys = Category.query.join(Product,(Category.id == Product.category_id)).all()
    brand = Product.query.filter_by(brand_id = id)
    brands = Brand.query.join(Product,(Brand.id == Product.brand_id)).all()
    return render_template('products/index.html', brand = brand,brands = brands,categorys = categorys, firstten=firstten, firstfour=firstfour)

@app.route('/category/<int:id>', methods=['GET','POST'])
def get_category(id):
    category = Product.query.filter_by(category_id = id)
    brands = Brand.query.join(Product,(Brand.id == Product.brand_id)).all()
    categorys = Category.query.join(Product,(Category.id == Product.category_id)).all()
    return render_template('products/index.html', category = category,categorys = categorys,brands=brands, firstten=firstten, firstfour=firstfour)

@app.route('/product/<int:id>', methods=['GET','POST'])
def single_pro(id):
    product= Product.query.get_or_404(id)
    return render_template('products/single_pro.html', product=product,firstaa=firstaa)