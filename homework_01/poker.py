#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

# Задание со *
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. Кроме прочего в данном варианте "рука"
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета, в колоде два джокерва.
# Черный джокер '?B' может быть использован в качестве треф
# или пик любого ранга, красный джокер '?R' - в качестве черв и бубен
# любого ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertools.
# Можно свободно определять свои функции и т.п.
# -----------------
import itertools


def hand_rank(hand):
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)


def card_ranks(hand):
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""
    num_cards = [str(el) for el in range(2, 10)]
    next_cards = ['T', 'J', 'Q', 'K', 'A']
    rank_key = list(itertools.chain(num_cards, next_cards))
    pattern = dict(zip(rank_key, [x for x in range(2, 15)]))
    return sorted([pattern[el[0]] for el in hand], reverse=True)


def flush(hand) -> bool:
    """Возвращает True, если все карты одной масти"""
    pattern = hand[0][1]
    return all((el[1] == pattern for el in hand))


def straight(ranks) -> bool:
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""
    return max(ranks) - min(ranks) == 4



def kind(n, ranks) -> int | None:
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""
    result = [
        el[0]
        for el in [list(g)
                   for k, g in itertools.groupby(ranks)]
        if len(el) == n
    ]
    if result:
        return result[0]
    return None


def two_pair(ranks) -> list[int] | None:
    """Если есть две пары, то возврщает два соответствующих ранга,
    иначе возвращает None"""
    result = [
        el[0]
        for el in [list(g)
                   for k, g in itertools.groupby(ranks)]
        if len(el) == 2
    ]
    if result:
        return result
    return None


def best_hand(hand) -> list[str]:
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """
    best = ([], [0, 0, 0])
    for current in itertools.combinations(hand, 5):
        current_rank = hand_rank(current)
        if current_rank[0] > best[1][0]:
            best = (current, current_rank)
        elif current_rank[0] == best[1][0] and current_rank[1] > best[1][1]:
            best = (current, current_rank)
        elif current_rank[0] == best[1][0] and current_rank[1] == best[1][1]\
                and current_rank[-1] > best[1][-1]:
            best = (current, current_rank)
    return best[0]


def best_wild_hand(hand) -> list[str]:
    """best_hand но с джокерами"""
    joker_substitution = '23456789TJQKA'
    if '?B' in hand:
        black_joker = itertools.product(joker_substitution, 'CS')
        hand.remove('?B')
        black_joker = [i for i in ["".join(el) for el in black_joker] if i not in hand]
        hand.extend(black_joker)
    if '?R' in hand:
        red_joker = itertools.product(joker_substitution, 'HD')
        hand.remove('?R')
        red_joker = [i for i in ["".join(el) for el in red_joker] if i not in hand]
        hand.extend(red_joker)
    return best_hand(hand)


def test_best_hand():
    print("test_best_hand...")
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


def test_best_wild_hand():
    print("test_best_wild_hand...")
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


def test_card_ranks():
    print('test_card_ranks')
    assert card_ranks("6C 7C 8C 9C TC 5C JS".split()) == [11, 10, 9, 8, 7, 6, 5]
    assert card_ranks("6C 2C 8C 9C TC 5C JS".split()) == [11, 10, 9, 8, 6, 5, 2]


def test_flush():
    print('test_flush')
    assert flush("6C 7C 8C 9C 5C".split())
    assert not flush("6C 7C 8C 9C 5S".split())


def test_straight():
    print("test_straight")
    assert straight(card_ranks("7C 8C 9C TC JC".split()))
    assert not straight(card_ranks("2C 3C 5C 6C AC".split()))


def test_kind():
    print("test_kind")
    result = kind(2, card_ranks("6C 6D 8C 8H 8S 5C 5S".split()))
    assert result == 6


def test_kind_None():
    print("test_kind")
    result = kind(2, card_ranks("6C 7D 8C 9H TS 5C 2S".split()))
    assert result is None, result


def test_two_pair():
    print("test_two_pair")
    hand = "6C 6D 8C 5C 5S"
    assert two_pair(card_ranks(hand.split())) == [6, 5]


def test_two_pair_None():
    print("test_two_pair")
    hand = "6C 2D 8C 9H 5S"
    assert two_pair(card_ranks(hand.split())) is None


if __name__ == '__main__':
    test_kind()
    test_kind_None()
    test_flush()
    test_card_ranks()
    test_two_pair()
    test_two_pair_None()
    test_straight()
    test_best_hand()
    test_best_wild_hand()
