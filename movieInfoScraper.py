from typing import Text, cast, final
import requests
from requests.api import head, request
from bs4 import BeautifulSoup as bs4
import csv
import re
import uuid
import pandas as pd

finalData = []

# x = pd.read_csv("urls.csv")
# for index, row in x.iterrows():
#     print(row[1])


def main():
    # websiteLink = "https://flixable.com/title/2-weeks-in-lagos/"
    websiteLink = "https://flixable.com/title/peaky-blinders/"
    # websiteLink = "https://flixable.com/title/fear-street-part-3-1666/"
    websiteLinks = ["https://flixable.com/title/peaky-blinders/", "https://flixable.com/title/fear-street-part-3-1666/"]
    for websiteLink in websiteLinks:
        res = requests.get(websiteLink)
        htmlPage = bs4(res.text, "html.parser")


        #features to extract
        #title, type (movie or show), director, genres, cast, country, date added, release year, rating, duration, description
        scrapeinfo(htmlPage)
    
    df = pd.DataFrame(finalData)
    df.to_csv("netflixData.csv", index=False, header=['Show Id', 'Title', 'Description', 'Director', 'Genres', 'Cast', 'Production Country', 'Release Date', 'Rating', 'Duration', 'Imdb Score', 'Content Type', 'Date Added'])
    
                                                    

def scrapeinfo(htmlPage):

    movieTitleContainer = htmlPage.find("h1", class_ = "title subpage text-left")
    movieTitle = ""
    if movieTitleContainer:
        movieTitle = movieTitleContainer.text
        print(movieTitle)
    else:
        movieTitle = ""
    
    movieDescriptionContainer = htmlPage.find("p", class_ = "card-description text-white")
    movieDescription = ""
    if movieDescriptionContainer:
        movieDescription = movieDescriptionContainer.text
    else:
        movieDescription = ""
    print(movieDescription)


    #find director
    directorContainer = htmlPage.find(string = re.compile("Director:"))
    director = ""
    if directorContainer:
        directorRealContainer = directorContainer.findNext("span")
        directorAlts = directorRealContainer.findAll("a")
        director = ""
        if directorAlts:
            #ensures that there is no "," after last entry
            for i in range(len(directorAlts)):
                if (i < len(directorAlts)-1):
                    director += directorAlts[i].text
                    director += ", "
                else:
                    director += directorAlts[i].text
    else:
        director = ""
    print(director)

    genreContainer = htmlPage.find("span", text = "Genres:")
    genre = ""
    if genreContainer:
        genreRealContainer = genreContainer.findNext("span")
        genreAlts = genreRealContainer.findAll("a")
        genre = ""
        if genreAlts:
            #ensures that there is no "," after last entry
            for i in range(len(genreAlts)):
                if (i < len(genreAlts)-1):
                    genre += genreAlts[i].text
                    genre += ", "
                else:
                    genre += genreAlts[i].text
    else:
        genre = ""
    print(genre)

    castContainer = htmlPage.find("span", text = "Cast:")
    cast = ""
    if castContainer:
        castRealContainer = castContainer.findNext("span")
        castAlts = castRealContainer.findAll("a")
        cast = ""
        if castAlts:
            #ensures that there is no "," after last entry
            for i in range(len(castAlts)):
                if (i < len(castAlts)-1):
                    cast += castAlts[i].text
                    cast += ", "
                else:
                    cast += castAlts[i].text
    else:
        cast = ""
    print(cast)


    productionCountryContainer = htmlPage.find("span", text = "Production Country:")
    productionCountry = ""
    if productionCountryContainer:
        productionRealContainer = productionCountryContainer.findNext("span")
        productionAlts = productionRealContainer.findAll("a")
        productionCountry = ""
        if productionAlts:
            #ensures that there is no "," after last entry
            for i in range(len(productionAlts)):
                if (i < len(productionAlts)-1):
                    productionCountry += productionAlts[i].text
                    productionCountry += ", "
                else:
                    productionCountry += productionAlts[i].text
    else:
        productionCountry = ""
    print(productionCountry)

    #contains year, duration = (season/length), rating
    cardCategory = htmlPage.find("h6", class_  = "card-category")
    cardSpans = cardCategory.findAll("span")
    movieReleaseYear = ""
    movieRating = ""
    movieDuration = ""
    movieImdbScore = ""
    if (len(cardSpans) == 5):
        for i in range(len(cardSpans)):
            #by looking at previous Kaggle dataset, we know some values of movieRating is missing,
            #to accomodate that, we have an if, else statement
        
            #releaseYear
            if (i == 0):
                movieReleaseYear = cardSpans[i].text
            elif (i == 1):
                movieRating = cardSpans[i].text
            elif (i == 2):
                movieDuration = cardSpans[i].text
            elif (i == 3):
                #logo pass
                pass
            elif (i == 4):
                movieImdbScore = cardSpans[i].text
    elif (len(cardSpans) == 3):
        #means movieImdbScore is missing
        for i in range(len(cardSpans)):
            if (i == 0):
                movieReleaseYear = cardSpans[i].text
            elif (i == 1):
                movieRating = cardSpans[i].text
            elif (i == 2):
                movieDuration = cardSpans[i].text
        movieImdbScore = ""
    elif (len(cardSpans) == 2):
        #means movieImdbScore and movieRating missing
        for i in range(len(cardSpans)):
            if (i == 0):
                movieReleaseYear = cardSpans[i].text
            elif (i == 1):
                movieDuration = cardSpans[i].text
        movieRating = ""
        movieImdbScore = ""
    

    print(movieReleaseYear)
    print(movieRating)
    print(movieDuration)
    print(movieImdbScore)

    
    contentType = ""
    #now we have to decide type based on if 'season' keyword is there or not in movieDuration
    substring = 'min'
    if substring in movieDuration:
        contentType = 'Movie'
    else:
        contentType = 'TV Show'

    print(contentType)

    
    #date added to Netflix
    dateAddedToNetflix = ""
    if contentType == 'Movie':
        dateAddedToNetflixContainer = htmlPage.find(string = re.compile("Added to Netflix:"))
        if dateAddedToNetflixContainer:
            dateRealContainer = dateAddedToNetflixContainer.findNext("span")
            dateAddedToNetflix = dateRealContainer.text
        else:
            dateAddedToNetflix = ""
    else:
        dateAddedToNetflixContainer = htmlPage.find(string = re.compile("New Season Added:"))
        if dateAddedToNetflixContainer:
            dateRealContainer = dateAddedToNetflixContainer.findNext("span")
            dateAddedToNetflix = dateRealContainer.text

        else:
            dateAddedToNetflix = ""
    
    print(dateAddedToNetflix)

    #generate random id for each entry
    id = uuid.uuid4()
    id = str(id)

    #time to all these in finalData
    finalData.append([id, movieTitle, movieDescription, director, genre, cast, productionCountry, movieReleaseYear, movieRating, movieDuration, movieImdbScore, contentType, dateAddedToNetflix])




    









        
        










main()