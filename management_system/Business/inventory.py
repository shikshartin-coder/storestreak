from .data_interface import Category_interface, Product_interface, Product_type_interface,Business_interface
from django.shortcuts import render,redirect, HttpResponseRedirect,HttpResponse
from django.shortcuts import redirect
from django.core.files.storage import default_storage
from landing_website import constants
from image_compressor import image_compressor

def category_view(request,page):
    error = None
    all_category_dict = {}
    category_list = Category_interface().get_category(request.user.id)
    for category in reversed(category_list):
        product_list = Product_interface().get_product_by_category_id(category.id)
        pro_type_list = []
        for pro in product_list:
            pro_type_list.append(Product_type_interface().get_all_product_type_by_product_id(pro.id))
        all_category_dict.update({category:len(pro_type_list)})

    context = {
        'error':error,
        'category_list':category_list,
        'page':page,
        'search_page':'category',
        'all_category_dict':all_category_dict,
    }
    return render(request,'./business/Inventory/business_category.html',context)

def add_category(request,page):
    if request.method == 'POST':
        btn = request.POST.get('btn')
        if btn == 'add-category':
            new_name = request.POST.get('category_name')
            image = image_compressor.compress( request.POST.get('category_image'),'category/new_category.jpeg')

            category_object = Category_interface().create_category(new_name,image,request.user.id)
            if category_object == None:
                context = {
                    'error' : "Error in creating category",
                    'page':page,
                }
            else:
                return redirect('inventory_view',part='category')

        if btn == 'edit':
           Category_interface().update_category()

    context = {
         'page':page,
    }
    return render(request,'./business/Inventory/add_category.html',context)

def category_edit(request,category_id):
    page = 'edit'
    category_obj = Category_interface().get_category_by_id(category_id)
    if(request.method == 'POST'):
        new_name = request.POST.get('category_name')
        image = image_compressor.compress( request.POST.get('category_image'),'category/category_'+category_id+'.jpeg')

        if(image == None):
            image = category_obj.image

        if(category_obj.image != image):
            try:
                path =  category_obj.image.path
                default_storage.delete(path)
            except:
                print('no file found')
        category_object = Category_interface().update_category(category_obj.id,new_name,image,True)
        return redirect('edit_category',category_id=category_id)

    context = {
        'page':page,
        'category_obj':category_obj,
    }
    return render(request,'./business/Inventory/add_category.html',context)


def inventory_edit_product_type(request,product_type_id):
    page='edit'
    product_type_obj = Product_type_interface().get_product_type_by_id(product_type_id)

    category_id = Product_interface().get_category_id_from_product_type_id(product_type_id)
    category_list = Category_interface().get_category(request.user.id)

    if(request.method == 'POST'):
        btn = request.POST.get('btn')

        name = request.POST.get('product_name')
        category_id = request.POST.get('category_id')
        content = request.POST.get('product_description')
        stock = request.POST.get('initial_stock')
        mrp = request.POST.get('mrp',0)
        cost = request.POST.get('price_per_unit')
        pack_size = request.POST.get('pack_size')
        unit = request.POST.get('unit')

        product_image = image_compressor.compress(request.POST.get('product_image'),'products/product_'+product_type_id+'.jpeg')
        if(product_image == None):
            product_image = product_type_obj.image

        if(product_type_obj.image != product_image):
            try:
                path =   product_type_obj.image.path
                default_storage.delete(path)
            except:
                print('image does not exist')

        if(btn == 'edit_product'):
            product_type_key = Product_type_interface().create_product_type_key(name)
            product_obj = Product_interface().update_product(product_type_obj.product_id,name,category_id)
            product_type_obj = Product_type_interface().update_product_type(product_type_id,name,product_type_key,content,stock,cost,mrp,product_image,pack_size,unit)
            return redirect('edit_product',product_type_id=product_type_id)

    context = {
        'product_type_obj':product_type_obj,
        'category_id':category_id,
        'category_list': category_list,
        'page':page,
    }
    return render(request,'./business/Inventory/business_new_inventory.html',context)

def add_product(request,page):
    category_list = Category_interface().get_category(request.user.id)
    if(len(category_list) <= 0 ):
        return redirect('inventory_view',part='category')
    error = None
    if(request.method == 'POST'):
        btn = request.POST.get('btn')

        name = request.POST.get('product_name')
        category_id = request.POST.get('category_id')
        content = request.POST.get('product_description')
        stock = request.POST.get('initial_stock')
        cost = request.POST.get('price_per_unit')
        mrp =  request.POST.get('mrp',0)
        product_image = image_compressor.compress(request.POST.get('product_image'),'products/new_product.jpeg')
        pack_size = request.POST.get('pack_size')
        unit = request.POST.get('unit')
        if(btn == 'new_product'):
            product_obj = Product_interface().create_product(name,category_id,request.user.id)
            if(product_obj != None):
                product_type_obj =  Product_type_interface().create_product_type(product_obj.id,name,content,stock,cost,mrp,product_image,pack_size,unit,request.user.id)
                if(product_type_obj == None):
                    if(Product_interface().delete_product(product_obj.id)):
                        error = "Product is not created"
                else:
                    return redirect('inventory')
    unit_lists = constants.units
    context = {
        'error':error,
        'category_list': category_list,
        'page':page,
        'unit_lists':unit_lists,
    }
    return render(request,'./business/Inventory/business_new_inventory.html',context)


def product_view(request,page):
    products = Product_interface().get_product(request.user.id)
    product_obj_dict = {}
    for pro in products:
        product_obj_dict.update({pro:len(Product_type_interface().get_all_product_type_by_product_id(pro.id))})
    context = {
        'page':page,
        'product_obj_dict':product_obj_dict,
    }
    return render(request,'./business/Inventory/grouped_products.html',context)

def edit_product(request,product_id,page):
    error = None
    category_list = Category_interface().get_category(request.user.id)
    product =  Product_interface().get_product_by_id(request,product_id)
    product_type_list = Product_type_interface().get_product_type_by_product(request,product.id)
    if(product == None):
        return redirect('inventory')

    if(request.method == 'POST'):
        btn = request.POST.get('btn')
        name = request.POST.get('product_name')
        stock = request.POST.get('initial_stock')
        cost = request.POST.get('price_per_unit')
        mrp = request.POST.get('mrp',0)
        content = request.POST.get('product_description')

        if(btn == 'new_product_type'):
            product_type_obj = Product_type_interface().create_product_type(product_id,name,content,stock,cost,request.user.id)
            return redirect('inventory_edit',product_id=product_id)

        if(btn == 'edit_category'):
            category_id = request.POST.get('category_id')
            name = request.POST.get('product_name')
            status  = True
            product_update = Product_interface().update_product(product_id,name,category_id,status)
            return redirect('inventory_edit',product_id=product_id)

        if(btn == 'edit_product_type'):
            product_type_id = request.POST.get('product_type_id')
            product_type_key = Product_type_interface().create_product_type_key(name)
            status = True
            product_type_obj = Product_type_interface().update_product_type( product_type_id,name,product_type_key,stock,cost,mrp,content,status)
            return redirect('inventory_edit',product_id=product_id)

    context = {
        'error':error,
        'product':product,
        'category_list': category_list,
        'product_type_list':product_type_list,
        'page':page,

       }
    return render(request,'./business/Inventory/business_edit_inventory.html',context)