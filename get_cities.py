import csv


def get_capital_cities_coor():
    # Capitals of the countris
    captial = ['Kabul','Bangkok', 'Beijing', 'Jakarta', 'New Delhi', 'Seoul', 'Taipei', 'Kathmandu', 'Lhasa', 'Vientiane',
               'Hanoi', 'Amsterdam', 'Berlin', 'Madrid', 'Rome', 'London', 'Paris', 'Prague', 'Stockholm', 'Vienna',
               'Bratislava', 'Andorra la Vella', 'Athens', 'Belgrade', 'Bratislava', 'Bern', 'Brussels', 'Bucharest',
               'Chisinau', 'Copenhagen', 'Helsinki', 'Budapest', 'Dublin','Kiev', 'Lisbon', 'Ljubljana', 'Luxembourg', 'Minsk',
               'Madrid', 'Moscow', 'Nicosia', 'Monaco', 'Oslo', 'Prague', 'Rome', 'Stockholm', 'Vaduz', 'Vienna',
               'Warsaw', 'Zagreb', 'Ottawa', 'Washington', 'Mexico', 'Belmopan', 'Guatemala', 'Tegucigalpa',
               'San Salvador', 'Managua', 'San Jose', 'Panama', 'Nuuk', 'Podgorica', 'Prague', 'Reykjavik', 'Riga',
               'San Marino', 'Sarajevo', 'Skopje', 'Sofia', 'Stockholm', 'Tallinn', 'Tirana', 'Vaduz', 'Valletta',
               'Vatican', 'Warsaw', 'Zagreb','Algiers',	"Luanda","Saint John's",'Buenos Aires',	'Yerevan','Canberra','Baku','Nassau','Manama','Dhaka','Bridgetown',
               'Brussels',	'Belmopan',	'Porto Novo',	'Thimphu',	'Sarajevo',	'Gaborone','Brasilia',	'Ouagadougou','Phnom Penh','Yaounde','Ottawa','Praia','Moroni','Brazzaville','San Jose','Cairo','Jerusalem','Nairobi','Tarawa Atoll',
               'Kuwait', 'Beirut','Lilongwe','Bamako','Mexico','Monaco','Rabat','Kathmandu','Niamey','Islamabad','Panama',
               'Lima','Kigali','Riyadh','Victoria','Tunis','Ankara','Ashgabat','Abu Dhabi','Harare','Cardiff','Colombo','Riga','Castries','Pristina']

    # Getting the World cities coordination from the file
    cities_world = {}
    with open("./data/worldcities.csv") as file:
        csvreader = csv.reader(file)
        for i, row in enumerate(csvreader):
            if i == 0:
                continue
            coordinates = [row[2], row[3]]
            city_name = row[0]
            if city_name in captial:
                cities_world[city_name] = coordinates

    return cities_world

