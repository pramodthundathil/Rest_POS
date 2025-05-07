from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserAddForm
from django.contrib.auth.models import User, Group
from .decorators import admin_only, unautenticated_user
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from datetime import date, datetime
from django.contrib.auth.decorators import login_required



from django.shortcuts import render
from Finance.models import Income, Expence
from Products.models import Checkout, OrderItem, Menu, Order
from datetime import datetime
import calendar
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def get_overview_chart_data(request):
    # Get the period from the request (default to 'month')
    period = request.GET.get('period', 'month')
    
    current_date = datetime.now()
    data = []
    
    if period == 'week':
        # Last 7 days
        labels = []
        income_data = []
        expense_data = []
        
        for i in range(6, -1, -1):
            date = current_date - timedelta(days=i)
            labels.append(date.strftime('%a'))  # Abbreviated day name
            
            # Get income for this day
            day_income = Income.objects.filter(
                date=date.date()
            ).values_list('amount', flat=True)
            income_data.append(round(sum(day_income), 2))
            
            # Get expenses for this day
            day_expenses = Expence.objects.filter(
                date=date.date()
            ).values_list('amount', flat=True)
            expense_data.append(round(sum(day_expenses), 2))
        
    elif period == 'year':
        # Last 12 months
        labels = []
        income_data = []
        expense_data = []
        
        for i in range(11, -1, -1):
            # Calculate month and year
            month = current_date.month - i
            year = current_date.year
            
            # Adjust for negative months
            while month <= 0:
                month += 12
                year -= 1
                
            labels.append(calendar.month_abbr[month])
            
            # Get income for this month
            month_income = Income.objects.filter(
                date__month=month,
                date__year=year
            ).values_list('amount', flat=True)
            income_data.append(round(sum(month_income), 2))
            
            # Get expenses for this month
            month_expenses = Expence.objects.filter(
                date__month=month,
                date__year=year
            ).values_list('amount', flat=True)
            expense_data.append(round(sum(month_expenses), 2))
    
    else:  # Default: month (last 30 days)
        # Days in current month
        labels = []
        income_data = []
        expense_data = []
        
        _, days_in_month = calendar.monthrange(current_date.year, current_date.month)
        
        for day in range(1, days_in_month + 1):
            date = datetime(current_date.year, current_date.month, day)
            labels.append(str(day))
            
            # Get income for this day
            day_income = Income.objects.filter(
                date__day=day,
                date__month=current_date.month,
                date__year=current_date.year
            ).values_list('amount', flat=True)
            income_data.append(round(sum(day_income), 2))
            
            # Get expenses for this day
            day_expenses = Expence.objects.filter(
                date__day=day,
                date__month=current_date.month,
                date__year=current_date.year
            ).values_list('amount', flat=True)
            expense_data.append(round(sum(day_expenses), 2))
    
    # Prepare the chart data
    chart_data = {
        'labels': labels,
        'datasets': [
            {
                'label': 'Income',
                'data': income_data,
                'backgroundColor': 'rgba(58, 122, 254, 0.2)',
                'borderColor': 'rgba(58, 122, 254, 1)',
                'borderWidth': 2
            },
            {
                'label': 'Expenses',
                'data': expense_data,
                'backgroundColor': 'rgba(255, 91, 92, 0.2)',
                'borderColor': 'rgba(255, 91, 92, 1)',
                'borderWidth': 2
            }
        ]
    }
    
    return JsonResponse(chart_data)

from django.http import JsonResponse
from django.db.models import Count, Sum, F, Avg
from django.utils import timezone
from datetime import timedelta



