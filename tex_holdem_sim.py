from enum import unique
import re

from urllib3 import Retry
from deck import build_deck; import random, numpy as np, csv


def deal_round(deck:list[dict], players = 3):
    random.shuffle(deck)
    hands = []
    for p in range(players):
        card1 = deck.pop(0)
        card2 = deck.pop(0)
        hands.append([p, (card1, card2)])
    field = []; flop = []
    for x in range(3):
        flp = deck.pop(0)
        deck.pop(0); flop.append(flp); field.append(flp)
    deck.pop(0); turn = deck.pop(0); field.append(turn)
    deck.pop(0); river = deck.pop(0); field.append(river)
    return hands, field

def analyze_hand(hand, field):
    """ Hand Ranks:   
        royalFlush = 1
        straightFlush = 2
        fourKind = 3 #Tested
        fullHouse = 4
        flush = 5 
        straight = 6 
        threeKind = 7 #Tested
        twoPair = 8 #Tested
        onePair = 9 #Tested
        highCard = 10
    """
    suits =  [c['S'] for c in hand]; suits.extend([c['S'] for c in field])
    faces =  [c['F'] for c in hand]; faces.extend([c['F'] for c in field])
    cards = zip(suits,faces)

    print('',suits, faces, '',sep = '\n')

    def find_flush(suits):
        flush = False
        unique_suits = list(set(suits)); unique_suits.sort()
        for us in unique_suits:
            n = suits.count(us)
            if n >= 5:
                flush = True
                break
        return flush        
    print('\tFlush: ',find_flush(suits))

    def find_royal_flush(suits, faces):
        royal_flush = False
        if find_flush(suits):
            required = ['10','Jack','Queen','King','Ace']
            if all([f in required for f in faces]):
                royal_flush = True
        return royal_flush
    print('\tRoyalFlush: ',find_royal_flush(suits, faces))

    def find_straight(faces):
        straight = False
        unique_faces = list(set(faces))
        if len(unique_faces)>=5:
            face_order = ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']
            face_sequence = [face_order.index(uf) for uf in unique_faces];face_sequence.sort()
            tests = [face_sequence[:5], face_sequence[1:7],face_sequence[2:]]
            
            if any([sorted(t) == list(range(min(face_sequence), max(face_sequence)+1)) for t in tests]):
                straight = True
        
        return straight
    print('\tStraight: ',find_straight(faces))

    def find_sets(faces:list[str]):
        hand_faces = faces[:2]
        unique_faces = list(set(faces)); unique_faces.sort()
        pairs = []
        if len(unique_faces) != len(faces):
            for uf in unique_faces:
                n = faces.count(uf)
                if n > 1 and uf in hand_faces:
                    pairs.append([uf, n])

        else:
            pairs = None
        return pairs
    print('\tSets: ',find_sets(faces))

    royalflush = find_royal_flush(suits, faces)
    straightflush = all([find_flush(suits), find_straight(faces)])
    flush = find_flush(suits)
    straight = find_straight(faces)

    if find_sets(faces):
        fourkind = any([s[1]==4 for s in find_sets(faces)])
        threekind = any([s[1]==3 for s in find_sets(faces)])
        twopair = len(find_sets(faces))>1
        onepair = all([len(find_sets(faces))==1, (find_sets(faces)[0])[1] == 2])
        fullhouse = all([onepair, threekind])
    else:
        fourkind, threekind, twopair, onepair, fullhouse = False, False, False, False, False



    
    best_hand = ['High Card', 10]
    if royalflush:
        best_hand = ['Royal Flush', 1]
    elif straightflush:
        best_hand = ['Straight Flush', 2]
    elif fourkind:
        best_hand = ['Four of a Kind', 3]
    elif fullhouse:
        best_hand = ['Full House', 4]
    elif flush:
        best_hand = ['Flush', 5]
    elif straight:
        best_hand = ['Straight', 6]
    elif threekind:
        best_hand = ['Three of a Kind', 7]
    elif twopair:
        best_hand = ['Two Pair', 8]
    elif onepair:
        best_hand = ['One Pair', 9]
    
    return best_hand

if __name__ == '__main__':
    for PLAYER in range(2,10):
        with open('byplayer/'+str(PLAYER)+'_players_texasholdem_output.csv', 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Round', 'Flop, River, Turn', 'Hands'])
            for x in range(100000):
                hands, field = deal_round(build_deck(), PLAYER)

                analysis = []
                for hand in hands:
                    best_hand = analyze_hand((hand)[1], field); analysis.append(best_hand)

                hands_for_chart = []
                for h in hands:
                    hand = []
                    for card in h[1]:
                        hand.append(card['F']+' of '+card['S'])
                        
                    hand = ';\n'.join(hand)
                    hands_for_chart.append(hand)

                field_for_chart = []
                for card in field:
                    field_for_chart.append(card['F']+' of '+card['S'])
                field_for_chart = ';\n'.join(field_for_chart)

                row = [x, field_for_chart]

                row.extend(hands_for_chart)
                row.extend(analysis)

                def determine_winner(hands, field, analysis):
                    levels = [a[1] for a in analysis]
                    best = min(levels)
                    winning_hand = analysis[levels.index(best)]
                    winners = []
                    for a, h in zip(hands, analysis):
                        if a[1] == best:
                            winners.append(h)
                    if len(winners) == 1:
                        winner = [winners[0], winning_hand]
                    else:
                        face_order = ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']
                        card_indexes = []
                        for player, hand in hands:
                            cards = [h['F'] for h in hand]
                            best = max([face_order.index(c) for c in cards])
                            card_indexes.append([player, best])
                        best_cards = [c[1] for c in card_indexes]
                        winning_num = max(best_cards)
                        if best_cards.count(winning_num) == 1:
                            winner = [best_cards.index(winning_num), winning_hand]
                        else:
                            winner = ['Draw', winning_hand]
                    print(winner)
                    return winner


                winner = determine_winner(hands,'\n' ,analysis)
                row.extend(winner)


                writer.writerow(row)

                
                


