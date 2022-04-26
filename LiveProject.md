# Python Live Project - Code Summary
## Introduction
This live project functioned as a simulation for a real professional working environment as part of a development team. Each of us was tasked with creating an original web application to be incorporated into a shared site built on the Django Web Development Framework.

For my portion of the site, I created a Housing Costs tracker that allows users to enter search parameters to return matching houses through a real estate API, and scraped a website that lists the top 15 fastest growing cities in the US, and returns the results. The app also allows users to create, edit, and delete home entries that they would like to track. 

You are welcome to peruse some of my [Sample Files](https://github.com/salxvador/PythonProjects/tree/main/HousingCosts) from this project.

### CRUD Functionality
#### Create
I began by creating a model for the data elements that I wanted to allow users of my app to track:

![model](https://user-images.githubusercontent.com/98099229/165300143-4d4a7a36-26cd-48bd-81a3-058014c3fec1.png)

I created a template using Django Crispy Forms and implemented my model as a form that would allow users to enter and save data for a tracked home:

![Crispy Form](https://user-images.githubusercontent.com/98099229/165301397-55061194-48e5-41cc-ad46-d6b8b7fc32e7.png)

#### Read
Once a new home is saved to the database, a separate view and template allow the user to examine all of their saved homes:

![List View](https://user-images.githubusercontent.com/98099229/165302186-57aacca5-aa4c-4b89-abbf-f97d5f8111db.png)

#### Update and Delete
Upon examining all saved homes, the user can click on a specific house to access update and delete functionality:

![Update and Delete](https://user-images.githubusercontent.com/98099229/165302647-72df6500-28f1-4040-be82-393f726bf523.png)


### Web Scraping
I used the BeautifulSoup library to scrape ConsumerAffairs.com to return the list of the 15 fastest growing cities in the US. This view function also contains all of the data manipulation required to be able to format the data coherently in the Django template.
As an added bonus for this portion of the project, I parsed the city name into a link that opens google maps to show where the city is located.
```
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
```

DISPLAY PAGE:

![BeautifulSoup Display](https://user-images.githubusercontent.com/98099229/165305162-e4c92c66-3ac3-45cf-b43c-a78a710642c7.png)


### API
Using the Requests Library, I connected to a limited-use free realty API that a user can query, and return matching results. This process includes built-in error handling if the user enters invalid parameters, and also if the API returns no results. Being that it is a free-tier subscription to the API, if we run out of requests for the month, a separate template indicates that the API is unavailable.
```
def realty_api_display(request, offset=0):
    # API endpoint, headers, and required parameters. Python generates request url automagically from these:
    url = 'https://realty-in-us.p.rapidapi.com/properties/list-for-sale'
    headers = {
        'X-RapidAPI-Host': '***',
        'X-RapidAPI-Key': '***'
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
```

I created a simple form for the user to enter their search parameters:

![API Search Form](https://user-images.githubusercontent.com/98099229/165303409-d0872dca-32c4-493b-8d67-b3b5dd95aa6a.png)


### Front-End Development
At the start of this project, the site had minimal styling associated to it. Once I had all of the required funtionality in place, I added more CSS/Bootstrap stylings, as well as JavaScript to bring more interest to the user experience. An example of this was adding a JavaScript Slideshow to the home page to explain what the web app is all about.

![Housing Costs Slideshow](https://user-images.githubusercontent.com/98099229/165305650-23048206-71c8-467e-b46f-8862370d383c.png)

### Skills Acquired
This project was invaluable for getting a solid introduction to the MVC design paradigm, and the implications of working on a shared project as part of a team. We had to collaborate on daily standups, and hone our skills with git/source control to make sure that we implemented our daily changes with respect to the rest of the developers on the project.
I now feel comfortable contributing to and troubleshooting issues in the Django web development framework, an researching possible solutions for new features in Python.
