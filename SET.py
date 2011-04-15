#!/usr/bin/python2
import random
import itertools

def make_property():
    return bin(random.randint(0,2))[2:].rjust(2,'0')

def make_card(deck):
    card = None
    while card is None or card in deck:
        card = make_property() + make_property() + make_property() + make_property()
    return card

def make_deck():
    deck = []
    while len(deck) < 81:
        deck.append(make_card(deck))
    return deck

# property order: color, number, pattern, shape
colors = {'00': 'P', '01': 'G', '10': 'R'}
reverse_colors = {'P': '00', 'G': '01', 'R': '10'}
numbers = {'00': '1', '01': '2', '10': '3'}
reverse_numbers = {'1': '00', '2': '01', '3': '10'}
patterns = {'00': 'L', '01': 'S', '10': 'O'}
reverse_patterns = {'L': '00', 'S': '01', 'O': '10'}
shapes = {'00': 'C', '01': 'T', '10': 'D'}
reverse_shapes = {'C': '00', 'T': '01', 'D': '10'}

def fresh_ref_dict():
    ref_dict = {'': []}
    for color in colors.values():
        ref_dict[color] = []
        for number in numbers.values():
            ref_dict[color+number] = []
            for pattern in patterns.values():
                ref_dict[color+number+pattern] = []
    return ref_dict

def hex_card_to_bin(hex_card):
    return bin(int(hex_card, 16))[2:].rjust(8,'0')

def bin_card_to_hex(bin_card):
    return hex(int(bin_card, 2))[2:].rjust(2,'0')

def bin_card_to_resolved(bin_card):
    return colors[bin_card[0:2]] + numbers[bin_card[2:4]] + patterns[bin_card[4:6]] + shapes[bin_card[6:8]] 

def resolved_card_to_bin(card):
    return reverse_colors[card[0]] + reverse_numbers[card[1]] + reverse_patterns[card[2]] + reverse_shapes[card[3]] 

def bin_deck_to_hex(deck):
    return [bin_card_to_hex(card) for card in deck]

def hex_deck_to_bin(deck):
    return [hex_card_to_bin(card) for card in deck]

def hex_deck_to_deckstring(deck):
    return ''.join(deck)

def deckstring_to_hex_deck(deckstring):
    deck = []
    for closure in itertools.repeat(lambda: deck.append(None), 81):
        closure()
    for i in range(2, len(deckstring)+2, 2):
        deck[(i-2)/2] = deckstring[i-2:i]
    return deck

def bin_deck_to_resolved(bin_deck):
    return [bin_card_to_resolved(c) for c in bin_deck]

def resolved_deck_to_bin(resolved_deck):
    return [resolved_card_to_bin(c) for c in resolved_deck]

def on_node(node, ref_dict):
     ref_dict[node[:3]].append(node[3:4])
     if len(ref_dict[node[:3]]) == 3:
         ref_dict[node[:2]].append(node[2:3])
         if len(ref_dict[node[:2]]) == 3:
             ref_dict[node[:1]].append(node[1:2])
             if len(ref_dict[node[:1]]) == 3:
                 ref_dict[''].append(node[0:1])

