from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from review.models import movie_details
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def basic(request):
    return HttpResponse("Hello,Director")

def movie_info(request):
    movie=request.GET.get("movie")
    date=request.GET.get("date")
    return JsonResponse({"status":"Success","result":{"movie_name":movie,"release_date":date}},status=200)


@csrf_exempt
def movies(request):
    if request.method=="POST":
        data=json.loads(request.body)
        print("RATING RECEIVED:", data.get("rating"))  
        rating_number = int(data.get("rating",0))
        movie=movie_details.objects.create(movie_name=data.get("movie_name"),release_date=data.get("release_date"),budget=data.get("budget"),rating=data.get("rating"))
        rating_stars = "★" * rating_number 
        return JsonResponse({"status":"success","message":"movie record inserted successflly","movie_name":movie.movie_name,"release_date":movie.release_date,"budget":movie.budget,"rating":rating_stars},status=200)
    # return JsonResponse({"error":"error occured"},status=400)
    elif request.method=="GET":
        result=list(movie_details.objects.all().values())
        print(result)
        return JsonResponse({"status":"ok","data":result},status=200)
    
    elif request.method == "PUT":
        data = json.loads(request.body)

    # Access only reference id
        ref_id = data.get("id")

    # Fetch movie using filter (no error)
        movie_qs = movie_details.objects.filter(id=ref_id)

    # If movie not found
        if not movie_qs.exists():
            return JsonResponse({"error": "Movie not found"}, status=404)

    # Get the exact movie object
        movie_obj = movie_qs.first()

    # Now update only the fields you want
        if data.get("movie_name"):
            movie_obj.movie_name = data.get("movie_name")

        if data.get("release_date"):
            movie_obj.release_date = data.get("release_date")

        if data.get("budget"):
            movie_obj.budget = data.get("budget")

        if data.get("rating"):
            movie_obj.rating = data.get("rating")

    # Save the updated movie
        movie_obj.save()

        return JsonResponse({
            "status": "success",
                "message": "Movie updated successfully"
        }, status=200)
    
    elif request.method == "DELETE":
        data = json.loads(request.body)

        movie_name = data.get("movie_name")

    # Search for this movie
        movie_qs = movie_details.objects.filter(movie_name=movie_name)

        if not movie_qs.exists():
            return JsonResponse({"error": "Movie not found"}, status=404)

    # Delete the movie
        movie_qs.delete()

        return JsonResponse({
            "status": "success",
            "message": f"{movie_name} is deleted"
        }, status=200)
    
def budget_more(request):
    if request.method == "GET":
        budget_limit = request.GET.get("budget")

        if not budget_limit:
            return JsonResponse({"error": "Please give budget"}, status=400)

        # Remove 'cr' from query parameter
        budget_limit = int(budget_limit.replace("cr", "").replace("CR", ""))

        result = []

        for m in movie_details.objects.all():
            # Clean the budget inside db
            db_budget = int(m.budget.replace("cr", "").replace("CR", ""))

            if db_budget > budget_limit:
                result.append({
                    "movie_name": m.movie_name,
                    "release_date": m.release_date,
                    "budget": m.budget,
                    "rating": m.rating
                })

        return JsonResponse(result, safe=False)


def rating_more(request):
    if request.method == "GET":
        rating_limit = request.GET.get("rating")

        if not rating_limit:
            return JsonResponse({"error": "Please give rating"}, status=400)

        # Convert rating to number (ex: "4" → 4)
        rating_limit = float(rating_limit)

        result = []

        for m in movie_details.objects.all():
            # Convert db rating to float
            db_rating = float(m.rating)

            if db_rating > rating_limit:
                result.append({
                    "movie_name": m.movie_name,
                    "release_date": m.release_date,
                    "budget": m.budget,
                    "rating": m.rating
                })

        return JsonResponse(result, safe=False)
