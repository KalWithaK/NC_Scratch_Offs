from bs4 import BeautifulSoup
from urllib.request import urlopen


#ROI Calculator
def roi_calculator(ticket_price, ovrall_odds, org_przpool, org_przcount, cur_przpool, cur_przcount):
    total_tickets = round(org_przcount * ovrall_odds)
    org_tcktvalue = org_przpool / total_tickets
    cur_ticketcount = round(cur_przcount * ovrall_odds)
    cur_tcktvalue = cur_przpool / cur_ticketcount
    org_roi = (org_tcktvalue - ticket_price) / ticket_price
    cur_roi = round((((cur_tcktvalue - ticket_price) / ticket_price) * 100),2)
   #  print("Original Prize Pool: " + str(org_przpool))
   #  print("Original Number of Prizes: " + str(org_przcount))
   #  print("Original Number of Tickets: " + str(total_tickets))
   #  print("Original Ticket Price: " + str(ticket_price))
   #  print("Original Ticket Value: $" + str(org_tcktvalue))
   #  print("Original Return on Investment: " + "{:.2%}".format(org_roi))
   #  print("Current Ticket Value: $" + str(cur_tcktvalue))
   #  print("Current Return on Investment: " + "{:.2%}".format(cur_roi))
   # print("Current Return on Investment: " + str(cur_roi) + "%")
    return cur_roi



prize_link = "https://nclottery.com/ScratchOffPrizes"
prize_page = urlopen(prize_link).read()
soup_prize = BeautifulSoup(prize_page, 'html.parser')
game_number = 0

one_dollar_game_count = len(soup_prize.find_all('div', attrs={'class':'box cloudfx databox price_1'}))
two_dollar_game_count = len(soup_prize.find_all('div', attrs={'class':'box cloudfx databox price_2'}))
three_dollar_game_count = len(soup_prize.find_all('div', attrs={'class':'box cloudfx databox price_3'}))
five_dollar_game_count = len(soup_prize.find_all('div', attrs={'class':'box cloudfx databox price_5'}))
ten_dollar_game_count = len(soup_prize.find_all('div', attrs={'class':'box cloudfx databox price_10'}))
twenty_dollar_game_count = len(soup_prize.find_all('div', attrs={'class':'box cloudfx databox price_20'}))
twenty_five_dollar_game_count = len(soup_prize.find_all('div', attrs={'class':'box cloudfx databox price_25'}))
thirty_dollar_game_count = len(soup_prize.find_all('div', attrs={'class':'box cloudfx databox price_30'}))
total_number_of_games = one_dollar_game_count+two_dollar_game_count+three_dollar_game_count+five_dollar_game_count+ten_dollar_game_count+twenty_dollar_game_count+twenty_five_dollar_game_count+thirty_dollar_game_count
print(total_number_of_games)
z = 0
a = 0
used_prices = []

