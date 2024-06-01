from django.shortcuts import render, redirect, get_object_or_404
from .models import FoodCategory, Menu, Tables, Order, OrderItem, Checkout
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from django.http import JsonResponse
from django.template.loader import render_to_string


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.


def Add_Category(request):
    if request.method == "POST":
        pic = request.FILES['pic']
        cname = request.POST['cname']
        foodcategory = FoodCategory.objects.create(image = pic, name= cname)
        foodcategory.save()
        messages.success(request,"Food Category Addedd...")
        return redirect("List_Category")
    
    return render(request,'add-category.html')

def List_Category(request):
    food_category = FoodCategory.objects.all()
    p = Paginator(food_category, 20)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    context = {
        "food_category":page_obj
    }
    return render(request,'list-category.html',context)

def DeleteCategory(request,pk):
    FoodCategory.objects.get(id = pk).delete()
    messages.success(request,'Food Category Deleted')
    return redirect('List_Category')


def Add_Product(request):
    food_category = FoodCategory.objects.all()
    description = " "
    if request.method == "POST":
        name = request.POST['name']
        category = FoodCategory.objects.get(id = int(request.POST['category']))
        potion = request.POST['potion']
        diet = request.POST['diet']
        price = request.POST['price']
        stock = request.POST['stock']
        image = request.FILES['pic']
        description = request.POST['description']

        menu = Menu.objects.create(
            name = name, 
            category = category, 
            image = image, 
            potion = potion, 
            diet =diet, 
            price = price, 
            stock = stock, 
            description = description 
            )
        menu.save()
        messages.success(request,"Menu Item added Success...")
        return redirect("List_Product")
    
    context = {
        "food_category":food_category
    }
    return render(request,'add-product.html',context)

def List_Product(request):
    menu = Menu.objects.all()

    context = {
        "menu":menu
    }
    return render(request,'list-product.html',context)

def DeleteProduct(request,pk):
    return redirect("List_Product")


def Add_Table(request):
    if request.method == "POST":
        tnum = request.POST['tnum']
        seats = request.POST['seats']
        if Tables.objects.filter(Table_number = tnum).exists():
            messages.error(request,"Table Already Exists...")
            return redirect("Add_Table")
        else:
            table = Tables.objects.create(Table_number = tnum, Number_of_Seats = seats)
            table.save()
            messages.success(request,"Table added Success...")
            return redirect("List_Table")

    return render(request,"add-table.html")

def List_Table(request):
    table = Tables.objects.all()
    context = {
        "table":table
    }
    return render(request,"list-table.html",context)

def Delete_Table(request,pk):
    Tables.objects.get(id = pk).delete()
    messages.success(request,"Table deleted success....")
    return redirect("List_Table")


def Pos(request):
    category = FoodCategory.objects.all()
    menu = Menu.objects.all()
    table = Tables.objects.all()
    orders = Order.objects.filter(user = request.user)
    order_details = []

    for order in orders:
        total_items = sum(item.quantity for item in order.items.all())
        total_price = sum(item.get_total_price() for item in order.items.all())
        order_details.append({
            'order': order,
            'total_items': total_items,
            'total_price': total_price,
        })

    context = {
        "category":category,
        "menu":menu,
        "table":table,
        "orders":orders,
        'order_details': order_details,
    }
    return render(request,'posinterface.html',context)

def OrderSingle(request,pk):
    category = FoodCategory.objects.all()
    menu = Menu.objects.all()
    order = Order.objects.get(id = pk)
    item = OrderItem.objects.filter(order = order)
    total_price = sum(item.get_total_price() for item in order.items.all())
    


    context = {
        "category":category,
        "menu":menu,
        "order":order,
        "item":item,
        "total_price":total_price
    }
    return render(request,"order-single.html",context)

def CreateOrder(request):
    if request.method == "POST":
        table = Tables.objects.get(id = int(request.POST['table']))
        order = Order.objects.create(table = table,user = request.user )
        order.save()
        
        return redirect('OrderSingle',pk = order.id )
    


