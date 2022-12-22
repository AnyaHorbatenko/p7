import argparse
parser = argparse. ArgumentParser(description="")
parser.add_argument("filename")
parser.add_argument("--medals", action="store_true", required=False)
parser.add_argument("--total", action="store_true", required=False)
parser.add_argument("--overall", action="store_true", required=False)
parser.add_argument("--interactive", action="store_true", required=False)
parser.add_argument("--country", required=False)
parser.add_argument("--year", required=False)
parser.add_argument("--output", required=False)

args = parser.parse_args()


def medals(file_name, write_result):
    gold_list = []
    silver_list = []
    bronze_list = []
    with open(file_name, "r") as file:
        head = file.readline()
        lines = file.readlines()
        for line in lines:
            data = line.split("\t")
            country = data[7]
            name = data[1]
            year = data[9]
            medal = data[14].rstrip("\n")
            sport = data[12]
            if str(args.year) == str(year) and args.country == country:
                if str(medal) == "Gold":
                    gold_list.append(name)
                    gold_list.append(sport)
                    gold_list.append(medal)
                elif medal == "Silver":
                    silver_list.append(name)
                    silver_list.append(sport)
                    silver_list.append(medal)
                elif medal == "Bronze":
                    bronze_list.append(name)
                    bronze_list.append(sport)
                    bronze_list.append(medal)
        winner_list = gold_list + silver_list + bronze_list
        winner_amount = int(len(winner_list) / 3)
        counter = 30
        if args.output != None:
            result_file = open(write_result, "w")
        while counter > 0:
            if winner_amount > 0:
                if args.output != None:
                    result_file.write(f'{" - ".join(winner_list[30 - counter:33 - counter])}\n')
                print(" - ".join(winner_list[30 - counter:33 - counter]))
                counter -= 3
                winner_amount -= 1
        print()
        print(int(len(gold_list) / 3), "Gold medals")
        print(int(len(silver_list) / 3), "Silver medals")
        print(int(len(bronze_list) / 3), "Bronze medals")

def total(filename, write_result):
    total = {}
    counter_year = 0
    with open(filename, "r") as file:
        head = file.readline()
        lines = file.readlines()
        for line in lines:
            data = line.split("\t")
            country = data[7]
            year = data[9]
            medal = data[14].rstrip("\n")
            if year == args.year:
                counter_year += 1
                if country not in total:
                    total[country] = [0, 0, 0]
                if medal == "Gold":
                    total[country][0] += 1
                if medal == "Silver":
                    total[country][1] += 1
                if medal == "Bronze":
                    total[country][2] += 1
        if counter_year < 1:
            print("No olympiad was held this year")
        else:
            if args.output != None:
                result_file = open(write_result, "w")
            for i in total:
                if total[i][0] + total[i][1] + total[i][2] > 0:
                    print(f"{i} - {total[i][0]} Gold - {total[i][1]} Silver - {total[i][2]} Bronze")
                    if args.output != None:
                        result_file.write(f'{i} - {total[i][0]} Gold - {total[i][1]} Silver - {total[i][2]} Bronze\n')

def run_overall(file_name, write_result, countries, varilable):
    country_list = countries
    dictionary_overall = {}
    exist_country = 0
    results = {}
    for i in country_list:
        with open(file_name, "r") as file:
            head = file.readline()
            lines = file.readlines()
            for line in lines:
                data = line.split("\t")
                country = data[6]  #uses full name of country
                year = data[9]
                medal = data[14].rstrip("\n")
                if country == i:
                    exist_country += 1
                    if year not in dictionary_overall:
                        dictionary_overall[year] = 0
                    if len(medal) > 3:
                        dictionary_overall[year] += 1
            if exist_country > 0:
                max_val = max(dictionary_overall.values())
                list_of_key = list(dictionary_overall.keys())
                list_of_value = list(dictionary_overall.values())
                position = list_of_value.index(max(dictionary_overall.values()))
                results[i] = f"in year {list_of_key[position]} received {varilable(dictionary_overall.values())} medals"
    if args.output != None:
        result_file = open(write_result, "w")
    if exist_country < 1:
        print("Wrong country")
    else:
        for i in results:
            if args.output != None:
                result_file.write(f'{i} {results[i]}\n')
            print(f"{i} {results[i]}")

def interactive(file_name):
    counter_games = 0
    stats = {}
    first_year = 2022
    first_city = ""
    user_input = input("Write name/code Country: ")
    with open(file_name, "r") as file:
        head = file.readline()
        lines = file.readlines()
        for line in lines:
            data = line.split("\t")
            country = data[6]
            country_code = data[7]
            city = data[11]
            year = data[9]
            medal = data[14].rstrip("\n")
            if user_input in country or user_input in country_code:
#1
                if int(year) < int(first_year):
                    first_year = year
                    first_city = city
                counter_games += 1
                if year not in stats:
                    stats[year] = [0, 0, 0]
                if medal == "Gold":
                    stats[year][0] += 1
                if medal == "Silver":
                    stats[year][1] += 1
                if medal == "Bronze":
                    stats[year][2] += 1
    G_total = 0
    S_total = 0
    B_total = 0
    for i in stats:
        G_total += stats[year][0]
        S_total += stats[year][1]
        B_total += stats[year][2]
    print(f"""
    First participation was in {first_year} in {first_city}
    The most successful olympiad:
    """)
    {run_overall(args.filename, args.output, list(user_input.split(" ")), max)}
    print("The most unsuccessful olympiad:")
    {run_overall(args.filename, args.output, list(user_input.split(" ")), min)}
    print(f"""That team had in avarage {G_total/counter_games} Gold medals, {S_total/counter_games} Silver medals, {G_total/counter_games} Bronze medals
    """)