def bin_deck_to_compressed_deckstring(bin_deck):
    ref_dict = fresh_ref_dict()
    #output_bits = [char for char in bin_deck[0]]
    output_bits = []
    def extend(two_bits):
        if two_bits[0] == '1':
            output_bits.append('1')
        else:
            output_bits.extend(two_bits)

    extend(bin_deck[0][0:2])
    extend(bin_deck[0][2:4])
    extend(bin_deck[0][4:6])
    extend(bin_deck[0][6:8])
    #print '%s eeee' % bin_card_to_resolved(bin_deck[0])
    on_node(bin_card_to_resolved(bin_deck[0]), ref_dict)

    def extend(two_bits):
        if two_bits[0] == '1':
            output_bits.append('1')
        else:
            output_bits.extend(two_bits)
    def handle_layer4(node):
        layer4 = ref_dict['']
        #print '%s layer4: %s' % (node, layer4),
        if len(layer4) == 2:
            #print 'n',
            pass
        elif len(layer4) == 1:
            if int(rtob(node)[0:2], 2) > int(reverse_colors[layer4[0]], 2):
                #print 's+a %s' % {'0': '1', '1': '0'}[rtob(node)[1:2]],
                output_bits.append({'0': '1', '1': '0'}[rtob(node)[1:2]])
            else:
                #print 'a %s' % rtob(node)[1:2],
                output_bits.append(rtob(node)[1:2])
        else:
            #print 'e %s' % rtob(node)[0:2],
            extend(rtob(node)[0:2])
    def handle_layer3(node):
        layer3 = ref_dict[node[0]]
        #print 'layer3: %s' % layer3,
        if len(layer3) == 2:
            #print 'n',
            pass
        elif len(layer3) == 1:
            if int(rtob(node)[2:4], 2) > int(reverse_numbers[layer3[0]], 2):
                #print 's+a', {'0': '1', '1': '0'}[rtob(node)[3:4]],
                output_bits.append({'0': '1', '1': '0'}[rtob(node)[3:4]])
            else:
                #print 'a', rtob(node)[3:4],
                output_bits.append(rtob(node)[3:4])
        else:
            #print 'e', rtob(node)[2:4],
            extend(rtob(node)[2:4])
    def handle_layer2(node):
        layer2 = ref_dict[node[0:2]]
        #print 'layer2: %s' % layer2,
        if len(layer2) == 2:
            #print 'n',
            pass
        elif len(layer2) == 1:
            if int(rtob(node)[4:6], 2) > int(reverse_patterns[layer2[0]], 2):
                #print 's+a', {'0': '1', '1': '0'}[rtob(node)[5:6]],
                output_bits.append({'0': '1', '1': '0'}[rtob(node)[5:6]])
            else:
                #print 'a', rtob(node)[5:6],
                output_bits.append(rtob(node)[5:6])
        else:
            #print 'e', rtob(node)[4:6],
            extend(rtob(node)[4:6])
    def handle_layer1(node):
        layer1 = ref_dict[node[0:3]]
        #print 'layer1: %s' % layer1,
        if len(layer1) == 2:
            #print 'n'
            pass
        elif len(layer1) == 1:
            #we know the shape from one bit
            if int(rtob(node)[6:8], 2) > int(reverse_shapes[layer1[0]], 2):
                #print 's+a', {'0': '1', '1': '0'}[rtob(node)[7:8]]
                output_bits.append({'0': '1', '1': '0'}[rtob(node)[7:8]])
            else:
                #print 'a', rtob(node)[7:8]
                output_bits.append(rtob(node)[7:8])
        else:
            #print 'e', rtob(node)[6:8]
            extend(rtob(node)[6:8])

    for bin_node in bin_deck[1:]:
        node = bin_card_to_resolved(bin_node)
        handle_layer4(node)
        handle_layer3(node)
        handle_layer2(node)
        handle_layer1(node)
        on_node(node, ref_dict)
    padding = (4 - len(output_bits) % 4) % 4
    output_bits.extend(itertools.repeat('0', padding))
    deckstring = ''
    for i in range(0, len(output_bits), 4):
        deckstring = (deckstring + 
                hex(int(''.join(output_bits[i:i+4]), 2))[2:])
    return deckstring

