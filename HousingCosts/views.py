from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from .models import House
from .forms import HouseForm, ApiSearchForm
import requests
from bs4 import BeautifulSoup


def housing_costs_home(request):
    return render(request, "HousingCosts/HousingCosts_home.html")


# Contains the modelForm
def housing_costs_create(request):
    form = HouseForm()
    if request.method == 'POST':
        form = HouseForm(request.POST)
        if form.is_valid():
            form.save()
            # This resets the form contents, so it is empty after clicking 'submit':
            form = HouseForm()
    # This points to our HouseForm modelForm (defined above):
    context = {'form': form}
    return render(request, "HousingCosts/HousingCosts_create_update.html", context)


def housing_costs_list(request):
    house_list = House.Homes.all()
    context = {'house_list': house_list}
    return render(request, 'HousingCosts/HousingCosts_list.html', context)


# This view creates the Details page based on the primary key of the DB item that is clicked.
def housing_costs_details(request, pk):
    pk = int(pk)
    details = get_object_or_404(House, pk=pk)
    context = {'details': details}
    return render(request, 'HousingCosts/HousingCosts_details.html', context)


# This view uses the same template as the create view, and pre-populates the form with
# the selected house's details. The submit button updates the info stored in DB.
def housing_costs_edit(request, pk):
    house = get_object_or_404(House, pk=pk)
    form = HouseForm(instance=house)

    if request.method == 'POST':
        # this is necessary so that we update existing record, rather than create a new one:
        form = HouseForm(request.POST, instance=house)
        if form.is_valid():
            form.save()
            # If the form is saved, redirect to the details pg for this house.
            return redirect(housing_costs_details, pk=pk)

    context = {'form': form}
    return render(request, 'HousingCosts/HousingCosts_create_update.html', context)


def housing_costs_delete(request, pk):
    house = get_object_or_404(House, pk=pk)
    if request.method == 'POST':
        house.delete()
        return redirect(housing_costs_list)
    context = {'details': house}
    return render(request, 'HousingCosts/HousingCosts_delete.html', context)


def realty_api_display(request, offset=0):
    # API endpoint, headers, and required parameters. Python generates request url automagically from these:
    url = 'https://realty-in-us.p.rapidapi.com/properties/list-for-sale'
    headers = {
        'X-RapidAPI-Host': 'realty-in-us.p.rapidapi.com',
        'X-RapidAPI-Key': '1dda6feeefmsh95fcaa253de27e3p137c53jsn9f798d0c5753'
    }

    listings = []

    # if the payload is saved as a cookie, use that. If there is no cookie, use default Portland params
    try:
        payload = request.session['payload']
    except KeyError:
        # limited to 10 Houses; these search params are used by default on page load:
        payload = {
            'state_code': 'ME',
            'city': 'Portland',
            'offset': offset,
            'limit': 10,
            'sort': 'relevance'
        }

    payload['offset'] = offset

    try:
        # response contains extra data. I only want listings dictionary items:
        # 'address', 'beds', 'bath', 'sqft', 'price'
        response = requests.get(url, headers=headers, params=payload).json()
        # This grabs only ['listings'] data so I can use it in template. Not formatted:
        listings.append(response['listings'])
    except KeyError:
        return realty_api_error(request)

    form = ApiSearchForm()
    # Code below executes when the form is submitted, if it is valid
    if request.method == 'POST':
        try:
            # bind the form contents:
            form = ApiSearchForm(request.POST)
            # use for debugging: print(form.is_valid())
            if form.is_valid():
                state_code = form.cleaned_data['state']
                city = form.cleaned_data['city']
                beds_min = form.cleaned_data['beds']
                baths_min = form.cleaned_data['baths']
                price_max = form.cleaned_data['price']

                # URL Payload is updated with form contents. Headers and endpoint stay the same:
                payload = {
                    'state_code': state_code,
                    'city': city,
                    'beds_min': beds_min,
                    'baths_min': baths_min,
                    'price_max': price_max,
                    'offset': 0,
                    'limit': 10,
                    'sort': 'relevance'
                }
                # pulls the data per search terms and create JSON object
                response = requests.get(url, headers=headers, params=payload).json()

                # This grabs only ['listings'] data so I can use it in template. [list]:
                listings.append(response['listings'])

                # use for debugging: print(listings)
                # update context and re-render template
                print(payload)
                context = {'listings': listings, 'form': form, 'payload': payload}
                # This creates a cookie that saves the search payload so that it will work with 'next page'
                request.session['payload'] = payload
                return render(request, 'HousingCosts/HousingCosts_api.html', context)
        except KeyError:
            return realty_api_error(request)

    # This context is rendered by default if user has not filled out search form:
    context = {'listings': listings, 'form': form, 'payload': payload}
    return render(request, 'HousingCosts/HousingCosts_api.html', context)


def realty_api_error(request):
    context = {}
    return render(request, 'HousingCosts/HousingCosts_api_error.html', context)


def realty_bs_display(request):
    # setting up the soup
    url = 'https://www.consumeraffairs.com/homeowners/fastest-growing-cities.html'
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'html.parser')
    # Only want to focus on the section of the site with city info
    cities = soup.find('section', id='population-growth-by-percentage')

    # empty list will hold city names or headlines
    city_list = []
    for city in cities.find_all('h3'):
        city_list.append(city.text)

    # This list will hold the city taglines with growth data
    summary_list = []
    for summary in cities.find_all('strong'):
        summary_list.append(summary.text)

    # blurb and entry are lists that establish keys for the above lists, then zip together in a dict
    # that can be passed/used in the django template.
    blurb = ['blurb' for i in range(len(summary_list))]
    entry = ['entry' for i in range(len(summary_list))]

    # generate the google maps search URL for each city in the list:
    search_url = 'https://www.google.com/maps/place/'

    # create empty list, split on the first space so we can discard #'1', '#2', etc
    output = []
    for i in city_list:
        output.append(list(i.split(' ', 1)))
    # print(output)

    # append the 2nd element from each resulting list (index=1) to a new list search_terms:
    search_terms = []
    for i in output:
        search_terms.append(i[1])
    # print(search_terms)

    # replace spaces with '+' for url format. enumerate returns the index and the value so we can update it:
    for idx, i in enumerate(search_terms):
        formatted = i.replace(' ', '+')
        search_terms[idx] = search_url + formatted
    # print(search_terms)

    # I can do this with list comprehension, but it is harder to read..
    # ln = [s.replace(' ', '+') for s in search_terms]
    # print(ln)

    # create keys for search link elements
    link = ['link' for i in range(len(summary_list))]

    # define our dictionary based on the above lists, zip them together:
    info = [{b: c, d: e, f: g} for (b, c, d, e, f, g) in zip(entry, city_list, blurb, summary_list, link, search_terms)]
    # print(info)
    context = {'info': info}
    return render(request, 'HousingCosts/HousingCosts_BeautifulSoup.html', context)
