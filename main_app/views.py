from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from . import models
from openai import OpenAI 
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request,'index.html')
def diet(request):
    return render(request,'dietoverview.html')
def contact(request):
    return render(request,'contact.html')
def about(request):
    return render(request,'about.html')

def loggout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')  # Redirect to login page after logout

def userlogin(request):
    if request.method == 'POST':
        # Get form data
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Log the user in
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')  # Redirect to home or dashboard after login
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'login.html')
    return render(request,'login.html')


def usersignup(request):
    if request.method=="POST":
        full_name = request.POST.get('fullName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        # Validation
        if not all([full_name, email, password, confirm_password]):
            messages.error(request, 'All fields are required.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=email).exists():
            messages.error(request, 'Email already in use.')
        else:
            # Create user
            user = User.objects.create(
                username=email,
                email=email,
                first_name=full_name.split()[0],  # Optional: Split first name
                last_name=" ".join(full_name.split()[1:]),  # Optional: Split last name
                password=make_password(password),  # Hash password
            )
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')  # Redirect to login page
    return render(request,'signup.html')
@login_required
def dashboard(request):
    user_diet_plans = models.DietPlan.objects.filter(user=request.user).order_by('-created_at')

    if request.method == "POST":
        # Collect form data
        gender = request.POST.get("gender")
        age = request.POST.get("age")
        height = request.POST.get("height")
        weight = request.POST.get("weight")
        diet_goal = request.POST.get("diet_goal")
        time_period = request.POST.get("diet_time_period")
        # API request
        api_key='YOUR API KEY' 
        client = OpenAI(api_key=api_key)
        client.base_url= "https://api.inferkit.ai/v1"  #alternate for openai api inferkit.ai
        prompt = (
            f"Generate a {time_period} {diet_goal} "
            f"diet plan for a {age}-year-old {gender.lower()} who is {height} cm tall and weighs {weight} kg. "
            "The diet plan should follow Indian food preferences and include only easily available, common foods "
            "(no rare or exotic items). Provide meals for the day including Breakfast, Mid-Morning Snack, Lunch, "
            f"Evening Snack, and Dinner. Only need day 1 plan that can be used throughout the {time_period} , remember egg falls under the category of non-veg.\n\n"
            "Response format:\n"
            "Day1:\n"
            "Breakfast: [Food items and quantities]\n"
            "Mid-Morning Snack: [Food items and quantities]\n"
            "Lunch: [Food items and quantities]\n"
            "Evening Snack: [Food items and quantities]\n"
            "Dinner: [Food items and quantities]\n"
        )        
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert dietician"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=500,
        )
        answer = response.choices[0].message.content.strip()
        
        # Storing in database
        diet_plan = models.DietPlan.objects.create(
                user=request.user,  # If you have user authentication
                gender=gender,
                age=age,
                height=height,
                weight=weight,
                diet_goal=diet_goal,
                diet_time_period=time_period,
                diet_plan_text=answer
            )
        diet_plan.save()
        diet_plan_json = {
                "Day1": {
                    "Breakfast": answer.split("Breakfast:")[1].split("Mid-Morning Snack:")[0].strip(),
                    "Mid_Morning_Snack": answer.split("Mid-Morning Snack:")[1].split("Lunch:")[0].strip(),
                    "Lunch": answer.split("Lunch:")[1].split("Evening Snack:")[0].strip(),
                    "Evening_Snack": answer.split("Evening Snack:")[1].split("Dinner:")[0].strip(),
                    "Dinner": answer.split("Dinner:")[1]
                }
            }
        
        return render(request, 'response.html', {'diet_plan': diet_plan_json})        
        
        
        
        
        
        
        
    return render(request,'userdashboard.html', {'user_diet_plans': user_diet_plans})

@login_required
def diet_history(request, plan_id):
    # Fetch the diet plan by its ID
    diet_plan = get_object_or_404(models.DietPlan, id=plan_id, user=request.user)
    
    # The diet plan's text content
    diet_plan_json = {
        "Day1": {
            "Breakfast": diet_plan.diet_plan_text.split("Breakfast:")[1].split("Mid-Morning Snack:")[0].strip(),
            "Mid_Morning_Snack": diet_plan.diet_plan_text.split("Mid-Morning Snack:")[1].split("Lunch:")[0].strip(),
            "Lunch": diet_plan.diet_plan_text.split("Lunch:")[1].split("Evening Snack:")[0].strip(),
            "Evening_Snack": diet_plan.diet_plan_text.split("Evening Snack:")[1].split("Dinner:")[0].strip(),
            "Dinner": diet_plan.diet_plan_text.split("Dinner:")[1]
        }
    }
    
    return render(request, 'response.html', {'diet_plan': diet_plan_json})