class Namespace(object): pass
# function to go the other way goes here
def compressed_deckstring_to_resolved(deckstring):
    ref_dict = fresh_ref_dict()
    bin_deckstring = [c for c in ''.join([bin(int(char, 16))[2:].rjust(4,'0') for char in deckstring])]
    deck = []

    ptr_ns = Namespace()
    ptr_ns.pointer = 0

    def add_card(card):
        #print card
        deck.append(card)
        on_node(card, ref_dict)

    def read_bit():
        bit = bin_deckstring[ptr_ns.pointer]
        #print ptr_ns.pointer,
        ptr_ns.pointer = ptr_ns.pointer + 1
        #print ptr_ns.pointer
        return bit
    def read_2bits():
        first = read_bit()
        if first == '1':
            return '10'
        else:
            return first + read_bit()

    def handle_layer4():
        if len(ref_dict['']) == 2:
            #print 'layer4, got 2',
            finished_colors = ref_dict['']
            real_color = (set('PGR') - set(finished_colors)).pop()
            #print 'color =', real_color,
            return real_color
        elif len(ref_dict['']) == 1:
            #print 'layer4, got 1',
            color = read_bit()
            #print 'color bit =', color,
            finished_color = ref_dict[''][0]
            #print 'finished_color =', finished_color,
            finished_color_num = int(reverse_colors[finished_color], 2)
            if int(color, 2) >= finished_color_num:
                real_color = colors[bin(int(color, 2) + 1)[2:].rjust(2,'0')]
            else:
                real_color = colors['0' + color]
            #print 'color =', real_color,
            return real_color
        else:
            #print 'layer4, got 0',
            color = read_2bits()
            real_color = colors[color]
            #print 'color =', real_color,
            return real_color

    def handle_layer3(real_color):
        if len(ref_dict[real_color]) == 2:
            #print 'layer3, got 2',
            finished_numbers = ref_dict[real_color]
            real_number = (set('123') - set(finished_numbers)).pop()
            #print 'number =', real_number,

            return real_color + real_number
        elif len(ref_dict[real_color]) == 1:
            #print 'layer3, got 1',
            number = read_bit()
            #print 'number bit =', number,
            finished_number = ref_dict[real_color][0]
            #print 'finished_number =', finished_number,
            finished_number_num = int(reverse_numbers[finished_number], 2)
            if int(number, 2) >= finished_number_num:
                real_number = numbers[bin(int(number, 2) + 1)[2:].rjust(2,'0')]
            else:
                real_number = numbers['0' + number]
            #print 'number =', real_number,

            return real_color+real_number
        else:
            #print 'layer3, got 0',
            number = read_2bits()
            real_number = numbers[number]
            #print 'number =', real_number,
            return real_color+real_number

    def handle_layer2(color_number):
        if len(ref_dict[color_number]) == 2:
            #print 'layer2, got 2',
            finished_patterns = ref_dict[color_number]
            real_pattern = (set('LSO') - set(finished_patterns)).pop()
            #print 'pattern =', real_pattern,
            return color_number+real_pattern
        elif len(ref_dict[color_number]) == 1:
            #print 'layer2, got 1',
            pattern = read_bit()
            #print 'pattern bit =', pattern,
            finished_pattern = ref_dict[color_number][0]
            #print 'finished_pattern =', finished_pattern,
            finished_pattern_num = int(reverse_patterns[finished_pattern], 2)
            if int(pattern, 2) >= finished_pattern_num:
                real_pattern = patterns[bin(int(pattern, 2) + 1)[2:].rjust(2,'0')]
            else:
                real_pattern = patterns['0' + pattern]
            #print 'pattern =', real_pattern,
            return color_number+real_pattern
        else:
            #print 'layer2, got 0',
            pattern = read_2bits()
            real_pattern = patterns[pattern]
            #print 'pattern =', real_pattern,
            return color_number + real_pattern

    def handle_layer1(color_number_pattern):
        if len(ref_dict[color_number_pattern]) == 2:
            #print 'layer1, got 2',
            finished_shapes = ref_dict[color_number_pattern]
            real_shape = (set('CTD') - set(finished_shapes)).pop()
            #print 'shape =', real_shape,

            return color_number_pattern + real_shape
        elif len(ref_dict[color_number_pattern]) == 1:
            #print 'layer1, got 1',
            shape = read_bit()
            #print 'shape bit =', shape,
            finished_shape = ref_dict[color_number_pattern][0]
            #print 'finished_shape =', finished_shape,
            finished_shape_num = int(reverse_shapes[finished_shape], 2)
            if int(shape, 2) >= finished_shape_num:
                real_shape = shapes[bin(int(shape, 2) + 1)[2:].rjust(2,'0')]
            else:
                real_shape = shapes['0' + shape]
            #print 'shape =', real_shape,

            return color_number_pattern + real_shape
        else:
            #print 'layer1, got 0',
            shape = read_2bits()
            real_shape = shapes[shape]
            #print 'shape =', real_shape,
            return color_number_pattern + real_shape

    while len(deck) < 81:
        add_card(handle_layer1(
                  handle_layer2(
                   handle_layer3(
                    handle_layer4()))))
    return deck

htob = hex_card_to_bin
btoh = bin_card_to_hex
btor = bin_card_to_resolved
rtob = resolved_card_to_bin

bdtohd = bin_deck_to_hex
hdtobd = hex_deck_to_bin

rdtobd = resolved_deck_to_bin
bdtord = bin_deck_to_resolved

hdtods = hex_deck_to_deckstring
dstohd = deckstring_to_hex_deck

bdtocds = bin_deck_to_compressed_deckstring
cdstord = compressed_deckstring_to_resolved

# CARDS:
# H -> B -> R
# R -> B -> H

# DECKS:
# HD -> BD -> RD
# RD -> BD -> HD

# DECKSTRINGS:
# HD -> DS
# DS -> HD
# BD -> CDS
# CDS -> RD