for x in range(0, total_number_of_games):
    game_value = str((f"{x:02d}"))
    #Price Value for ID
    game_url_box = (soup_prize.find_all('span', attrs={'class':'gamename'})[z]).find('a')
    game_url = "https://nclottery.com" + game_url_box['href']
    attributes_page = urlopen(game_url).read()
    soup_attributes = BeautifulSoup(attributes_page, 'html.parser')
    ticket_price_box = ((((soup_attributes.find('table', attrs={'class': 'juxtable'})).find('tbody'))).find_all('tr')[0]).find_all('td')[1]
    ticket_price = int(ticket_price_box.text.replace('$', ''))
    a = used_prices.count(ticket_price)
    used_prices.append(ticket_price)

    # Game Number
    game_number_box = (soup_prize.find_all('div', attrs={'class': 'box cloudfx databox price_' + str(ticket_price)})[a].find('span', attrs={'class': 'gamenumber'}))
    game_number = game_number_box.text[-3:]
    # print("Game Number: " + game_number)

    # Game Name
    name_box = ((soup_attributes.find('form', attrs={'name': 'aspnetForm'})).find_all('div', attrs={'class': "band"})[2]).find('h1')
    name = name_box.text[1:]
    # print("Name: " + name)

    # Game Odds
    odds_box = \
    ((((soup_attributes.find('table', attrs={'class': 'juxtable'})).find('tbody'))).find_all('tr')[2]).find_all('td')[1]
    odds = float(odds_box.text[-5:].replace('*', ''))
    # print("Overall Odds: " + str(odds))
    # Number of Rows per game
    number_of_rows: int = len(((soup_prize.find_all('div', attrs={'class': 'box cloudfx databox price_' + str(ticket_price)})[a]).find('tbody')).findAll('tr'))

    # Total prize money Remaining
    total_remaining_prize_value = 0
    for i in range(0, number_of_rows):
        value = (f"{i:02d}")
       # print('ctl00_MainContent_InstantGamesRepeater_ctl' + game_value + '_InstantPrizesRepeater_ctl' + value + '_lblPrizeValueTotalRemaining')
        remaining_prize_value_box = soup_prize.find('span', attrs={'id': 'ctl00_MainContent_InstantGamesRepeater_ctl' + game_value + '_InstantPrizesRepeater_ctl' + value + '_lblPrizeValueTotalRemaining'})
        try:
            remaining_prize_value = int(remaining_prize_value_box.text.replace('$', '').replace(',', ''))
        except:
            remaining_prize_value = 0
        total_remaining_prize_value = total_remaining_prize_value + remaining_prize_value
        # print(remaining_prize_value)
    # print('Total Remaining Prize Value: $' + str(total_remaining_prize_value))

    # Total Prize Count Remaining
    total_remaining_prize_count = 0
    for j in range(0, number_of_rows):
        value = (f"{j:02d}")
        remaining_prize_count_box = soup_prize.find('span', attrs={
            'id': 'ctl00_MainContent_InstantGamesRepeater_ctl' + game_value + '_InstantPrizesRepeater_ctl' + value + '_lblPrizeCountRemaining'})
        remaining_prize_count = int(remaining_prize_count_box.text.replace(',', ''))
        total_remaining_prize_count = total_remaining_prize_count + remaining_prize_count
        # print(remaining_prize_count)
    # print('Total Remaining Prizes: ' + str(total_remaining_prize_count))

    # Original Prize Count
    total_original_prize_count = 0
    for k in range(0, number_of_rows):
        value = (f"{k:02d}")
        original_prize_count_box = soup_prize.find('span', attrs={
            'id': 'ctl00_MainContent_InstantGamesRepeater_ctl' + game_value + '_InstantPrizesRepeater_ctl' + value + '_lblPrizeCount'})
        original_prize_count = int(original_prize_count_box.text.replace(',', ''))
        total_original_prize_count = total_original_prize_count + original_prize_count
        # print(original_prize_count)
    # print('Total Original Prizes: ' + str(total_original_prize_count))

    # Original Prize Value
    total_original_prize_value = 0
    for n in range(0, number_of_rows):
        value = (f"{n:02d}")
        original_prize_count_box = soup_prize.find('span', attrs={
            'id': 'ctl00_MainContent_InstantGamesRepeater_ctl' + game_value + '_InstantPrizesRepeater_ctl' + value + '_lblPrizeCount'})
        original_prize_count = int(original_prize_count_box.text.replace(',', ''))
        original_prize_value_box = soup_prize.find('span', attrs={
            'id': 'ctl00_MainContent_InstantGamesRepeater_ctl' + game_value + '_InstantPrizesRepeater_ctl' + value + '_lblPrizeValue'})
        try:
            original_prize_value = int(original_prize_value_box.text.replace('$', '').replace(',', '')) * original_prize_count
        except:
            original_prize_value = 0
        total_original_prize_value = total_original_prize_value + original_prize_value
        # print(original_prize_value)
    # print('Original Prize Value: $' + str(total_original_prize_value))

    # print("Game Number: " + game_number)
    # print("Name: " + name)
    # print("Overall Odds: " + str(odds))
    # print("Ticket Price: $" + str(ticket_price))
    # print('Total Original Prizes: ' + str(total_original_prize_count))
    # print('Original Prize Value: $' + str(total_original_prize_value))
    # print('Total Remaining Prizes: ' + str(total_remaining_prize_count))
    # print('Total Remaining Prize Value: $' + str(total_remaining_prize_value))
    roi = str((roi_calculator(ticket_price, odds, total_original_prize_value, total_original_prize_count,
                   total_remaining_prize_value, total_remaining_prize_count))) + "%"

    print(name + ": " + roi)
    z = z+1








