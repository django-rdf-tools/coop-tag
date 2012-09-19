/*
 * 	easyListSplitter 1.0.2 - jQuery Plugin
 *	written by Andrea Cima Serniotti	
 *	http://www.madeincima.eu
 *
 *	Copyright (c) 2010 Andrea Cima Serniotti (http://www.madeincima.eu)
 *	Dual licensed under the MIT (MIT-LICENSE.txt)
 *	and GPL (GPL-LICENSE.txt) licenses.
 *
 *	Built for jQuery library
 *	http://jquery.com
 *
 */
 
 /*
	To activate the plugin add the following code to your own js file:
	
	$('.your-list-class-name').easyListSplitter({ 
			colNumber: 3,
			direction: 'horizontal'
	});
	
 */

var j = 1;
 
(function($) {
	$.fn.easyListSplitter = function(options) {
	
	var defaults = {
		colNumber: 2, // Insert here the number of columns you want. Consider that the plugin will create the number of cols requested only if there are enough items in the list.
		direction: 'vertical'
	};
			
	this.each(function() {
		
		var obj = $(this);
		var settings = $.extend(defaults, options);
		var totalListElements = $(this).children('li').size();
		var baseColItems = Math.ceil(totalListElements / settings.colNumber);
		var listClass = $(this).attr('class');
		
		// -------- Create List Elements given colNumber ------------------------------------------------------------------------------
		
		for (i=1;i<=settings.colNumber;i++)
		{
			if(i==1){
				$(this).addClass('listCol1').wrap('<div class="listContainer'+j+'"></div>');
			} else if($(this).is('ul')){ // Check whether the list is ordered or unordered
				$(this).parents('.listContainer'+j).append('<ul class="listCol'+i+'"></ul>');
			} else{
				$(this).parents('.listContainer'+j).append('<ol class="listCol'+i+'"></ol>');
			}
				$('.listContainer'+j+' > ul,.listContainer'+j+' > ol').addClass(listClass);
		}
		
		var listItem = 0;
		var k = 1;
		var l = 0;
		
		if(settings.direction == 'vertical'){ // -------- Append List Elements to the respective listCol  - Vertical -------------------------------
			
			$(this).children('li').each(function(){
				listItem = listItem+1;
				if (listItem > baseColItems*(settings.colNumber-1) ){
					$(this).parents('.listContainer'+j).find('.listCol'+settings.colNumber).append(this);
				}
				else {
					if(listItem<=(baseColItems*k)){
						$(this).parents('.listContainer'+j).find('.listCol'+k).append(this);
					}
					else{
						$(this).parents('.listContainer'+j).find('.listCol'+(k+1)).append(this);
						k = k+1;
					}
				}
			});
			
			$('.listContainer'+j).find('ol,ul').each(function(){
				if($(this).children().size() === 0) {
				$(this).remove();
				}
			});
			
		} else{  // -------- Append List Elements to the respective listCol  - Horizontal ----------------------------------------------------------
			
			$(this).children('li').each(function(){
				l = l+1;

				if(l <= settings.colNumber){
					$(this).parents('.listContainer'+j).find('.listCol'+l).append(this);
					
				} else {
					l = 1;
					$(this).parents('.listContainer'+j).find('.listCol'+l).append(this);
				}
			});
		}
		
		$('.listContainer'+j).find('ol:last,ul:last').addClass('last'); // Set class last on the last UL or OL
		j = j+1;
		
	});

	};

})((typeof window.jQuery == 'undefined' && typeof window.django != 'undefined') ? django.jQuery : jQuery);
