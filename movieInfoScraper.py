from typing import cast, final
import requests
from requests.api import request
from bs4 import BeautifulSoup as bs4
import csv

def main():
    # websiteLink = "https://flixable.com/title/2-weeks-in-lagos/"
    websiteLink = "https://flixable.com/title/ozark/"
    res = requests.get(websiteLink)
    htmlPage = bs4(res.text, "html.parser")


    #features to extract
    #title, type (movie or show), director, genres, cast, country, date added, release year, rating, duration, description
    scrapeinfo(htmlPage)


def scrapeinfo(htmlPage):

    movieTitleContainer = htmlPage.find("h1", class_ = "title subpage text-left")
    if movieTitleContainer:
        movieTitle = movieTitleContainer.text
        print(movieTitle)
    else:
        movieTitle = ""
    
    movieDescriptionContainer = htmlPage.find("p", class_ = "card-description text-white")
    if movieDescriptionContainer:
        movieDescription = movieDescriptionContainer.text
    else:
        movieDescription = ""
    print(movieDescription)

    genreContainer = htmlPage.find("span", text = "Genres:")
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


    #now we have to decide type based on if 'season' keyword is there or not in movieDuration


    




        
        










main()