def get_top_products(request):
    try:
        # Get the filter parameter (default to 'month')
        time_filter = request.GET.get('filter', 'month')
        
        # Set the time range based on the filter
        today = timezone.now().date()
        if time_filter == 'week':
            start_date = today - timedelta(days=7)
        elif time_filter == 'year':
            start_date = today - timedelta(days=365)
        else:  # Default to month
            start_date = today - timedelta(days=30)
        
        # Query to get top 5 products by order count
        top_products = OrderItem.objects.filter(
            order__create_date__date__gte=start_date
        ).values(
            'menu_item'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        # Format the data for the response
        products_data = []
        
        for product in top_products:
            try:
                # Get the actual Menu object to access its fields properly
                menu_item = Menu.objects.get(id=product['menu_item'])
                
                # Get image URL or default
                image_url = ''
                if menu_item.image and hasattr(menu_item.image, 'url'):
                    image_url = menu_item.image.url
                
                products_data.append({
                    'name': menu_item.name,
                    'count': product['count'],
                    'image': image_url,
                })
            except Menu.DoesNotExist:
                # Skip if menu item doesn't exist
                continue
            except Exception as e:
                # Log the error but continue processing other items
                print(f"Error processing menu item {product['menu_item']}: {str(e)}")
                continue
        
        return JsonResponse({'top_products': products_data})
    
    except Exception as e:
        # Return error response
        return JsonResponse({'error': str(e)}, status=500)


def get_order_summary(request):
    # Get the filter parameter (default to 'month')
    time_filter = request.GET.get('filter', 'month')
    
    # Set the time range based on the filter
    today = timezone.now().date()
    if time_filter == 'week':
        start_date = today - timedelta(days=7)
        date_format = '%a'  # Day name (Mon, Tue, etc.)
        days = 7
    elif time_filter == 'year':
        start_date = today - timedelta(days=365)
        date_format = '%b'  # Month name (Jan, Feb, etc.)
        days = 12
    else:  # Default to month
        start_date = today - timedelta(days=30)
        date_format = '%d'  # Day of month (01-31)
        days = 30
    
    # Calculate total orders and revenue in the period
    orders_in_period = Order.objects.filter(
        create_date__date__gte=start_date,
        checkout_status=True  # Only consider completed orders
    )
    
    total_revenue = orders_in_period.aggregate(
        total=Sum('total_price')
    )['total'] or 0
    
    avg_order_value = orders_in_period.aggregate(
        avg=Avg('total_price')
    )['avg'] or 0
    
    # Find top order value
    top_order_value = orders_in_period.order_by('-total_price').first()
    top_order = top_order_value.total_price if top_order_value else 0
    
    # Get daily order data for chart
    if time_filter == 'year':
        # Group by month for yearly view
        date_trunc = 'month'
    elif time_filter == 'week':
        # Group by day for weekly view
        date_trunc = 'day'
    else:
        # Group by day for monthly view
        date_trunc = 'day'
    
    from django.db.models.functions import TruncDay, TruncMonth, ExtractDay, ExtractMonth
    from django.db.models import DateField
    from django.db.models.functions import Cast
    
    # Prepare correct grouping based on filter
    if date_trunc == 'month':
        orders_by_date = orders_in_period.annotate(
            date=TruncMonth('create_date')
        )
    else:
        orders_by_date = orders_in_period.annotate(
            date=TruncDay('create_date')
        )
    
    # Group by date
    orders_by_date = orders_by_date.values('date').annotate(
        count=Count('id'),
        revenue=Sum('total_price')
    ).order_by('date')
    
    # Create a dictionary for all dates in range (filled with zeros by default)
    chart_data = []
    
    if time_filter == 'year':
        # For yearly view: last 12 months
        current_month = today.replace(day=1)
        for i in range(11, -1, -1):  # Count down to show most recent last
            month = (current_month - timedelta(days=30*i)).strftime('%b')
            chart_data.append({
                'label': month,
                'count': 0,
                'revenue': 0
            })
    elif time_filter == 'week':
        # For weekly view: last 7 days
        for i in range(6, -1, -1):  # Count down to show most recent last
            day = (today - timedelta(days=i)).strftime('%a')
            chart_data.append({
                'label': day,
                'count': 0,
                'revenue': 0
            })
    else:
        # For monthly view: last 30 days
        for i in range(29, -1, -1):  # Count down to show most recent last
            day = (today - timedelta(days=i)).strftime('%d')
            chart_data.append({
                'label': day,
                'count': 0,
                'revenue': 0
            })
    
    # Fill in actual data
    label_mapping = {}
    for entry in chart_data:
        label_mapping[entry['label']] = entry
    
    for order in orders_by_date:
        label = order['date'].strftime(date_format)
        if label in label_mapping:
            label_mapping[label]['count'] = order['count']
            label_mapping[label]['revenue'] = float(order['revenue'])
    
    # Calculate percentages
    if total_revenue > 0:
        avg_percentage = min(int((avg_order_value / total_revenue) * 100), 100)
        top_percentage = min(int((top_order / total_revenue) * 100), 100)
    else:
        avg_percentage = 0
        top_percentage = 0
    
    # Format monetary values
    avg_order_value = round(avg_order_value, 2)
    top_order = round(top_order, 2)
    
    # Prepare response data
    response_data = {
        'avg_order_value': avg_order_value,
        'avg_percentage': avg_percentage,
        'top_order_value': top_order,
        'top_percentage': top_percentage,
        'chart_data': chart_data
    }
    
    return JsonResponse(response_data)

# from django.http import JsonResponse
# from datetime import datetime, timedelta
# from django.views.decorators.http import require_GET
# from .models import Income, Expence
# import json

@require_GET
def get_income_data(request):
    """API endpoint to get income data for charts"""
    timeframe = request.GET.get('timeframe', 'month')
    
    # Calculate date range based on timeframe
    end_date = datetime.now().date()
    
    if timeframe == 'week':
        start_date = end_date - timedelta(days=7)
    elif timeframe == 'month':
        start_date = end_date - timedelta(days=30)
    elif timeframe == 'year':
        start_date = end_date - timedelta(days=365)
    else:
        start_date = end_date - timedelta(days=30)  # Default to month
    
    # Query the database
    income_data = Income.objects.filter(
        date__gte=start_date,
        date__lte=end_date
    ).values('date', 'amount', 'perticulers')
    
    # Convert to list for JSON serialization
    result = list(income_data)
    
    return JsonResponse(result, safe=False)

@require_GET
def get_expense_data(request):
    """API endpoint to get expense data for charts"""
    timeframe = request.GET.get('timeframe', 'month')
    
    # Calculate date range based on timeframe
    end_date = datetime.now().date()
    
    if timeframe == 'week':
        start_date = end_date - timedelta(days=7)
    elif timeframe == 'month':
        start_date = end_date - timedelta(days=30)
    elif timeframe == 'year':
        start_date = end_date - timedelta(days=365) 
    else:
        start_date = end_date - timedelta(days=30)  # Default to month
    
    # Query the database
    expense_data = Expence.objects.filter(
        date__gte=start_date,
        date__lte=end_date
    ).values('date', 'amount', 'perticulers')
    
    # Convert to list for JSON serialization
    result = list(expense_data)
    
    return JsonResponse(result, safe=False)

def get_current_month_income_and_expense():
    # Get current year and month
    today = datetime.date.today()
    current_month_start = today.replace(day=1)
    current_month_end = (today.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
    
    # Filter and aggregate total income for the current month
    total_income = Income.objects.filter(
        date__gte=current_month_start,
        date__lte=current_month_end
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # Filter and aggregate total expenses for the current month
    total_expense = Expence.objects.filter(
        date__gte=current_month_start,
        date__lte=current_month_end
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    return total_income, total_expense

def monthly_income_view():
    today = datetime.today()
    
    # Get the first and last day of the current month
    first_day_of_month = today.replace(day=1)
    next_month = first_day_of_month.replace(month=today.month % 12 + 1, day=1) if today.month != 12 else first_day_of_month.replace(year=today.year + 1, month=1)
    last_day_of_month = next_month - timedelta(days=1)

    # Get all income and expense entries for the current month
    income_entries = Income.objects.filter(date__range=[first_day_of_month, last_day_of_month])
    expense_entries = Expence.objects.filter(date__range=[first_day_of_month, last_day_of_month])

    # Calculate weekly income
    weekly_income = []
    weekly_expense = []
    current_start = first_day_of_month
    while current_start <= last_day_of_month:
        current_end = min(current_start + timedelta(days=6), last_day_of_month)

        # Income for the week
        weekly_total_income = income_entries.filter(date__range=[current_start, current_end]).aggregate(Sum('amount'))['amount__sum'] or 0
        weekly_income.append(weekly_total_income)

        # Expense for the week
        weekly_total_expense = expense_entries.filter(date__range=[current_start, current_end]).aggregate(Sum('amount'))['amount__sum'] or 0
        weekly_expense.append(weekly_total_expense)

        current_start = current_end + timedelta(days=1)

    # Pass the weekly income and expense data to the template
    
    
    

    return weekly_income, weekly_expense


def popular_menu_items(request):
    # Get time period from request parameter (default to 'month')
    time_period = request.GET.get('period', 'month')
    
    # Calculate date range based on time period
    today = timezone.now().date()
    if time_period == 'week':
        start_date = today - timedelta(days=7)
    elif time_period == 'month':
        start_date = today - timedelta(days=30)
    elif time_period == 'year':
        start_date = today - timedelta(days=365)
    else:
        # Default to month
        start_date = today - timedelta(days=30)
    
    # Query the database for popular menu items
    popular_items = OrderItem.objects.filter(
        order__create_date__date__gte=start_date,
        order__create_date__date__lte=today
    ).values(
        'menu_item__name', 
        'menu_item__category__name'
    ).annotate(
        total_orders=Count('id'),
        total_quantity=Sum('quantity'),
        total_revenue=Sum('price')
    ).order_by('-total_quantity')[:10]  # Get top 10 items
    
    # Format the data for the chart
    categories = []
    items = []
    quantities = []
    revenues = []
    
    for item in popular_items:
        items.append(item['menu_item__name'])
        quantities.append(item['total_quantity'])
        revenues.append(float(item['total_revenue']))
        categories.append(item['menu_item__category__name'])
    
    # Prepare the response data
    data = {
        'items': items,
        'quantities': quantities,
        'revenues': revenues,
        'categories': categories,
        'period': time_period
    }
    
    return JsonResponse(data)

def Index(request):
    # Get current month and year
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    month_name = calendar.month_name[current_month]
    
    # Calculate total income for the current month
    month_income = Income.objects.filter(
        date__month=current_month,
        date__year=current_year
    ).values_list('amount', flat=True)
    total_income = sum(month_income)
    
    # Calculate total expenses for the current month
    month_expenses = Expence.objects.filter(
        date__month=current_month,
        date__year=current_year
    ).values_list('amount', flat=True)
    total_expenses = sum(month_expenses)
    
    # Count total invoices (using Checkout model)
    total_invoices = Checkout.objects.count()

    weekly_income,weekly_expense = monthly_income_view()
    
    context = {
        'month': month_name,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'total_invoices': total_invoices,
        "weekly_income":weekly_income,
        "weekly_expense":weekly_expense,
    }
    
    return render(request, 'index.html', context)



@unautenticated_user
def SignIn(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pswd']
        user1 = authenticate(request, username = username , password = password)
        
        if user1 is not None:
            
            request.session['username'] = username
            request.session['password'] = password
            login(request, user1)
            return redirect('PosIndex')
        
        else:
            messages.error(request,'Username or Password Incorrect')
            return redirect('SignIn')
    return render(request,"login.html")


def SignOut(request):
    logout(request)
    return redirect('SignIn')

@login_required(login_url="SignIn")
def ListUser(request):
    contacts = User.objects.all()
    p = Paginator(contacts, 20)
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
        'contacts':page_obj
    }

    return render(request,"user-list.html",context)


@login_required(login_url="SignIn")
def AddUser(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname= request.POST['lname']
        email = request.POST["email"]
        uname = request.POST["uname"]
        pswd = request.POST["pswd"]
        pswd1 = request.POST["pswd1"]
        utype = request.POST['utype']

        if pswd != pswd1:
            messages.error(request,"Password Do not Matches..")
            return redirect("AddUser")
        if User.objects.filter(username = uname).exists():
            messages.error(request,"Username alredy exists user another username")
            return redirect("AddUser")
        if User.objects.filter(email = email).exists():
            messages.error(request,"Email alredy exists user another email")
            return redirect("AddUser")
        else:
            user = User.objects.create_user(first_name = fname,last_name = lname,email = email, username = uname, password =pswd)
            user.save()

            group = Group.objects.get(name=utype)
            user.groups.add(group)
            if utype == "dboy":
                user.is_active = False
                user.save()
            messages.success(request,"Staff added To Staff list....")
            return redirect("ListUser")
    return render(request,"user-add.html")

@login_required(login_url="SignIn")
def DeleteUser(request,pk):
    User.objects.get(id = pk).delete()
    messages.success(request,"User Data Deleted.....")
    return redirect("ListUser")






# authetication an d log out functions starts................................
@unautenticated_user
def SignUp(request):
    form = UserAddForm()
    if request.method == "POST":
        # fname = request.POST["fname"]
        # email = request.POST["email"]
        # uname = request.POST["uname"]
        # pswd = request.POST["pswd"]
        # pswd1 = request.POST["pswd1"]

        # if pswd != pswd1:
        #     messages.info(request,"Password Do not Matches..")
        #     return redirect("SignUp")
        # if User.objects.filter(username = uname).exists():
        #     messages.info(request,"Username alredy exists user another username")
        #     return redirect("SignUp")
        # if User.objects.filter(email = email).exists():
        #     messages.info(request,"Email alredy exists user another email")
        #     return redirect("SignUp")

        form = UserAddForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.save()
            group = Group.objects.get(name='student')
            user.groups.add(group)
            messages.success(request,"User Created.. Please Login....")
            return redirect("SignIn")
        
    return render(request,"register.html",{"form":form})


def PermissionDenyed(request):
    return render(request,"pages-error.html")



def custom_page_not_found_view(request, exception):
    return render(request, 'pages-error.html', status=404)

def custom_server_error_view(request):
    return render(request, 'pages-error.html', status=500)

def custom_permission_denied_view(request, exception):
    return render(request, 'pages-error.html', status=403)

def custom_bad_request_view(request, exception):
    return render(request, 'pages-error.html', status=400)