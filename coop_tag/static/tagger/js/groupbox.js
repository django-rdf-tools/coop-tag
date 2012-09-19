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