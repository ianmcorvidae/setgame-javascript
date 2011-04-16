function randomProperty() {
	var rand=Math.floor(Math.random()*3).toString(2);
	if (rand.length === 1) { rand = "0" + rand; }
	return rand;
}
function makeCard(deck) {
	var card = null;
	while (card == null || $.inArray(card, deck) != -1) {
		card = randomProperty() + randomProperty() + randomProperty() + randomProperty();
	}
	return card;
}
function makeDeck() {
	var deck = new Array();
	while (deck.length < 81) {
		deck.push(makeCard(deck));
	}
	if (deck.length == 81) {
		return deck;
	} else {
		return makeDeck();
	}
}
colors = {'00': 'P', '01': 'G', '10': 'R'}
reverse_colors = {'P': '00', 'G': '01', 'R': '10'}
numbers = {'00': '1', '01': '2', '10': '3'}
reverse_numbers = {'1': '00', '2': '01', '3': '10'}
patterns = {'00': 'L', '01': 'S', '10': 'O'}
reverse_patterns = {'L': '00', 'S': '01', 'O': '10'}
shapes = {'00': 'C', '01': 'T', '10': 'D'}
reverse_shapes = {'C': '00', 'T': '01', 'D': '10'}

function makeReferenceDictionary() {
	var refd = new Object();
	refd[''] = new Array();
	var keys = ['00', '01', '10'];
	for (var i_a in keys) {
		var color = colors[keys[i_a]];
		refd[color] = new Array();
		for (var i_b in keys) {
			var num = numbers[keys[i_b]];
			refd[color + num] = new Array();
			for (var i_c in keys) {
				var pat = patterns[keys[i_c]];
				refd[color+num+pat] = new Array();
	}}}
	return refd;
}

function onNode(node, refd) {
	if (refd[node.substring(0,3)].push(node.substring(3,4)) == 3) {
		if (refd[node.substring(0,2)].push(node.substring(2,3)) == 3) {
			if (refd[node.substring(0,1)].push(node.substring(1,2)) == 3) {
				refd[''].push(node.substring(0,1));
}}}}

function btor(card) {
	var rc = colors[card.substring(0,2)] + numbers[card.substring(2,4)] + patterns[card.substring(4,6)] + shapes[card.substring(6,8)];
	return rc;
}
function rtob(card) {
	var bc = reverse_colors[card.substring(0,1)] + reverse_numbers[card.substring(1,2)] + reverse_patterns[card.substring(2,3)] + reverse_shapes[card.substring(3,4)];
	return bc;
}

function convertDeck(deck, per_card) {
	var rd = new Array();
	for (var card_index in deck) {
		rd.push(per_card(deck[card_index]));
	}
	return rd;
}
function rdtobd(deck) {
	return convertDeck(deck, rtob);
}
function bdtord(deck) {
	return convertDeck(deck, btor);
}

function encodeTwoBits(bits, arr) {
	if (bits[0] == '1') {
		arr.push('1');
	} else {
		arr.push('0');
		arr.push(bits[1]);
	}
}
function bdtocds(deck) {
	var referenceDictionary = makeReferenceDictionary();
	var outputBits = new Array();
	for (var index in deck) {
		onNode(btor(deck[index]), referenceDictionary);
	}
}
function cdstobd(cds) {
	var referenceDictionary = makeReferenceDictionary();
	var cds_array = makeCdsArray(cds);
	var deck = new Array();
	var pointer = 0;
	while (deck.length < 81) {
		deck.push(readCard(cds_array, referenceDictionary));
	}
	return deck
}
function makeCdsArray(cds) {
	var cds_array = new Array();
	for (var i = 0; i < cds.length; i++) {
		var bin = parseInt(cds.substring(i, i+1),16).toString(2);
		while (bin.length < 4) {
			bin = '0' + bin;
		}
		cds_array.push(bin.substring(0,1))
		cds_array.push(bin.substring(1,2))
		cds_array.push(bin.substring(2,3))
		cds_array.push(bin.substring(3,4))
	}
	return cds_array;
}
function readProperty(cds_array, refd, key, dict, reverse_dict) {
	keys = ['00', '01', '10'];
	if (refd[key].length == 2) {
		var finished = refd[key];
		if ($.inArray(dict[keys[0]],finished) != -1) {
			if($.inArray(dict[keys[1]], finished) != -1) {
				var val = dict[keys[2]];
			} else {
				var val = dict[keys[1]];
			}
		} else {
			var val = dict[keys[0]];
		}
		return reverse_dict[val];
	} else if (refd[key].length == 1) {
		var bits = new Array();
		var finished = refd[key][0];
		var bit = cds_array.shift();
		var finished_num = parseInt(reverse_dict[finished],2);
		var bit_num = parseInt(bit, 2);
		if (bit_num >= finished_num) {
			if (bit == '0') {
				bits.push('0');
				bits.push('1');
			} else {
				bits.push('1');
				bits.push('0');
			}
		} else {
			bits.push('0');
			bits.push(bit);
		}
		return bits[0] + bits[1];
	} else {
		var bits = new Array();
		bits.push(cds_array.shift());
		if (bits[0] == '0') {
			bits.push(cds_array.shift());
		} else {
			bits.push('0');
		}
		return bits[0] + bits[1];
	}
}
function readCard(cds_array, refd) {
	var col = readProperty(cds_array, refd, '', colors, reverse_colors);
	var rev_col = colors[col];
	var num = readProperty(cds_array, refd, rev_col, numbers, reverse_numbers);
	var rev_num = numbers[num];
	var pat = readProperty(cds_array, refd, rev_col + rev_num, patterns, reverse_patterns);
	var rev_pat = patterns[pat];
	var shp = readProperty(cds_array, refd, rev_col + rev_num + rev_pat, shapes, reverse_shapes);
	node =  col + num + pat + shp;
	onNode(btor(node), refd);
	return node;
}
