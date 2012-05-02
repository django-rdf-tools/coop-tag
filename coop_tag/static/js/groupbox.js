

function updateCounter (list){
    //console.log(list)
    var items = list.find('input[type=checkbox][checked]');
    var counter = list.prev().children();
    if( items.length > 0 ){
        //console.log(items)
        counter.children().html(items.length);
        counter.show();
        return true;
    }else{
        counter.hide();
        return false;
    }
}

// (function($){
//     $(document).ready(function(){

//         if($('ul.groupbox-list').length > 0 && typeof django.jQuery.fn.columnize === 'function'){
            
//             $('div.groupbox-header').click(function(e){
//                 $(this).next("ul.groupbox-list").slideToggle();
//             });
            
//             $('.groupbox ul').columnize({columns:3}).hide();
//             //$("ul.groupbox-list").easyListSplitter({colNumber:3});
//             $('.groupbox-list input[type=checkbox]').bind('change',function(e){
//                 var parent_list = $(this).parents('ul');
//                 //console.log(parent_list);
//                 updateCounter(parent_list);
//             });
            
//             $('.groupbox-list').each(function(){
//                 var init = updateCounter($(this));
//                 if(init){
//                     $(this).show();
//                 }
//             });
//         }
//     });
// })(
// (typeof window.jQuery == 'undefined' && typeof window.django != 'undefined') ? django.jQuery : jQuery
// );