def add_to_order(request):
    if request.method == "POST":
        menu_item_id = request.POST.get('menu_item_id')
        order_id = request.POST.get('order_id')
        menu_item = get_object_or_404(Menu, id=menu_item_id)
        order = get_object_or_404(Order, id=order_id)

        # Create or update the OrderItem
        order_item, created = OrderItem.objects.get_or_create(order=order, menu_item=menu_item, defaults={'price': menu_item.price})
        if not created:
            order_item.quantity += 1
            order_item.save()

        # Render the updated order items and return as HTML
        item = OrderItem.objects.filter(order = order)
        total_price = sum(item.get_total_price() for item in order.items.all())
        order_html = render_to_string('order-summery.html', {'order': order,"item":item,"total_price":total_price})

        return JsonResponse({'order_html': order_html})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def increase_quantity(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        order_item = get_object_or_404(OrderItem, id=item_id)
        order_item.quantity += 1
        order_item.save()

        item = OrderItem.objects.filter(order = order_item.order)
        total_price = sum(item.get_total_price() for item in order_item.order.items.all())
        order_html = render_to_string('order-summery.html', {'order': order_item.order, 'total_price': total_price,"item":item})

        return JsonResponse({'order_html': order_html})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def decrease_quantity(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        order_item = get_object_or_404(OrderItem, id=item_id)
        if order_item.quantity > 1:
            order_item.quantity -= 1
            order_item.save()

        item = OrderItem.objects.filter(order = order_item.order)
        total_price = sum(item.get_total_price() for item in order_item.order.items.all())
        order_html = render_to_string('order-summery.html', {'order': order_item.order, 'total_price': total_price,"item":item})

        return JsonResponse({'order_html': order_html})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def Delete_menuitem(request,pk):
    item = OrderItem.objects.get(id = pk)
    order = item.order.id
    item.delete()
    return redirect("OrderSingle",pk = order)


def TakeOrder(request,pk):
    order = Order.objects.get(id =pk)
    order.take_order = True
    order.completion_status = False
    order.save()
    posted_data = order 
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "updates",
        {
            "type": "send_update",
            "message": "Database updated",
            
        }
    )
    return redirect("Pos")


def receipt_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()
    total_price = sum(item.get_total_price() for item in items)
    context = {
        'order': order,
        'item': items,
        'total_price': total_price,
    }
    return render(request, 'receipt.html', context)


def KitchenDashboard(request):
    orders = Order.objects.filter( take_order= True, completion_status = False )
    order_details = []
    orderitem = OrderItem.objects.all()
    for order in orders:
        orderitem = OrderItem.objects.filter(order = order)
        order_details.append(
            {
                "order":order,
                "orderitem":orderitem
            }
        ) 

    context = {
        "order_details":order_details
    } 

    return render(request,"kitchendash.html",context)



def refresh_table(request):
    orders = Order.objects.filter(take_order = True,completion_status = False)
    order_details = []
    orderitem = OrderItem.objects.all()
    for order in orders:
        orderitem = OrderItem.objects.filter(order = order)
        order_details.append(
            {
                "order":order,
                "orderitem":orderitem
            }
        ) 

    context = {
        "order_details":order_details
    }
    table_html = render_to_string('kitchendashitems.html', context)
    return JsonResponse({'table_html': table_html})

def Status_Change(request):
    if request.method == "POST":
        order_id = request.POST.get('orderid')  # Corrected key name
        order = get_object_or_404(Order, id=order_id)
        order.status = "In Progress"
        order.save()
        
        orders = Order.objects.filter(take_order=True,completion_status = False)
        order_details = []
        for order in orders:
            orderitem = OrderItem.objects.filter(order=order)
            order_details.append({
                "order": order,
                "orderitem": orderitem
            }) 

        context = {
            "order_details": order_details
        }
        table_html = render_to_string('kitchendashitems.html', context)
        return JsonResponse({'order_html': table_html})
    
def Status_Change_Order_Ready(request):
    if request.method == "POST":
        order_id = request.POST.get('orderid')  # Corrected key name
        order = get_object_or_404(Order, id=order_id)
        order.status = "Order Ready"
        order.save()
        
        orders = Order.objects.filter(take_order=True,completion_status = False)
        order_details = []
        for order in orders:
            orderitem = OrderItem.objects.filter(order=order)
            order_details.append({
                "order": order,
                "orderitem": orderitem
            }) 

        context = {
            "order_details": order_details
        }
        table_html = render_to_string('kitchendashitems.html', context)
        return JsonResponse({'order_html': table_html})
    

def Status_Change_Menu_Finish(request):
    if request.method == "POST":
        order_item_id = request.POST.get('orderid')  # Ensure the correct key is used
        order_item = get_object_or_404(OrderItem, id=order_item_id)
        order_item.completion_status = True
        order_item.save()
        
        orders = Order.objects.filter(take_order=True,completion_status = False)
        order_details = []
        for order in orders:
            orderitem = OrderItem.objects.filter(order=order)
            order_details.append({
                "order": order,
                "orderitem": orderitem
            })

        context = {
            "order_details": order_details
        }
        table_html = render_to_string('kitchendashitems.html', context)
        return JsonResponse({'order_html': table_html})

    

def Status_Change_OrderCompeletion(request,pk):
    
    order = get_object_or_404(Order, id=pk)
    order.completion_status = True
    order.take_order = False
    order.save()
    return redirect("KitchenDashboard")
        
        

    

