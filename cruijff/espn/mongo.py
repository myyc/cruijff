from pymongo import MongoClient


def mongo_games():
    mc = MongoClient()
    return mc.get_database("espn").get_collection("games")
