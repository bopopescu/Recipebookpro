//Set height and width first???
	function helper(){
		help = document.getElementsByClassName('help');
		helpRecipeNames = document.getElementById('helpRecipeNames');
		if(help[0].style.display === 'block'){
			help[0].style.display = '';
			help[1].style.display = '';
			helpRecipeNames.style.display = '';
		}
		else{
			help[0].style.display = 'block';
			help[1].style.display = 'block';
			helpRecipeNames.style.display = 'block';
		}
	};
	function ingredientClick(){
		if(i.value === i.defaultValue && i.style.color==='grey'){
			i.value = '';
			i.style.color = 'black';
		}
	};
	function ingredientBlur(){
		if(i.value === ''){
			i.value = i.defaultValue;
			i.style.color = 'grey';
		}
	};
	function randomClicked(){
		if(i.value === 'ingredient'){
			i.value = '';
		}
	};
	$(document).ready(function(){
		i = document.getElementById('ingredient');
		i.value = i.defaultValue;
		if (typeof window.DeviceMotionEvent != 'undefined') {
			// Shake sensitivity (a lower number is more)
			var sensitivity = 20;
		
			// Position variables
			var x1 = 0, y1 = 0, z1 = 0, x2 = 0, y2 = 0, z2 = 0;
		
			// Listen to motion events and update the position
			window.addEventListener('devicemotion', function (e) {
				x1 = e.accelerationIncludingGravity.x;
				y1 = e.accelerationIncludingGravity.y;
				z1 = e.accelerationIncludingGravity.z;
			}, false);
		
			// Periodically check the position and fire
			// if the change is greater than the sensitivity
			setInterval(function () {
				var change = Math.abs(x1-x2+y1-y2+z1-z2);
		
				if (change > sensitivity) {
					document.getElementById('randomButton').click();
				}
		
				// Update new position
				x2 = x1;
				y2 = y1;
				z2 = z1;
			}, 150);
		}
	 	
		//Fancybox
	 	$(document).ready(function() {
			$(".fancybox").fancybox({
				'closeBtn' : false,
				'width' : 880,
				helpers	: {
					overlay : {
						css : {
							'background' : 'rgba(240, 240, 240, 0.80)',
						}
					}
				},
			});
		}); 
	
	
		recipeCounter = 0;
		flipbook = $("#flipbook");
		flipbook.turn({
			width:960,
			height:630,
			autoCenter: true,
		});
	 	opened = false;
	 	numberOfPages = flipbook.turn("pages");
		$(window).bind("keydown", function(e){
			//Left key
			if(e.keyCode === 37){
				flipbook.turn('previous');
			}
			else if(e.keyCode === 39){
				flipbook.turn('next');
			}
		});
		//Shifting flipbook when closed 
		flipbook.bind("turned", function(event, page, view) {
			//Turning to page 1 or last page
			if(opened){
				if(flipbook.turn('page')===1){
					flipbook.animate({marginLeft:margin});
					opened = false;
				}
				//check if on last page.
	 			if(flipbook.turn("page") === numberOfPages){
					flipbook.animate({marginLeft: margin+480});
					opened = false
				} 
			}
			else{
				flipbook.animate({marginLeft: margin+230});
				opened = true;
			}
		}); 
		
});