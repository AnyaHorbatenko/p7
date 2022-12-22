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

