var state_arr = new Array("Andhra Pradesh", "Arunachal Pradesh", "Assam","Bihar", "Chhattisgarh",
			"Dadra and Nagar Haveli", "Daman and Diu", "Delhi", "Goa", "Gujarat", "Haryana", "Himachal Pradesh",
			"Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala", "Lakshadweep", "Madhya Pradesh", "Maharashtra",
			"Manipur","Meghalaya","Mizoram","Nagaland","Orissa","Pondicherry","Punjab","Rajasthan","Sikkim",
			"Tamil Nadu", "Tripura", "Uttar Pradesh", "Uttaranchal", "West Bengal"); 


// States

var s_a = new Array();    // city array

		s_a[0]="";

		s_a[1]="Visakhapatnam|Vijayawada|Guntur|Nellore|Kurnool|Rajahmundry|Kadapa|Kakinada|Tirupati|Anantapur|Vizianagaram|Eluru|Ongole|Nandyal|Machilipatnam|Adoni|Tenali|Proddatur|Chittoor|Hindupur|Bhimavaram|Madanapalle|Srikakulam|Guntakal|Dharmavaram|Gudivada|Narasaraopet|Tadpatri|Tadepalligudem|Chilakaluripet";  

		s_a[2]="Bordumsa|Bubang|Changlang|Chopelling|Deban|Dharampur|Gandhigram|Jairampur|Kharsang|Khemiyong|KheremBisa|Kutum|Basti|Lallung|Manabhum|Manmao|Miao|Namchik|Namdang|Namphai|Namtok|New Mohang|Rajanagar|Rangfrah Covt College|Ranglum|Two-hat|Vijoynagar|Vijoypur|Yangkang";

		s_a[3]="Abhayapuri|Baithalangshu|Barama|Barpeta|Bihupuria|Bijni|Bilasipara|Bokajan|Bokakhat|Boko|Dhakuakhana|Dhemaji|Dhubri|Dibrugarh|Digboi|Diphu|Goalpara|Gohpur|Golaghat|Guwahati|Hailakandi|Hajo|Halflong|Hojai|Howraghat|Jorhat|Karimganj|Kokarajhar|Maibong|Majuli|Mangaldoi|Mariani|Moranhat|Morigaon|Nagaon|Nalbari|North Lakhimpur|Rangapara|Sadiya|Sibsagar|Silchar|Tarabarihat|Tezpur|Tinsukia|Udalgiri|Udarbondh";

		s_a[4]="Ara|Araria|Arwal|Aurangabad|Banka|Begusarai|Bettiah|Bhabhua|Bhagalpur|Bhojpur|Buxar|Chapra|Darbhanga|East Champaran|Motihari|Gaya|Gopalganj|Hajipur|Jamui|Katihar|Khagaria|Kishanganj|Lakhisarai|Madhepura|Madhubani|Monghyr|Muzaffarpur|Nalanda|Nawada|Patna|Purnea|Rohtas|Sasaram|Saharsa|Samastipur|SaranSheikhpura|Sheohar|Sitamarhi|Siwan|Supaul|Vaishali|West Champaran";

		s_a[5]="Ambikapur|Baikunthpur|Balod|Baloda Bazar|Balrampur|Bastar|Bemetara|Bijapur|Bilaspur|Dantewada|Dhamtari|Durg|Gariaband|Jagdalpur|Jashpur|Janjgir-Champa|Kondagaon|Korba|Koriya|Kanker|Kabirdham|Kawardha|Mahasamund|Mungeli|Narayanpur|Raigarh|Rajnandgaon|Raipur|Surajpur|Sukma|Surguja";
		

function populateCities( stateElementId, cityElementId ){
	
	var selectedStateIndex = document.getElementById( stateElementId ).selectedIndex;

	var cityElement = document.getElementById( cityElementId );
	
	cityElement.length=0;	
	cityElement.options[0] = new Option('Select City','');
	cityElement.selectedIndex = 0;
	
	var city_arr = s_a[selectedStateIndex].split("|");
	
	for (var i=0; i<city_arr.length; i++) {
		cityElement.options[cityElement.length] = new Option(city_arr[i],city_arr[i]);
	}
}

function populateStates(stateElementId, cityElementId){

	var stateElement = document.getElementById(stateElementId);
	stateElement.length=0;
	stateElement.options[0] = new Option('Select State','-1');
	stateElement.selectedIndex = 0;
	for (var i=0; i<state_arr.length; i++) {
		stateElement.options[stateElement.length] = new Option(state_arr[i],state_arr[i]);
	}

	if( cityElementId ){
		stateElement.onchange = function(){
			populateCities( stateElementId, cityElementId );
		}
	}
}
