function randomProperty() {
	var rand=Math.floor(Math.random()*3).toString(2);
	if (rand.length === 1) { rand = "0" + rand; }
	return rand;
}
function makeCard(deck) {
	card = null;
	while (card == null || $.inArray(card, deck) != -1) {
		card = randomProperty() + randomProperty() + randomProperty() + randomProperty();
	}
	return card;
}
function makeDeck() {
	deck = new Array();
	while (deck.length < 81) {
		deck.push(makeCard(deck));
	}
	return deck;
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
	refd = new Object();
	refd[''] = new Array();
	keys = ['00', '01', '10'];
	for (i_a in keys) {
		color = colors[keys[i_a]];
		refd[color] = new Array();
		for (i_b in keys) {
			num = numbers[keys[i_b]];
			refd[color + num] = new Array();
			for (i_c in keys) {
				pat = patterns[keys[i_c]];
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
	rc = colors[card.substring(0,2)] + numbers[card.substring(2,4)] + patterns[card.substring(4,6)] + shapes[card.substring(6,8)];
	return rc;
}
function rtob(card) {
	bc = reverse_colors[card.substring(0,1)] + reverse_numbers[card.substring(1,2)] + reverse_patterns[card.substring(2,3)] + reverse_shapes[card.substring(3,4)];
	return bc;
}

function convert_deck(deck, per_card) {
	rd = new Array();
	for (var card_index in deck) {
		rd.push(per_card(deck[card_index]));
	}
	return rd;
}
function rdtobd(deck) {
	return convert_deck(deck, rtob);
}
function bdtord(deck) {
	return convert_deck(deck, btor);
}

function encode_2bits(bits, arr) {
	if (bits[0] == '1') {
		arr.push('1');
	} else {
		arr.push('0');
		arr.push(bits[1]);
	}
}
function bdtocds(deck) {
	referenceDictionary = makeReferenceDictionary();
	outputBits = new Array();
	for (var index in deck) {
		onNode(btor(deck[index]), referenceDictionary);
	}
}
function cdstord(cds) {
	referenceDictionary = makeReferenceDictionary();
}
